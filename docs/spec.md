# Especificação Técnica — Validador de Placas Brasileiras

**Versão:** 1.0
**Data:** 2026-09-12
**Status:** Aprovada para a Entrega 1

---

## 1. Descrição do Problema

Sistemas que lidam com veículos (estacionamentos, pedágios, controle de frota, cadastros)
precisam garantir que uma placa informada por um usuário ou por outro sistema realmente
corresponde a um formato oficial de identificação veicular brasileira antes de persistir,
consultar ou processar esse dado. Entradas inválidas geram cadastros duplicados,
consultas que nunca retornam resultado e inconsistência entre bases.

Este projeto entrega um **validador de formato** de placas brasileiras, exposto como:

1. uma **função núcleo** pura, sem dependência de framework; e
2. uma **API HTTP** (FastAPI) que expõe essa função.

Dada uma placa em texto, o sistema informa se ela é **válida**, qual o **padrão**
identificado (antigo ou Mercosul) e, em caso de rejeição, **por que** foi rejeitada.

### 1.1 Padrões suportados

| Padrão | Máscara | Exemplo | Observação |
|---|---|---|---|
| Antigo (pré-2018) | `AAA-9999` | `ABC-1234` | Hífen opcional na entrada |
| Mercosul | `AAA9A99` | `ABC1D23` | 5ª posição é **letra** |

Legenda: `A` = letra A–Z, `9` = dígito 0–9.

### 1.2 Escopo

**Está no escopo:**

- Validação sintática (formato/máscara) das placas nos dois padrões.
- Normalização da entrada antes da validação.
- Identificação do padrão da placa válida.
- Motivo estruturado da rejeição.
- Exposição por API HTTP com contrato documentado.
- Suíte de testes automatizados rastreável a esta especificação.

**Está FORA do escopo (não-objetivos):**

- Consulta a bases oficiais (DENATRAN, DETRAN, SINESP) ou qualquer chamada externa.
- Verificação de **existência real** da placa, do veículo ou do proprietário.
- Consulta de débitos, multas, restrições, roubo/furto ou leilão.
- Placas de outros países do Mercosul (Argentina, Uruguai, Paraguai) ou estrangeiras.
- Placas especiais brasileiras com regra própria de emissão (diplomática, oficial,
  colecionador, experiência) — são tratadas apenas pelo formato, sem regra extra.
- Conversão entre padrão antigo e Mercosul.
- OCR / leitura de placa a partir de imagem.
- Persistência em banco de dados, autenticação e autorização.
- Interface gráfica (front-end).

---

## 2. Requisitos Funcionais

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RF-01** | O sistema deve validar placas no padrão antigo `AAA-9999`. | `ABC-1234` retorna válida com padrão `antigo`. |
| **RF-02** | O sistema deve validar placas no padrão Mercosul `AAA9A99`. | `ABC1D23` retorna válida com padrão `mercosul`. |
| **RF-03** | O sistema deve normalizar a entrada antes de validar (RN-03). | ` abc-1234 ` retorna válida. |
| **RF-04** | O sistema deve informar qual padrão foi identificado em uma placa válida. | Campo `padrao` ∈ {`antigo`, `mercosul`}. |
| **RF-05** | O sistema deve informar a placa em sua forma normalizada. | Campo `placa_normalizada` sempre presente na resposta de sucesso. |
| **RF-06** | O sistema deve rejeitar entradas que não atendam a nenhum padrão, informando o motivo. | Campo `motivo` preenchido com um código de RN violada. |
| **RF-07** | O sistema deve expor a validação por `POST /validar`. | Requisição válida retorna `200` com o corpo do contrato §5.2. |
| **RF-08** | A API deve rejeitar corpo malformado ou campo ausente com erro estruturado. | Retorna `422` no formato §5.4. |
| **RF-09** | A função núcleo deve ser utilizável sem subir a API. | Import direto do módulo núcleo, sem importar FastAPI. |
| **RF-10** | A API deve expor um endpoint de verificação de saúde `GET /health`. | Retorna `200` com `{"status": "ok"}`. |

---

