# ADR-003 — Separação entre núcleo e API

**Status:** Aceita
**Data:** 2026-10-25

**Decisão:** manter a normalização, os tipos de resultado e a validação em `app/core/`.

**Justificativa:** reduz o acoplamento com o framework web e permite testar as regras sem depender de requisições HTTP.

**Consequências:** os módulos centrais devem evitar dependências de FastAPI, Pydantic e Starlette.
