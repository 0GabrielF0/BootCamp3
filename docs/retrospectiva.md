# Retrospectiva de Aprendizados — Validador de Placas Brasileiras

**Projeto:** BootCamp3 · **Repositório:** https://github.com/0GabrielF0/BootCamp3

## 1. Eficácia dos agentes de IA no fluxo SDD

O grupo usou o **Claude Code** como apoio na especificação, na implementação, nos testes e
na documentação. A IA foi mais eficaz quando trabalhou **a partir da especificação**: as
tabelas de regras de negócio e os 43 casos de teste da spec foram convertidos com rapidez em
testes parametrizados, e a conferência da spec contra o código mergeado gerou a versão 1.1
com as diferenças registradas.

O limite apareceu no **PR #9**: a primeira versão passava em todos os 20 testes da época, mas
divergia da spec em 5 pontos (rota `/validate`, ausência de `/health`, hífen obrigatório,
normalização incompleta e falta do campo `motivo`). Código e testes tinham sido gerados
juntos e concordavam entre si, mesmo errados. Quem encontrou o problema foi a **revisão
humana do PR**, comparando o código com a spec.

**Conclusão do grupo:** no SDD, a IA é eficaz como ferramenta de produção, desde que a spec
seja a referência independente e um integrante revise o resultado contra ela.

## 2. Ganho de produtividade

O grupo não mediu tempo de forma controlada, então o ganho é descrito pelo que foi entregue.
Com apoio da IA, o projeto chegou a:

- **47 testes automatizados, 100% aprovados**, e **100% de cobertura** do núcleo de
  validação, acima da meta de 90% da spec;
- especificação com 10 requisitos funcionais, 10 não funcionais, 12 regras de negócio e
  43 casos de teste, mantida alinhada ao código (v1.0 → v1.1);
- documentação de arquitetura, decisões técnicas (ADRs) e relatório técnico-ético
  produzidos junto com o código, e não só no final.

O ganho real veio da combinação de IA com especificação: a IA acelerou a escrita, e a spec
com casos numerados deu um critério objetivo para saber quando cada parte estava pronta.

## 3. Principais dificuldades superadas

| Dificuldade | Como foi superada |
|---|---|
| Testes verdes que não provavam conformidade (PR #9) | A revisão do PR pediu mudanças; código e testes foram refeitos a partir da spec até os 47 testes atuais. |
| Erros 404 e 405 fora do formato padronizado da API | Descobrimos que esses erros vêm do Starlette e registramos o tratador nessa classe; agora todo erro segue o contrato da spec. |
| Documentação desatualizada depois do merge | A spec foi conferida contra o repositório e corrigida na v1.1, com motivo e impacto no changelog. |
| Conflitos entre branches locais e remotas | O fluxo foi simplificado: sem a branch `develop`, cada pessoa cria sua branch a partir da `main` atualizada e abre PR direto para ela. |
| Erro 403 no push por credenciais trocadas | Ajustamos o login e a identidade do Git (`git config`) para que cada commit saísse com o autor correto. |

## 4. Lições aprendidas sobre governança em equipe

- **Nada vai direto para a `main`.** A branch principal é protegida e só recebe PR com pelo
  menos uma aprovação; quem abre o PR não aprova o próprio.
- **Uma branch por tarefa, com nome `pessoa/assunto`.** O nome mostra de quem é e do que se
  trata, e branches curtas reduzem conflitos.
- **Testes automáticos em todo PR.** O GitHub Actions roda a suíte antes do merge (no PR #12,
  aprovado em 17 s), e a revisão humana confere o resto.
- **A spec também passa por PR.** Toda mudança de especificação entra pelo mesmo fluxo, com
  registro no `spec-changelog.md`.
- **Autoria e rastreabilidade importam.** Commits com o autor certo e PRs com descrição clara
  deixam o histórico confiável para revisão e avaliação.

## 5. Avaliação final

O projeto atingiu o objetivo: um validador de placas testado, documentado e construído por um
processo rastreável. A principal lição é que **a IA aumenta a velocidade, mas a qualidade vem
da especificação e da revisão em equipe**.

Para próximos projetos, o grupo levaria desde o primeiro dia:

- testes escritos direto das tabelas da spec e marcados com o ID que verificam;
- Docker e medição de cobertura configurados no início;
- branches curtas.
