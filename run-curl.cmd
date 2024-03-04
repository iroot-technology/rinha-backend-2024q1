curl -X POST http://127.0.0.1:8000/clientes/2/transacoes -H 'Content-Type: application/json' -d '{"tipo": "d", "descricao": "teste", "valor": "1000"}'
curl -X POST http://127.0.0.1:8000/clientes/2/transacoes -H 'Content-Type: application/json' -d '{"tipo": "d", "descricao": "teste", "valor": "300"}'
curl -X POST http://127.0.0.1:8000/clientes/2/transacoes -H 'Content-Type: application/json' -d '{"tipo": "d", "descricao": "teste", "valor": "2300"}'
curl -X POST http://127.0.0.1:8000/clientes/2/transacoes -H 'Content-Type: application/json' -d '{"tipo": "c", "descricao": "teste", "valor": "100"}'

