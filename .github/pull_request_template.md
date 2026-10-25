## O que muda

<!-- Resumo da alteração + "Closes #N". -->

## Requisitos e regras relacionados

<!-- Ex.: RF-07, RN-03, CT-35. -->

## Critérios de aceitação

- [ ] Harness 100% verde no ambiente padronizado (`docker compose run --rm tests`) e CI verde.
- [ ] Nenhum teste foi alterado ou removido para passar.
- [ ] Mudanças de comportamento estão refletidas em `docs/spec.md` e registradas em `docs/spec-changelog.md`.
- [ ] Novas regras ou casos de borda têm teste associado ao ID CT/RN.
- [ ] Decisões de arquitetura novas têm ADR em `docs/adr/`.
- [ ] Erros lógicos encontrados registrados em `docs/ERROS.md`.
- [ ] Código gerado por IA foi lido e revisado por um integrante.

## Colaboração com IA

<!-- Ferramenta usada, o que foi gerado, o que foi ajustado à mão e por quê. -->

## Como testar

```bash
docker compose run --rm tests
```
