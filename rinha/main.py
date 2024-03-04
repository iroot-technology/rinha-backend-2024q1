from typing import Union
from connect import connect
from fastapi import FastAPI, HTTPException, Depends, Response
from model import Transacoes
import psycopg2

app = FastAPI()

@app.post("/clientes/{id}/transacoes")
async def criar_transacao(id: int, transacao: Transacoes):
    #import pdb; pdb.set_trace
    if transacao.tipo == 'd':
        transacao.valor = abs(transacao.valor) * -1
    stmt = """
        with cte_i as (
            insert into transacoes (clientes_id, data, tipo, descricao, valor)
                 values ({},now(),'{}','{}',{}) 
              returning clientes_id, tipo, valor
        ), cte_u as (
            update clientes 
               set saldo = saldo + cte_i.valor 
              from cte_i 
             where clientes.id = cte_i.clientes_id 
         /*returning clientes.limite, (clientes.limite + clientes.saldo) saldo*/
         returning clientes.limite, clientes.saldo
        ) 
        select row_to_json(cte_u)
          from cte_u
    """.format(id, transacao.tipo, transacao.descricao, transacao.valor)
    pconn = connect()
    try:
        with pconn.cursor() as cursor:
            cursor.execute(stmt)
            cur = cursor.fetchone()
            pconn.commit()
    except psycopg2.errors.lookup("23505") as Error:
        # 23505 CheckViolation Unique
        det = '[ERROR]: Violacao de integridade para o Cliente {} .'.format(id)
        raise HTTPException(status_code=422, detail=det)
    except psycopg2.errors.lookup("23514") as Error:
        # 23514 CheckViolation IntegrityError
        det = '[ERROR]: Violacao de integridade para o Cliente {} .'.format(id)
        raise HTTPException(status_code=422, detail=det)
    except psycopg2.errors.lookup("23503") as Error:
        # 23503 ForeignKeyViolation IntegrityError
        det = '[ERROR]: Cliente {} inexistente.'.format(id)
        raise HTTPException(status_code=404, detail=det)
    finally:
        pconn.close()
    return cur[0]


@app.get("/clientes/{id}/extrato")
def gerar_extrato(id: int):

    stmt = """
        select 
            format('{{"saldo": {{"total": %s, "data_extrato": "%s", "limite": %s }}, "ultimas_transacoes": [ %s ]}}', 
              --(case when saldo=0 then saldo else (limite + saldo) end), 
              saldo, 
              now(), 
              limite, 
              array_to_string(array_agg(row_to_json(t)), ',')
            )::jsonb
          from clientes c 
          left join lateral (
             select abs(valor) AS valor, tipo, descricao, data AS realizada_em 
               from transacoes t 
              where t.clientes_id = c.id
              union all select 0 as valor, 'c' as tipo, 'inicio' as descricao, '1970-01-01 00:00:00-03' as realizada_em
              order by 4 desc 
              limit 2
          ) t on true 
         where id = {}
         group by limite, saldo
    """.format(id)
    pconn = connect()
    try:
        with pconn.cursor() as cursor:
            cursor.execute(stmt)
            cur = cursor.fetchone()
            pconn.close()
            if cur is None:
                raise TypeError
    except Exception as error:
        raise HTTPException(status_code=404, detail='Extrato inexistente.')
    return cur[0]
