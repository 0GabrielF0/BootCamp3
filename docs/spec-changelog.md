# Changelog da Especificação — Validador de Placas Brasileiras

Registro de refinamentos da especificação técnica ([`spec.md`](./spec.md) e
[`components.md`](./components.md)) feitos a partir de feedback do grupo, revisão de PR ou
resultado de testes. Atende ao item **"Refinamento por Feedback"** da Entrega 1.

## Como registrar uma alteração

1. Toda mudança na spec entra por PR, junto com a alteração no documento.
2. Adicione uma nova seção no **topo** da lista de versões (ordem cronológica inversa).
3. Use versionamento semântico do documento:
   - **MAIOR** (`2.0`): mudança que quebra contrato já implementado (rota, formato de
     resposta, semântica de regra existente).
   - **MENOR** (`1.1`): novo RF/RNF/RN ou novo caso de teste, sem quebrar o que existe.
   - **CORREÇÃO** (`1.0.1`): correção de texto, exemplo ou erro de digitação.
4. Nunca reutilize um ID (RF/RNF/RN/CT) aposentado. Marque-o como `OBSOLETO` e crie um novo.
5. Sempre preencha o **motivo** e o **impacto nos testes**.

### Modelo de entrada

```markdown
## vX.Y — AAAA-MM-DD

**Origem:** (revisão de PR #N | falha no teste CT-NN | decisão em reunião | professor)
**Autor:** Nome

**O que mudou**
- ...

**Motivo**
- ...

**Impacto**
- IDs afetados: ...
- Testes a criar/ajustar: ...
- Código a ajustar: ...
```

---

## v1.1 — 2026-10-21

**Origem:** revisão do PR #9 (implementação do validador) e conferência da spec contra o código mergeado.
**Autor:** Adler Murga Ferreira (RA 22511624)

**Contexto — loop de feedback no PR #9**

A primeira versão do PR #9 passava em todos os testes (20 na época), mas divergia da spec:

- endpoint `/validate` em vez de `POST /validar` (RF-07);
- ausência de `GET /health` (RF-10);
- hífen obrigatório no padrão antigo, contrariando RN-01 e RN-03.1;
- normalização sem a remoção do hífen separador (RN-03, RN-03.4);
- ausência do campo `motivo` com os códigos de RN-06 a RN-08.

Os testes passavam porque verificavam o comportamento do código, não o da especificação.
A revisão pediu mudanças; código e testes foram ajustados à spec (47 testes passando, CI
verde) e as regras de negócio foram mantidas. Lição registrada: um teste só é evidência de
conformidade quando verifica a regra (RN/CT) da spec, e não o que o código já faz.

Depois do merge, a spec foi conferida contra a implementação. As diferenças encontradas
estão abaixo; em todas, a decisão do código foi considerada pertinente e a spec foi
ajustada a ela.

**O que mudou**

- `spec.md` §5.1: os contratos do núcleo passam a indicar o módulo de cada elemento
  (`resultado.py`, `normalizador.py`, `validador.py`), como implementado.
- `spec.md` §5.5: nova linha para `404` em rota inexistente, com `codigo: "REQUISICAO_INVALIDA"`.
- `spec.md` §5.7 (novo): contrato de `GET /`, rota informativa que aponta para `/docs`.
- `spec.md` §6.3: novos casos CT-42 (`GET /`) e CT-43 (`POST /validate` responde `404`),
  ambos já cobertos por `tests/test_api.py`.
- `spec.md` §7: caminho dos testes corrigido para `tests/test_validator.py` e
  rastreabilidade do teste de arquitetura e dos testes do normalizador.
- `components.md`: C4, C5 e C6 apontam para `app/schemas.py` e `app/main.py`; a subpasta
  `app/api/` prevista na v1.0 não foi criada.
- `components.md` C6: tabela de handlers, incluindo o motivo de registrar a
  `HTTPException` do Starlette (erros `404`/`405` de roteamento).
