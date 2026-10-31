# Refinamento por Testes, Erros Lógicos e Re-especificação

- **Projeto:** Validador de Placas Brasileiras (BootCamp3)
- **Base analisada:** branch `main`, commit `28b082b`; atualizado em 2026-10-25
- **Evidência de execução:** `python -m pytest -v --cov=app.core --cov-report=term-missing`

## Resultados dos testes automatizados

A suíte foi executada com `python -m pytest -q`, após a instalação das dependências de
`requirements.txt`. Na primeira execução registrada, o resultado foi **47 testes aprovados e
0 falhas** (`47 passed`), em cerca de 0,27 segundo.

A suíte cobre os formatos antigo e Mercosul, a normalização de caixa, espaços nas
extremidades e hífen separador, além de entradas inválidas e casos de borda: valor nulo,
tipo não textual, entrada vazia, tamanho incorreto, espaços internos, caracteres especiais
ou acentuados e padrões alfanuméricos desconhecidos. Os testes da API também verificam
as rotas `/`, `/health` e `/validar`, respostas válidas e inválidas, campo ausente, tipo
incorreto e respostas para rota ou método HTTP não permitidos.

Durante a execução foi exibido um aviso de depreciação do Starlette sobre o uso de `httpx`
com `TestClient`. O aviso não causou falha nos testes.

**Atualização (2026-10-25):** depois que as pendências da seção final foram resolvidas, a
suíte passou a ter **50 testes aprovados, 0 falhas** e **100% de cobertura** em `app/core`.
A execução foi feita no mesmo ambiente do CI (contêiner `python:3.12-slim`). O log completo
está no [README](../README.md#7-execução-dos-testes).

## Inspeção e correção de erros lógicos

A revisão registrada em [`spec-changelog.md`](./spec-changelog.md) identificou que a primeira
versão do PR #9 passava nos 20 testes existentes à época, mas não atendia integralmente à
especificação. As divergências documentadas foram:

- foi implementada a rota `/validate` em vez de `POST /validar` (RF-07);
- faltava o endpoint `GET /health` (RF-10);
- o hífen era obrigatório no padrão antigo, embora a regra previsse hífen opcional (RN-01 e
  RN-03.1);
- a normalização não removia o hífen separador (RN-03 e RN-03.4);
- as respostas de rejeição não incluíam o campo estruturado `motivo` (RN-06 a RN-08).

A estratégia de correção foi alinhar o código e os testes aos requisitos da especificação:
ajustar o contrato das rotas, implementar a normalização definida, retornar o motivo
estruturado e ampliar a suíte. A implementação atual separa a normalização da validação e
testa, entre outros pontos, placas com e sem hífen, letras minúsculas e padrões não
reconhecidos.

O registro também destaca uma causa importante: os testes iniciais foram escritos de modo
a confirmar o comportamento do código, em vez de verificar de forma independente as regras
especificadas.

## Loop de re-especificação

Após a revisão do PR #9, foi feita uma conferência entre a implementação mergeada e a
especificação. O changelog registra ajustes documentais na versão 1.1 para refletir decisões
e componentes efetivamente existentes: os módulos reais do núcleo, o comportamento de
`GET /`, o tratamento documentado de rota inexistente (`404`) e os casos de teste
correspondentes. Essas mudanças foram motivadas pela necessidade de manter a
rastreabilidade entre requisitos, código e testes. Nenhuma regra de negócio central foi
alterada nessa revisão; a especificação foi refinada para descrever corretamente o contrato
e a organização implementados.

A versão 1.1.1 fechou as pendências que a v1.1 marcou como "antes da entrega final" (ver
seção seguinte).

## Pendências e limites da evidência

Na primeira análise, o changelog listava como pendentes os testes de API dos casos CT-35
(`"XXX"`), CT-36 (campo `plaka` no lugar de `placa`) e CT-39 (corpo que não seja JSON), e
não havia relatório de cobertura registrado.

**Situação em 2026-10-25 (spec v1.1.1):**

- CT-35, CT-36 e CT-39 ganharam testes em `tests/test_api.py` e passam.
- A cobertura medida no núcleo é de 100%, acima da meta de 90%.
- Continua em aberto a marcação explícita de cada teste com o ID do CT/RN correspondente
  (P-06 no changelog).

## Evidências consultadas

- [`tests/test_validator.py`](../tests/test_validator.py)
- [`tests/test_api.py`](../tests/test_api.py)
- [`docs/spec.md`](./spec.md)
- [`docs/spec-changelog.md`](./spec-changelog.md)
- [`requirements.txt`](../requirements.txt)
