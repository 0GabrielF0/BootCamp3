# Roteiro de Demonstração

Percorre o fluxo completo da API no ambiente padronizado. As respostas abaixo foram obtidas
em 2026-10-25. Também é possível usar a interface interativa em
`http://127.0.0.1:8000/docs`.

## 1. Subir a API

```bash
docker compose up --build api
```

## 2. Status e saúde

```bash
curl http://127.0.0.1:8000/
# {"projeto":"Validador de Placas Brasileiras","status":"operacional","documentacao":"/docs"}

curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

## 3. Placas válidas (RN-01, RN-02, RN-03)

```bash
curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"ABC-1234"}'
# 200 {"valida":true,"placa_normalizada":"ABC1234","padrao":"antigo","motivo":null,...}

curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":" abc1d23 "}'
# 200 {"valida":true,"placa_normalizada":"ABC1D23","padrao":"mercosul","motivo":null,...}
```

## 4. Placas rejeitadas, com motivo

```bash
curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"ABC-12345"}'
# 200 {"valida":false,...,"motivo":"TAMANHO_INVALIDO",...}

curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"AB@1234"}'
# 200 {"valida":false,...,"motivo":"CARACTERE_INVALIDO",...}

curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"placa":"1234ABC"}'
# 200 {"valida":false,...,"motivo":"FORMATO_DESCONHECIDO",...}
```

## 5. Requisições inválidas (contrato HTTP)

```bash
curl -X POST http://127.0.0.1:8000/validar -H "Content-Type: application/json" -d '{"plaka":"ABC1234"}'
# 422 {"erro":{"codigo":"REQUISICAO_INVALIDA",...,"detalhes":[{"campo":"placa","problema":"Campo obrigatório ausente."}]}}

curl http://127.0.0.1:8000/validar
# 405 {"erro":{"codigo":"METODO_NAO_PERMITIDO",...}}
```

## 6. Rodar o harness

```bash
docker compose run --rm tests
# ... 50 passed — log completo em logs_testes_final.txt
```
