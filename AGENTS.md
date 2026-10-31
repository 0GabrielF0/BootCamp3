# Instruções para agentes de IA

Contexto e regras para agentes de geração de código (Claude Code, Codex CLI, Cursor e
similares) usados neste repositório. O fluxo é **Spec-Driven Development (SDD)**: a
especificação vem antes do código, e o código só é aceito quando os testes provam que ele
cumpre a especificação.

## Projeto

API que valida placas veiculares brasileiras nos padrões antigo (`AAA9999`) e Mercosul
(`AAA9A99`).

- `app/core/` — domínio puro: `normalizador.py`, `validador.py`, `resultado.py`.
  **Não pode importar FastAPI, Pydantic ou Starlette** (RNF-01; verificado por teste).
- `app/main.py`, `app/schemas.py` — borda HTTP (FastAPI).
- `tests/` — `test_validator.py` (núcleo) e `test_api.py` (contrato HTTP).
- `docs/spec.md` — fonte da verdade (RF, RNF, RN, CT).
- `docs/components.md`, `docs/spec-changelog.md`, `docs/adr/`.

## Comandos

```bash
pip install -r requirements.txt
python -m pytest -v                                         # suíte completa
python -m pytest -v --cov=app.core --cov-report=term-missing # cobertura (meta >= 90%)
docker compose up --build                                   # API em http://127.0.0.1:8000
```

## Fluxo SDD obrigatório

1. **Ler a spec antes de codar.** Toda mudança parte de um RF/RN/CT em `docs/spec.md`.
   Se o pedido não estiver na spec, pare e proponha a alteração na spec primeiro.
2. **Teste antes ou junto do código.** O teste verifica a regra da spec, não o que o código
   já faz. Cite o ID no teste (ex.: `# CT-35`).
3. **Spec mudou? Registre.** Toda alteração de contrato ou regra entra em
   `docs/spec-changelog.md` (versão, origem, motivo, impacto). Nunca reutilize um ID.
4. **Decisão de arquitetura nova? Crie um ADR** em `docs/adr/NNN-titulo.md`.
5. **Nada é mergeado sem revisão humana.** O agente abre a branch e o PR; um integrante lê
   o diff, roda os testes e aprova.

## Regras de código

- Python 3.12, sem dependências novas sem justificativa no PR.
- Mensagens ao usuário em português; códigos de `motivo` seguem o enum de `resultado.py`.
- Não lançar exceção para entrada comum do usuário: devolver `ResultadoValidacao` com `motivo`.
- Mudanças pequenas e focadas; sem refatorações fora do escopo do PR.

## Git

- Branches: `feature/*` ou `docs/*` a partir de `develop`; PR para `develop`; `main` só recebe
  PR de `develop`. Nunca fazer push direto em `main`.
- Commits no formato Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`).
- Use o template de PR (`.github/pull_request_template.md`) e preencha os critérios de aceitação.

## Segurança e privacidade

- Não colar segredos, tokens ou dados pessoais em prompts, código, testes ou logs.
- Não executar comandos destrutivos (`git push --force`, `rm -rf`, reset de histórico) sem
  pedido explícito de um integrante.
- Desconfie de APIs, bibliotecas ou parâmetros sugeridos pelo agente: confirme na
  documentação oficial antes de usar (risco de alucinação; ver
  `docs/relatorio-tecnico-etico.md`).