## 3. Requisitos Não-Funcionais

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RNF-01** | O núcleo de validação **não pode** depender do FastAPI, Pydantic ou de qualquer framework web. | Módulo núcleo importa apenas biblioteca padrão (`re`, `dataclasses`, `enum`). |
| **RNF-02** | A validação deve ser determinística e sem efeitos colaterais (função pura). | Mesma entrada produz mesma saída; sem I/O, sem estado global. |
| **RNF-03** | A validação de uma placa deve responder em menos de 5 ms (excluindo overhead HTTP). | Medição local no ambiente Docker padrão do projeto. |
| **RNF-04** | O projeto deve rodar em ambiente padronizado via Docker. | `docker compose up` sobe a API sem passos manuais extras. |
| **RNF-05** | A suíte de testes (pytest) deve cobrir todos os RF e todas as RN. | Cada teste referencia o ID (RF/RN) que verifica. |
| **RNF-06** | Cobertura de testes do módulo núcleo maior ou igual a 90%. | Relatório de cobertura anexado à entrega. |
| **RNF-07** | Toda a documentação, mensagens de erro e códigos de motivo devem estar em português. | Revisão de PR. |
| **RNF-08** | A API deve publicar documentação OpenAPI automática. | `/docs` e `/openapi.json` acessíveis. |
| **RNF-09** | O sistema nunca deve lançar exceção não tratada para entrada de usuário. | Entrada nula, vazia ou binária retorna resposta estruturada, não `500`. |
| **RNF-10** | Código e documentação versionados em Git com fluxo `main` / `feature/*` e PR obrigatório. | Histórico do repositório. |

---

## 4. Regras de Negócio

### 4.1 Formato

| ID | Regra |
|---|---|
| **RN-01** | Uma placa é válida no **padrão antigo** se, após normalização, casar exatamente com `^[A-Z]{3}[0-9]{4}$` (7 caracteres: 3 letras + 4 dígitos). |
| **RN-02** | Uma placa é válida no **padrão Mercosul** se, após normalização, casar exatamente com `^[A-Z]{3}[0-9][A-Z][0-9]{2}$` (7 caracteres: 3 letras, 1 dígito, 1 letra, 2 dígitos). |

### 4.2 Normalização

| ID | Regra |
|---|---|
| **RN-03** | A entrada deve ser normalizada antes da validação, nesta ordem: (1) remover espaços em branco das pontas (`strip`); (2) converter para MAIÚSCULAS; (3) remover **um** hífen separador, se presente. |
| **RN-03.1** | O hífen é **opcional**: `ABC-1234` e `ABC1234` são equivalentes e ambos válidos. |
| **RN-03.2** | Apenas hífens são removidos. Espaços **internos** não são removidos e invalidam a placa (`ABC 1234` é rejeitada por RN-07). |
| **RN-03.3** | A normalização não altera, remove ou transcreve acentos. `ÁBC1234` mantém o `Á` e é rejeitada por RN-08. |
| **RN-03.4** | A resposta de sucesso devolve a placa normalizada **sem hífen** e em maiúsculas (forma canônica de 7 caracteres). |

### 4.3 Rejeição

| ID | Regra | Código de motivo |
|---|---|---|
| **RN-04** | Entrada `None` (nula) é rejeitada. | `ENTRADA_NULA` |
| **RN-05** | Entrada que não seja do tipo texto (`str`) é rejeitada. | `TIPO_INVALIDO` |
| **RN-06** | Entrada vazia ou composta apenas de espaços é rejeitada. | `ENTRADA_VAZIA` |
| **RN-07** | Entrada que, após normalização, não possua exatamente 7 caracteres é rejeitada. | `TAMANHO_INVALIDO` |
| **RN-08** | Entrada com 7 caracteres que contenha caracteres fora de `[A-Z0-9]` (especiais, acentos, pontuação, espaço interno, emoji) é rejeitada. | `CARACTERE_INVALIDO` |
| **RN-09** | Entrada com 7 caracteres alfanuméricos que não case com RN-01 nem com RN-02 é rejeitada. | `FORMATO_DESCONHECIDO` |
| **RN-10** | A ordem de avaliação das rejeições é: RN-04, RN-05, RN-06, RN-07, RN-08, RN-09. O primeiro motivo encontrado é o retornado. | — |
| **RN-11** | Mais de um hífen, ou hífen em posição diferente da 4ª, não é removido pela normalização e leva à rejeição por RN-07 ou RN-08. | — |
| **RN-12** | Uma placa válida pertence a **exatamente um** padrão; os formatos RN-01 e RN-02 são mutuamente exclusivos (a 5ª posição é dígito no antigo e letra no Mercosul). | — |

---

## 5. Contratos de Entrada e Saída

### 5.1 Função núcleo (sem framework — RNF-01)

Módulo: `app/core/validador.py`

```python
from dataclasses import dataclass
from enum import Enum


class Padrao(str, Enum):
    ANTIGO = "antigo"
    MERCOSUL = "mercosul"


class Motivo(str, Enum):
    ENTRADA_NULA = "ENTRADA_NULA"
    TIPO_INVALIDO = "TIPO_INVALIDO"
    ENTRADA_VAZIA = "ENTRADA_VAZIA"
    TAMANHO_INVALIDO = "TAMANHO_INVALIDO"
    CARACTERE_INVALIDO = "CARACTERE_INVALIDO"
    FORMATO_DESCONHECIDO = "FORMATO_DESCONHECIDO"


@dataclass(frozen=True)
class ResultadoValidacao:
    valida: bool
    placa_normalizada: str | None   # forma canônica de 7 caracteres, ou None se rejeitada
    padrao: Padrao | None           # preenchido apenas quando valida is True
    motivo: Motivo | None           # preenchido apenas quando valida is False
    mensagem: str                   # descrição em português, sempre preenchida


def normalizar(entrada: str) -> str:
    """Aplica RN-03. Não valida."""


def validar_placa(entrada: object) -> ResultadoValidacao:
    """Aplica RN-01 a RN-12. Nunca lança exceção (RNF-09)."""
```

