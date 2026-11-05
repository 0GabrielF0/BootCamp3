# Decomposição em Unidades — Validador de Placas Brasileiras

**Versão:** 2.0
**Data:** 2026-10-31
**Documento base:** [`spec.md`](./spec.md)

Objetivo: dividir o sistema em unidades independentes e testáveis, de modo que cada uma
possa ser implementada, revisada e testada isoladamente (desenvolvimento iterativo),
respeitando **RNF-01** (o núcleo não depende de framework web).

---

## 1. Visão Geral das Camadas

| Camada | Componente | Módulo | Depende de |
|---|---|---|---|
| Domínio | C1 — Normalizador | `app/core/normalizador.py` | biblioteca padrão |
| Domínio | C2 — Validador núcleo | `app/core/validador.py` | C1, biblioteca padrão |
| Domínio | C3 — Modelo de resultado | `app/core/resultado.py` | biblioteca padrão |
| Borda | C4 — Schemas Pydantic | `app/schemas.py` | Pydantic, C3 (apenas valores) |
| Borda | C5 — Camada API | `app/main.py` | FastAPI, C2, C4 |
| Borda | C6 — Tratador de erros | `app/main.py` (handlers registrados na aplicação) | FastAPI, Starlette |
| Borda | C7 — Interface web PlacaCheck | `app/static/` (`index.html`, `style.css`, `script.js`) | Contrato HTTP de C5 |

Na v1.0 a borda estava prevista em uma subpasta `app/api/`. A implementação concentrou
rotas e handlers em `app/main.py` e os schemas em `app/schemas.py`: com três rotas e
três handlers, a subpasta não trazia ganho de organização. A separação domínio × borda
(RNF-01), que é o que a decomposição exige, foi mantida.

**Regra de dependência (obrigatória):** as setas apontam sempre da borda para o domínio.
Nenhum módulo em `app/core/` pode importar `fastapi`, `pydantic`, `starlette` ou módulos
da borda. Essa regra é verificada por um teste automatizado (ver §6).

---

## 2. Componentes

### C1 — Normalizador

**Responsabilidade:** transformar a entrada bruta na forma canônica definida em **RN-03**.
Não decide se a placa é válida.

**Interface:**

```python
def normalizar(entrada: str) -> str:
    """RN-03: strip -> upper -> remove um hífen separador. Retorna a forma canônica."""
```

- Entrada: `str` (o chamador já garantiu o tipo).
- Saída: `str` normalizada. Pode ter tamanho diferente de 7 — quem julga é C2.
- Sem efeitos colaterais, sem exceções esperadas.

**Testável isoladamente por:** CT-03, CT-04, CT-05, CT-08, CT-21, CT-22.

---

### C2 — Validador núcleo

**Responsabilidade:** aplicar **RN-01, RN-02 e RN-04 a RN-12** e produzir um
`ResultadoValidacao`. É o coração do sistema e o único lugar onde as regras vivem.

**Interface:**

```python
def validar_placa(entrada: object) -> ResultadoValidacao:
    """Aplica a ordem de rejeição de RN-10. Nunca lança exceção (RNF-09)."""
```

- Entrada: `object` — aceita qualquer coisa, inclusive `None` e tipos não-texto, porque
  RN-04 e RN-05 fazem parte das regras.
- Saída: `ResultadoValidacao` (C3).
- Usa C1 internamente. Não conhece HTTP, JSON, status code ou Pydantic.

**Testável isoladamente por:** CT-01 a CT-33.

---

### C3 — Modelo de resultado

**Responsabilidade:** representar o resultado da validação como dado, com vocabulário
fechado, sem depender de framework.

**Interface:** `Padrao` (Enum), `Motivo` (Enum) e `ResultadoValidacao` (dataclass imutável),
conforme §5.1 da `spec.md`.

Invariantes:

- `valida is True` implica `padrao` e `placa_normalizada` preenchidos e `motivo is None`.
- `valida is False` implica `motivo` preenchido e `padrao is None`.

**Testável isoladamente por:** testes de invariante sobre cada resultado retornado por C2.

---

