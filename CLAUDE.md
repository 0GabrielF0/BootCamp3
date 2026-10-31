# CLAUDE.md

Instruções para o Claude Code neste repositório. As regras comuns a todos os agentes estão
em `AGENTS.md` e valem integralmente aqui:

@AGENTS.md

## Específico do Claude Code

- Antes de editar, leia a seção da spec e os testes relacionados ao pedido.
- Ao terminar uma tarefa, rode `python -m pytest -v` e mostre o resultado real; não declare
  sucesso sem a saída dos testes.
- Prefira propor a alteração e abrir o PR em vez de mergear; o merge é decisão humana.