**Invariantes do retorno:**

- `valida is True` implica `padrao is not None`, `placa_normalizada is not None` e `motivo is None`.
- `valida is False` implica `motivo is not None` e `padrao is None`.

### 5.2 `POST /validar` — sucesso (placa válida)

**Requisição**

```http
POST /validar HTTP/1.1
Content-Type: application/json

{
  "placa": "abc-1234"
}
```

**Resposta — `200 OK`**

```json
{
  "valida": true,
  "placa_normalizada": "ABC1234",
  "padrao": "antigo",
  "motivo": null,
  "mensagem": "Placa válida no padrão antigo."
}
```

Exemplo Mercosul:

```json
{
  "valida": true,
  "placa_normalizada": "ABC1D23",
  "padrao": "mercosul",
  "motivo": null,
  "mensagem": "Placa válida no padrão Mercosul."
}
```

### 5.3 `POST /validar` — placa inválida

Placa inválida **não** é erro de protocolo: a requisição foi processada com sucesso.
Retorna **`200 OK`** com `valida: false`.

**Requisição**

```json
{ "placa": "AB!1234" }
```

**Resposta — `200 OK`**

```json
{
  "valida": false,
  "placa_normalizada": null,
  "padrao": null,
  "motivo": "CARACTERE_INVALIDO",
  "mensagem": "A placa contém caracteres não permitidos. Use apenas letras de A a Z e dígitos de 0 a 9."
}
```

### 5.4 `POST /validar` — erro de contrato

Corpo ausente, JSON malformado, campo `placa` ausente ou de tipo errado.

**Requisição**

```json
{ "plaka": "ABC1234" }
```

**Resposta — `422 Unprocessable Entity`**

```json
{
  "erro": {
    "codigo": "REQUISICAO_INVALIDA",
    "mensagem": "Corpo da requisição inválido.",
    "detalhes": [
      {
        "campo": "placa",
        "problema": "Campo obrigatório ausente."
      }
    ]
  }
}
```

Formato do objeto de erro:

| Campo | Tipo | Descrição |
|---|---|---|
| `erro.codigo` | `string` | Código estável, em MAIÚSCULAS, para consumo por máquina. |
| `erro.mensagem` | `string` | Descrição em português para leitura humana. |
| `erro.detalhes` | `array` | Lista de `{campo, problema}`; pode ser vazia. |

### 5.5 Tabela de códigos de status

| Status | Situação | Corpo |
|---|---|---|
| `200` | Requisição válida; placa válida **ou** inválida. | §5.2 / §5.3 |
| `422` | Corpo malformado, campo ausente ou tipo errado (RF-08). | §5.4, `codigo: "REQUISICAO_INVALIDA"` |
| `405` | Método HTTP não permitido em `/validar` (ex.: `GET`). | §5.4, `codigo: "METODO_NAO_PERMITIDO"` |
| `500` | Falha interna inesperada. Não deve ocorrer para entrada de usuário (RNF-09). | §5.4, `codigo: "ERRO_INTERNO"` |

### 5.6 `GET /health`

**Resposta — `200 OK`**

```json
{ "status": "ok" }
```

---

## 6. Casos de Teste Esperados

Cada caso referencia o ID da regra que verifica, para rastreabilidade na suíte pytest (RNF-05).

### 6.1 Casos válidos

| # | Entrada | `valida` | `placa_normalizada` | `padrao` | Regra |
|---|---|---|---|---|---|
| CT-01 | `"ABC-1234"` | `true` | `ABC1234` | `antigo` | RN-01, RN-03.1 |
| CT-02 | `"ABC1234"` | `true` | `ABC1234` | `antigo` | RN-01 |
| CT-03 | `"abc-1234"` | `true` | `ABC1234` | `antigo` | RN-03 |
| CT-04 | `"  ABC-1234  "` | `true` | `ABC1234` | `antigo` | RN-03 |
| CT-05 | `" abc1234 "` | `true` | `ABC1234` | `antigo` | RN-03 |
| CT-06 | `"ABC1D23"` | `true` | `ABC1D23` | `mercosul` | RN-02 |
| CT-07 | `"abc1d23"` | `true` | `ABC1D23` | `mercosul` | RN-03 |
| CT-08 | `"ABC-1D23"` | `true` | `ABC1D23` | `mercosul` | RN-03.1 |
| CT-09 | `"AAA0A00"` | `true` | `AAA0A00` | `mercosul` | RN-02 (borda: dígitos mínimos) |
| CT-10 | `"ZZZ9Z99"` | `true` | `ZZZ9Z99` | `mercosul` | RN-02 (borda: limite superior) |
| CT-11 | `"AAA-0000"` | `true` | `AAA0000` | `antigo` | RN-01 (borda: todos zeros) |
| CT-12 | `"ZZZ-9999"` | `true` | `ZZZ9999` | `antigo` | RN-01 (borda: todos noves) |

