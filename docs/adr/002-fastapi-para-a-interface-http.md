# ADR-002 — FastAPI para a interface HTTP

**Status:** Aceita
**Data:** 2026-10-25

**Decisão:** expor a validação por meio de uma API FastAPI.

**Justificativa:** permite definir endpoints, validar requisições e gerar documentação OpenAPI.

**Consequências:** a camada HTTP deve permanecer separada das regras centrais de negócio.
