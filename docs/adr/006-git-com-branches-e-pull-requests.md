# ADR-006 — Git com branches e Pull Requests

**Status:** Aceita
**Data:** 2026-10-25

**Decisão:** utilizar `main`, `develop` e branches `feature/*`, com integração por Pull Requests.

**Justificativa:** favorece revisão por pares, rastreabilidade das alterações e proteção da versão principal.

**Consequências:** commits de funcionalidades devem passar pelo fluxo de revisão estabelecido pelo grupo.

**Observação:** nas Entregas 1 e 2 os PRs foram abertos diretamente contra `main` (protegida). A partir da Entrega 2, novos PRs devem ter `develop` como base.