### C4 — Schemas Pydantic

**Responsabilidade:** contrato de serialização da API. Valida a **forma do corpo HTTP**
(campo `placa` presente e do tipo texto) e serializa a resposta. **Não** contém regra de
negócio de placa — a decisão de validade é sempre de C2.

**Interface:**

```python
class ValidarPlacaRequest(BaseModel):
    placa: str

class ValidarPlacaResponse(BaseModel):
    valida: bool
    placa_normalizada: str | None
    padrao: str | None
    motivo: str | None
    mensagem: str

class DetalheErro(BaseModel):
    campo: str
    problema: str

class ErroResponse(BaseModel):
    erro: CorpoErro   # codigo, mensagem, detalhes: list[DetalheErro]
```

**Fronteira de responsabilidade:** falha no schema produz `422` (RF-08, CT-36 a CT-39).
Falha de regra de negócio produz `200` com `valida: false` (CT-35).

**Testado por:** testes de contrato da API em `tests/test_api.py` (os schemas são exercitados
pelo `TestClient`; não há suíte de serialização separada).

---

### C5 — Camada API

**Responsabilidade:** adaptar HTTP para chamada de função e vice-versa. É uma camada fina,
sem lógica de decisão.

**Interface (endpoints):**

| Método | Rota | Entrada | Saída |
|---|---|---|---|
| `POST` | `/validar` | `ValidarPlacaRequest` | `200` `ValidarPlacaResponse` |
| `GET` | `/health` | — | `200` `{"status": "ok"}` |
| `GET` | `/` | — | `200` página PlacaCheck (spec §5.7) |
| `GET` | `/static/*` | — | `200` arquivos da interface (spec §5.8) |

Fluxo do `POST /validar`:

1. FastAPI valida o corpo com C4. Falhou, C6 devolve `422`.
2. Chama `validar_placa(request.placa)` (C2).
3. Converte o `ResultadoValidacao` em `ValidarPlacaResponse` (mapeamento 1:1 de campos).
4. Responde `200` sempre que o passo 2 executou.

**Testável isoladamente por:** CT-34 a CT-43, via `TestClient` do FastAPI.

---

### C6 — Tratador de erros

**Responsabilidade:** converter as exceções do framework no objeto de erro padronizado
de §5.4 da `spec.md` (`REQUISICAO_INVALIDA`, `METODO_NAO_PERMITIDO`, `ERRO_INTERNO`),
garantindo **RNF-09** — nenhum stack trace vaza para o cliente.

**Interface:** handlers registrados em `app/main.py`:

| Exceção | Status | `codigo` |
|---|---|---|
| `RequestValidationError` | `422` | `REQUISICAO_INVALIDA` |
| `StarletteHTTPException` com status `405` | `405` | `METODO_NAO_PERMITIDO` |
| `StarletteHTTPException` com outro status (ex.: `404`) | o próprio status | `REQUISICAO_INVALIDA` |
| `Exception` | `500` | `ERRO_INTERNO` |

O handler é registrado para a `HTTPException` do Starlette, e não só para a do FastAPI,
porque os erros de roteamento (`404`, `405`) são lançados pelo Starlette. Registrar apenas
a classe do FastAPI deixaria esses casos fora do formato de §5.4.

---

### C7 — Interface web PlacaCheck

**Responsabilidade:** permitir o uso da validação pelo navegador (RF-11). Coleta a placa,
chama `POST /validar` e exibe o resultado. A decisão de validade é sempre de C2, por meio de C5.

**Interface:** consome o contrato de §5.2 a §5.4 da `spec.md`. É servida por C5 em `GET /` e
`GET /static/*`, sem servidor separado.

**Testável por:** CT-44 e CT-45 (entrega da página e dos arquivos). O comportamento no
navegador é verificado manualmente com o roteiro de `docs/DEMO.md`.

---

## 3. Interfaces entre Componentes

