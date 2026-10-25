# ADR-007 — Docker para padronização do ambiente

**Status:** Aceita
**Data:** 2026-10-25

**Decisão:** utilizar Docker e Docker Compose para padronizar a execução da aplicação.

**Justificativa:** reduzir diferenças entre ambientes de desenvolvimento e execução.

**Consequências:** a imagem usa `python:3.12-slim`, a mesma versão do CI. Validada em 2026-10-25: `docker compose up --build` sobe a API, `GET /health` responde `{"status":"ok"}` e a suíte passa dentro de um contêiner `python:3.12-slim`.