- `components.md` §6: arquivo de teste de cada unidade e localização do teste de arquitetura.
- `components.md`: documentado `app/validator.py` como módulo de compatibilidade.

**Motivo**

- Manter a rastreabilidade (RNF-05) fiel ao repositório: referência a arquivo inexistente
  quebra o vínculo entre regra, teste e código.
- Registrar comportamentos da API que já existiam e eram testados, mas não estavam na spec
  (`GET /`, `404` com erro padronizado).
- A separação domínio × borda (RNF-01) foi preservada; só a organização física da borda
  ficou mais simples.

**Impacto**

- IDs afetados: §5.5, §5.7 (novo), CT-42 e CT-43 (novos). Nenhum RF, RNF ou RN mudou.
- Testes a criar/ajustar: ver P-05 e P-06.
- Código a ajustar: nenhum.

---

## v1.0 — 2026-09-12

**Origem:** especificação inicial da Entrega 1 (Spec-Driven Development).
**Autor:** Adler Murga Ferreira (RA 22511624)

**O que mudou**

- Criação de `docs/spec.md`: descrição do problema, escopo e não-objetivos, 10 requisitos
  funcionais (RF-01 a RF-10), 10 requisitos não-funcionais (RNF-01 a RNF-10), 12 regras de
  negócio (RN-01 a RN-12), contratos da função núcleo e da API (`POST /validar`,
  `GET /health`) e 41 casos de teste (CT-01 a CT-41).
- Criação de `docs/components.md`: decomposição em seis unidades (C1 normalizador,
  C2 validador núcleo, C3 modelo de resultado, C4 schemas Pydantic, C5 camada API,
  C6 tratador de erros), interfaces entre elas e diagramas Mermaid.
- Criação deste changelog.

**Decisões registradas**

- Placa inválida responde `200` com `valida: false`; `422` fica reservado a erro de
  contrato HTTP. Motivo: separar "requisição malformada" de "resposta de negócio negativa".
- O núcleo de validação não importa FastAPI nem Pydantic (RNF-01), com teste de arquitetura
  como guarda. Motivo: permitir testar e reutilizar as regras sem subir servidor.
- O motivo da rejeição é um código fechado (`Motivo`), não texto livre. Motivo: permitir que
  os testes referenciem a regra violada de forma estável.
- Validação é apenas sintática; consulta a bases oficiais fica fora do escopo. Motivo:
  manter a Entrega 1 sem dependência externa e com testes determinísticos.

**Impacto**

- IDs afetados: todos (versão inicial).
- Testes a criar: `tests/test_normalizador.py`, `tests/test_validador.py`,
  `tests/test_api.py`, `tests/test_arquitetura.py`.
- Código a criar: `app/core/` (C1–C3) e `app/api/` (C4–C6).

---

## Pendências conhecidas (candidatas a v1.1)

| Item | Descrição | Disparador |
|---|---|---|
| P-01 | Endpoint de validação em lote (`POST /validar-lote`). | Se surgir requisito de importação de planilha. |
| P-02 | Regra para placas de motocicleta / formatos especiais. | Feedback do professor ou do grupo. |
| P-03 | Aceitar separador diferente de hífen (espaço, ponto). | Se os testes apontarem entrada real nesse formato. |
| P-04 | Internacionalização das mensagens. | Fora do escopo enquanto RNF-07 valer. |
| P-05 | Cobrir na API os casos CT-35 (`"XXX"`), CT-36 (`{"plaka": ...}`) e CT-39 (corpo não-JSON), ainda sem teste. | Antes da entrega final. |
| P-06 | Marcar cada teste com o ID do CT/RN que verifica (RNF-05), para rastreabilidade direta no relatório de testes. | Antes da entrega final. |
| P-07 | Remover `app/validator.py` quando nada mais depender do caminho antigo. | Próxima limpeza de código. |
