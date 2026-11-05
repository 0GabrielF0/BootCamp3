# Ciclos de Trabalho — Validador de Placas

Registro da divisão de tarefas, reconstruído a partir das issues, dos Pull Requests e dos commits
do GitHub. O grupo não abriu sprints formais durante o projeto: os ciclos abaixo são agrupamentos
pelas datas reais do histórico, e os nomes na tabela são os logins do GitHub.

## Ciclo 1 — Problema e especificação (10 a 13/09/2026)

**Objetivo:** definir o problema, os requisitos, as regras e a estrutura do repositório.

| Tarefa | Registro | Autor | Revisão |
|---|---|---|---|
| Problema e objetivo | Issue #1 | `0GabrielF0` | — |
| Requisitos | Issue #2 | `0GabrielF0` | — |
| Regras de validação | Issue #3 | `0GabrielF0` | — |
| Arquitetura inicial | Issue #4 | `0GabrielF0` | — |
| Estrutura do repositório | Issue #5 | `0GabrielF0` | — |
| Especificação técnica SDD | Issue #6, PR #7 | `AdlerMrF` | Sem revisão formal registrada |
| Integrantes e detalhes no README | PR #8 | `0GabrielF0` | Sem revisão formal registrada |

## Ciclo 2 — Implementação e primeira re-especificação (15 a 21/10/2026)

**Objetivo:** implementar o validador, os testes e o Docker, e conferir a spec contra o código.

| Tarefa | Registro | Autor | Revisão |
|---|---|---|---|
| Validador, API, testes e Docker | PR #9 | `0GabrielF0` | `AdlerMrF`: mudanças solicitadas, depois aprovação |
| Spec v1.1 | Issue #11, PR #10 | `AdlerMrF` | `0GabrielF0`: comentário e aprovação |

## Ciclo 3 — Consolidação da Entrega 2 (24 e 25/10/2026)

**Objetivo:** produzir o relatório ético-técnico, registrar os erros e fechar as pendências da spec.

| Tarefa | Registro | Autor | Revisão |
|---|---|---|---|
| Relatório técnico-ético | PR #12 | `JeanBrito061` | `arthurgb2005` e `0GabrielF0`: aprovação |
| Refinamento por testes e erros | PR #14 | `Paivadev726` | `AdlerMrF`: aprovação |
| Agentes, ADRs, CT-35/36/39 e spec v1.1.1 | PR #15 | `AdlerMrF` | `0GabrielF0`: aprovação |

## Ciclo 4 — Interface web (31/10/2026)

**Objetivo:** oferecer uma interface visual para a validação.

| Tarefa | Registro | Autor | Revisão |
|---|---|---|---|
| Interface PlacaCheck | PR #16 | `0GabrielF0` | `AdlerMrF`: aprovação |
| README com guia de execução | PR #17 | `0GabrielF0` | `AdlerMrF`: aprovação |
| Governança do projeto (atividade individual) | Issue #13 | `Joseph957-bit-bit` | — |

## Limitações conhecidas do registro

- As issues #1 a #5 e #13 seguem abertas, sem responsável nem milestone.
- Os PRs #7 e #8 foram integrados sem revisão formal no GitHub.
- Os 5 primeiros commits de README foram feitos diretamente em `main`, antes do primeiro PR (ver ADR-006).
