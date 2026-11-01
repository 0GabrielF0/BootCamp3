# Registro de Erros Lógicos — Validador de Placas

Erros que compilavam e rodavam, mas faziam a coisa errada. Cada entrada registra como o erro
foi detectado, a causa, a correção e a prevenção.

**Classificação** (critério SDD): *implementação* = um programador lendo só a spec teria
acertado; *especificação* = a spec permitia a interpretação errada, e a correção entra também
no [`spec-changelog.md`](./spec-changelog.md).

## E-01 · Rota `/validate` em vez de `POST /validar`

- **Detecção:** revisão humana do PR #9 (pedido de mudanças). Os 20 testes da época passavam.
- **Causa:** o código e os testes foram gerados juntos com apoio de IA, e os testes chamavam a
  mesma rota errada que o código expunha. A spec (RF-07) definia `POST /validar`.
- **Correção:** rota renomeada; os testes passaram a usar o contrato da spec (PR #9).
- **Prevenção:** os testes de API são escritos a partir da tabela de contratos da spec, não
  do código.
- **Classificação:** implementação.

## E-02 · Endpoint `GET /health` ausente

- **Detecção:** revisão humana do PR #9. Nenhum teste cobria o requisito.
- **Causa:** o RF-10 foi ignorado na implementação; sem teste, a ausência não aparecia.
- **Correção:** endpoint criado e `test_health` adicionado (PR #9).
- **Prevenção:** todo RF da spec precisa ter ao menos um teste com o ID correspondente.
- **Classificação:** implementação.

## E-03 · Hífen obrigatório no padrão antigo

- **Detecção:** revisão humana do PR #9.
- **Causa:** a regex exigia `ABC-1234`, rejeitando `ABC1234`, que a RN-01 e a RN-03.1 aceitam.
  Os testes só usavam exemplos com hífen, então confirmavam o erro.
- **Correção:** a normalização passou a remover o hífen separador antes da validação; a regex
  ficou `^[A-Z]{3}[0-9]{4}$` (PR #9).
- **Prevenção:** os casos parametrizados cobrem as duas formas (`ABC-1234` e `ABC1234`).
- **Classificação:** implementação.

## E-04 · Normalização sem remover o hífen separador

- **Detecção:** revisão humana do PR #9, ligada ao E-03.
- **Causa:** a normalização fazia só `upper()` e `strip()`, sem a RN-03.4.
- **Correção:** `normalizar()` remove o hífen apenas na posição de separador, e os testes
  `test_normalizador_*` verificam as três situações (separador, outra posição, hífens extras).
- **Prevenção:** cada sub-regra da RN-03 tem um teste próprio.
- **Classificação:** implementação.

## E-05 · Rejeição sem o campo `motivo`

- **Detecção:** revisão humana do PR #9.
- **Causa:** a resposta só dizia `valida: false`, sem o código estruturado da RN-06 a RN-08.
  O teste verificava apenas `valida`, então passava.
- **Correção:** o enum `Motivo` foi criado em `app/core/resultado.py`, e cada rejeição
  devolve o código correspondente (PR #9).
- **Prevenção:** os testes de entradas inválidas comparam o `motivo` esperado, não só o booleano.
- **Classificação:** implementação.

## E-06 · Spec descrevendo componentes que não existiam

- **Detecção:** conferência da spec contra o código mergeado, depois do PR #9 (issue #11).
- **Causa:** a spec v1.0 previa uma subpasta `app/api/` e não descrevia o comportamento de
  `GET /` nem o `404` de rota inexistente. O código real seguiu outro desenho.
- **Correção:** spec v1.1, que alinhou `spec.md` e `components.md` à implementação (PR #10).
- **Prevenção:** a spec muda no mesmo PR que muda o contrato.
- **Classificação:** especificação.

## E-07 · Casos de teste da spec sem teste correspondente

- **Detecção:** auditoria do repositório contra a spec antes da entrega final.
- **Causa:** os casos CT-35 (`"XXX"`), CT-36 (campo `plaka`) e CT-39 (corpo não-JSON) estavam
  na spec, mas nunca foram codificados. A suíte verde escondia a lacuna.
- **Correção:** três testes novos em `tests/test_api.py` (spec v1.1.1, PR #15).
- **Prevenção:** os testes citam o ID do CT (`# CT-35`), o que permite conferir a cobertura
  da tabela da spec.
- **Classificação:** implementação.

## E-08 · Interface adicionada sem atualizar a especificação

- **Detecção:** auditoria do repositório contra os critérios das entregas, depois dos PRs #16 e #17.
- **Causa:** a interface foi implementada e `GET /` mudou de JSON para HTML, mas a spec ainda dizia que
  front-end estava fora do escopo. O teste foi ajustado ao novo comportamento e a suíte seguiu verde.
- **Correção:** spec v2.0, com RF-11, CT-44, CT-45 e o componente C7; CT-42 marcado como obsoleto.
- **Prevenção:** o critério de aceitação do template de PR sobre `docs/spec.md` deve ser conferido pelo revisor.
- **Classificação:** especificação.

## E-09 · CT-03, CT-04 e CT-05 sem suas entradas exatas

- **Detecção:** ao marcar cada teste com o ID do CT correspondente (P-06).
- **Causa:** a suíte usava entradas parecidas (`" abc-1234 "`, `"abc1234"`), mas não as da tabela da spec.
  Como esses testes não citavam IDs, a lacuna não aparecia.
- **Correção:** as três entradas foram adicionadas a `test_placas_validas` (spec v2.0).
- **Prevenção:** cada linha parametrizada cita o ID que verifica.
- **Classificação:** implementação.

## E-10 · Marcações de bloco de código em `index.html`

- **Detecção:** leitura do arquivo na auditoria; depois confirmada pelo teste CT-44, que falhou.
- **Causa:** o arquivo começava com ` ```html ` e terminava com ` ``` `. Como o `<!DOCTYPE html>` não era o
  início do documento, o navegador podia renderizar a página em modo de compatibilidade. O teste anterior só
  procurava o texto `PlacaCheck` e não detectava o problema.
- **Correção:** marcações removidas; CT-44 exige que o documento comece por `<!DOCTYPE html>`.
- **Prevenção:** ler o diff completo de arquivos gerados com IA antes de aprovar o PR.
- **Classificação:** implementação.

## Lição do ciclo

Os erros E-01 a E-05 passaram por uma suíte 100% verde e só foram encontrados por **revisão
humana contra a spec**. É a evidência central do pilar "revisão humana obrigatória" do
[relatório técnico-ético](./relatorio-tecnico-etico.md).
