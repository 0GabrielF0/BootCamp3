# ADR-006 — Git com branches e Pull Requests

**Status:** Aceita
**Data:** 2026-10-31 (revisada; versão anterior de 2026-10-25)

**Decisão:** utilizar `main` protegida e branches `feature/*` ou `docs/*`, com integração por Pull Requests diretamente em `main`.

**Justificativa:** favorece revisão por pares, rastreabilidade das alterações e proteção da versão principal.

**Consequências:** commits de funcionalidades devem passar pelo fluxo de revisão estabelecido pelo grupo.

**Observação:** a decisão inicial previa uma branch `develop`, citada na Entrega 1, e a versão de 2026-10-25 desta ADR pretendia adotá-la como base dos PRs. Na prática, todos os PRs foram abertos contra `main`, e `develop` não existe mais no repositório. O grupo mantém o fluxo praticado porque `main` protegida com revisão obrigatória atende a um projeto deste porte. Os 5 primeiros commits de README (10 e 11/09/2026) foram feitos diretamente em `main`, antes da proteção da branch e do primeiro PR.
