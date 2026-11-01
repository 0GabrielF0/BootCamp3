# Roteiro de Demonstração

Percorre o fluxo completo da aplicação no ambiente padronizado. Também é possível usar a
documentação interativa em `http://127.0.0.1:8000/docs`.

## 1. Subir a API

```bash
docker compose up --build api
```

## 2. Interface web (RF-11, verificação manual)

Abra `http://127.0.0.1:8000/` no navegador e confira:

| Digite | Resultado esperado |
|---|---|
| `abc-1234` | Placa válida, `ABC1234`, padrão `antigo` |
| `abc1d23` | Placa válida, `ABC1D23`, padrão `mercosul` |
| `1234ABC` | Placa inválida, com a mensagem do motivo |

## 3. Saúde

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

## 4. Placas válidas (RN-01, RN-02, RN-03)

```bash
curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"ABC-1234"}'
# 200 {"valida":true,"placa_normalizada":"ABC1234","padrao":"antigo","motivo":null,...}

curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":" abc1d23 "}'
# 200 {"valida":true,"placa_normalizada":"ABC1D23","padrao":"mercosul","motivo":null,...}
```

## 5. Placas rejeitadas, com motivo

```bash
curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"ABC-12345"}'
# 200 {"valida":false,...,"motivo":"TAMANHO_INVALIDO",...}

curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"AB@1234"}'
# 200 {"valida":false,...,"motivo":"CARACTERE_INVALIDO",...}

curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"1234ABC"}'
# 200 {"valida":false,...,"motivo":"FORMATO_DESCONHECIDO",...}
```

## 6. Requisições inválidas (contrato HTTP)

```bash
curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"plaka":"ABC1234"}'
# 422 {"erro":{"codigo":"REQUISICAO_INVALIDA",...,"detalhes":[{"campo":"placa","problema":"Campo obrigatório ausente."}]}}

curl http://127.0.0.1:8000/validar
# 405 {"erro":{"codigo":"METODO_NAO_PERMITIDO",...}}
```

## 7. Rodar o harness

```bash
docker compose run --rm tests
# ... 61 passed
```