### 6.2 Casos inválidos

| # | Entrada | `valida` | `motivo` | Regra |
|---|---|---|---|---|
| CT-13 | `None` | `false` | `ENTRADA_NULA` | RN-04 |
| CT-14 | `1234567` (int) | `false` | `TIPO_INVALIDO` | RN-05 |
| CT-15 | `["ABC1234"]` (lista) | `false` | `TIPO_INVALIDO` | RN-05 |
| CT-16 | `""` | `false` | `ENTRADA_VAZIA` | RN-06 |
| CT-17 | `"   "` | `false` | `ENTRADA_VAZIA` | RN-06 |
| CT-18 | `"ABC123"` (6 caracteres) | `false` | `TAMANHO_INVALIDO` | RN-07 |
| CT-19 | `"ABC12345"` (8 caracteres) | `false` | `TAMANHO_INVALIDO` | RN-07 |
| CT-20 | `"A"` | `false` | `TAMANHO_INVALIDO` | RN-07 |
| CT-21 | `"ABC 1234"` (espaço interno) | `false` | `TAMANHO_INVALIDO` | RN-03.2, RN-07 |
| CT-22 | `"AB-C-1234"` (dois hífens) | `false` | `TAMANHO_INVALIDO` | RN-11 |
| CT-23 | `"ABC!234"` | `false` | `CARACTERE_INVALIDO` | RN-08 |
| CT-24 | `"ÁBC1234"` (acento) | `false` | `CARACTERE_INVALIDO` | RN-03.3, RN-08 |
| CT-25 | `"ABÇ1234"` (cedilha) | `false` | `CARACTERE_INVALIDO` | RN-08 |
| CT-26 | `"ABC_1234"` | `false` | `TAMANHO_INVALIDO` | RN-07 (8 caracteres, `_` não é hífen) |
| CT-27 | `"ABC12@4"` | `false` | `CARACTERE_INVALIDO` | RN-08 |
| CT-28 | `"1234ABC"` | `false` | `FORMATO_DESCONHECIDO` | RN-09 |
| CT-29 | `"ABCD123"` (4 letras) | `false` | `FORMATO_DESCONHECIDO` | RN-09 |
| CT-30 | `"AB1C234"` (2 letras iniciais) | `false` | `FORMATO_DESCONHECIDO` | RN-09 |
| CT-31 | `"ABCDEFG"` (só letras) | `false` | `FORMATO_DESCONHECIDO` | RN-09 |
| CT-32 | `"1234567"` (só dígitos) | `false` | `FORMATO_DESCONHECIDO` | RN-09 |
| CT-33 | `"ABC1DD3"` (6ª posição letra) | `false` | `FORMATO_DESCONHECIDO` | RN-09 |

### 6.3 Casos de contrato da API

| # | Requisição | Status | Corpo esperado |
|---|---|---|---|
| CT-34 | `POST /validar` com `{"placa": "ABC-1234"}` | `200` | §5.2, `valida: true` |
| CT-35 | `POST /validar` com `{"placa": "XXX"}` | `200` | §5.3, `valida: false` |
| CT-36 | `POST /validar` com `{"plaka": "ABC1234"}` | `422` | §5.4 |
| CT-37 | `POST /validar` com `{}` | `422` | §5.4 |
| CT-38 | `POST /validar` com `{"placa": 123}` | `422` | §5.4 |
| CT-39 | `POST /validar` com corpo não-JSON | `422` | §5.4 |
| CT-40 | `GET /validar` | `405` | §5.4 |
| CT-41 | `GET /health` | `200` | `{"status": "ok"}` |

---

## 7. Rastreabilidade

| Artefato | Referencia |
|---|---|
| Testes do núcleo (`tests/test_validador.py`) | CT-01 a CT-33; RN-01 a RN-12 |
| Testes da API (`tests/test_api.py`) | CT-34 a CT-41; RF-07, RF-08, RF-10 |
| Decomposição em componentes | `docs/components.md` |
| Histórico de refinamentos desta spec | `docs/spec-changelog.md` |