| De | Para | Contrato |
|---|---|---|
| C5 | C4 | Corpo HTTP (JSON) para `ValidarPlacaRequest` |
| C5 | C2 | `validar_placa(placa: str) -> ResultadoValidacao` |
| C2 | C1 | `normalizar(entrada: str) -> str` |
| C2 | C3 | Constrói `ResultadoValidacao` |
| C5 | C4 | `ResultadoValidacao` para `ValidarPlacaResponse` (mapeamento de campos) |
| C6 | C5 | Intercepta exceções e devolve `ErroResponse` |
| C7 | C5 | `POST /validar` com JSON; exibe `ValidarPlacaResponse` ou `ErroResponse` |

Cada seta acima é um ponto de dublê (`stub`/`fake`) possível, permitindo testar C5 com um
validador falso e testar C2 sem HTTP.

---

## 4. Diagrama

```mermaid
flowchart TD
    Cliente["Cliente HTTP"]
    Navegador["Navegador"]

    subgraph Borda["Camada de Borda (depende de framework)"]
        C5["C5 - Camada API<br/>app/main.py<br/>FastAPI"]
        C4["C4 - Schemas Pydantic<br/>app/schemas.py"]
        C6["C6 - Tratador de erros<br/>handlers em app/main.py"]
        C7["C7 - Interface PlacaCheck<br/>app/static/"]
    end

    subgraph Nucleo["Núcleo de Domínio (RNF-01: sem framework)"]
        C2["C2 - Validador núcleo<br/>validador.py<br/>RN-01, RN-02, RN-04..RN-12"]
        C1["C1 - Normalizador<br/>normalizador.py<br/>RN-03"]
        C3["C3 - Modelo de resultado<br/>resultado.py<br/>Padrao, Motivo, ResultadoValidacao"]
    end

    Navegador -->|"usa a página"| C7
    C7 -->|"POST /validar (JSON)"| C5
    Cliente -->|"POST /validar (JSON)"| C5
    C5 -->|"valida corpo"| C4
    C4 -.->|"corpo inválido: 422"| C6
    C6 -->|"ErroResponse"| Cliente
    C5 -->|"validar_placa(placa)"| C2
    C2 -->|"normalizar(entrada)"| C1
    C1 -->|"forma canônica"| C2
    C2 -->|"ResultadoValidacao"| C3
    C2 -->|"ResultadoValidacao"| C5
    C5 -->|"200 ValidarPlacaResponse"| Cliente

    linkStyle default stroke-width:1px
```

Dependência entre camadas (nunca o inverso):

```mermaid
flowchart LR
    A["app/main.py + app/schemas.py<br/>FastAPI + Pydantic"] --> B["app/core/*<br/>apenas biblioteca padrão"]
    B -. proibido .-> A
```

---

## 5. Ordem de Implementação Sugerida

Cada passo é uma tarefa independente, testável e mergeável por PR próprio:

1. C3 — modelo de resultado (sem lógica).
2. C1 — normalizador + testes de RN-03.
3. C2 — validador núcleo + testes CT-01 a CT-33.
4. C4 — schemas + testes de serialização.
5. C5 — rotas + testes CT-34, CT-35, CT-41.
6. C6 — tratamento de erro + testes CT-36 a CT-40.
7. C7 — interface web + testes CT-44 e CT-45.

Os passos 1 a 3 não dependem de FastAPI e podem ser feitos em paralelo com o
empacotamento Docker.

---

## 6. Testabilidade

| Unidade | Arquivo de teste | Tipo de teste | Dependências externas |
|---|---|---|---|
| C1, C2, C3 | `tests/test_validator.py` | Unitário puro (`pytest.mark.parametrize`) | nenhuma |
| C4, C5, C6 | `tests/test_api.py` | Integração via `TestClient` | FastAPI |
| C7 | `tests/test_api.py` e `docs/DEMO.md` | Entrega via `TestClient` e verificação manual no navegador | FastAPI, navegador |

**Teste de arquitetura (guarda de RNF-01):** `test_nucleo_nao_depende_de_framework_web`, em
`tests/test_validator.py`, lê os módulos de `app/core/` e falha se encontrar referência a
`fastapi`, `pydantic`, `starlette` ou `app.api`. Isso impede que a
regra de dependência seja quebrada em um PR futuro sem que alguém perceba.
