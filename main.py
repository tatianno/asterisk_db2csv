from db import mysql_conn
from functions import exten
from settings import path
from datetime import datetime
import sys

def get_exten(channel):
    data = channel.split('/')
    tech = None
    exten= None

    if len(data) > 1:
        tech = data[0]
        exten = data[1].split('-')
        if len(exten) > 1:
            exten = exten[0]
    
    return exten

if len(sys.argv) > 1:
    data_query = sys.argv[1]
else:
    data_query = datetime.now().strftime('%Y-%m-%d')

entrantes_tipo = [
    'INT',
    'ENT'
]

exten_dict = exten.get_list()
calls = 'data;origem;destino;duracao;status;tipo;queue \n'
resumo_calls = 'Representante;Sainte Total;Não Atendidas;Ativos;(-)1 Min.;Entrante Total;Ocupado;Não Atendidas;Receptivas;(-)1 Min.;Tot. Contatos;Perdidas;% Perdidas \n'

my_conn = mysql_conn()
fields = 'calldate, src, dst, channel, dstchannel, lastapp, billsec, disposition, accountcode'
query = "SELECT {} FROM cdr WHERE calldate like '{}%' and accountcode != ''".format(fields, data_query)
result = my_conn.query(query)

consolidado = {}
total = {
    'sainte_total': 0,
    'sainte_nao_atendidas': 0,
    'sainte_ocupado': 0,
    'ativos': 0,
    'sainte_menos_1_min': 0,
    'entrante_total': 0,
    'entrante_ocupado': 0,
    'entrante_nao_atendidas': 0,
    'receptivos': 0,
    'entrante_menos_1_min': 0,
}

for username in exten_dict:
    extensao = exten_dict[username]
    consolidado[extensao] = {
        'sainte_total': 0,
        'sainte_nao_atendidas': 0,
        'sainte_ocupado': 0,
        'ativos': 0,
        'sainte_menos_1_min': 0,
        'entrante_total': 0,
        'entrante_ocupado': 0,
        'entrante_nao_atendidas': 0,
        'receptivos': 0,
        'entrante_menos_1_min': 0,
    }

for (calldate, src, dst, channel, dstchannel, lastapp, billsec, disposition, accountcode) in result:
    
    data = calldate.strftime("%Y-%m-%d %H:%M:%S")
    origem = get_exten(channel)
    destino = get_exten(dstchannel)
    
    #Chamadas ORIGEM
    if origem in exten_dict:
        origem = exten_dict[origem]
        
        #Contabilizando SAINTES
        if accountcode not in entrantes_tipo:
            consolidado[origem]['sainte_total'] += 1

            #Calculando duracao
            try:
                duracao = int(billsec)
            except:
                duracao = 0

            if duracao >= 60:
                consolidado[origem]['ativos'] += 1
            
            else:
                if disposition == 'NO ANSWER':
                    consolidado[origem]['sainte_nao_atendidas'] += 1
            
                elif disposition == 'BUSY':
                    consolidado[origem]['sainte_ocupado'] += 1
                
                else:
                    consolidado[origem]['sainte_menos_1_min'] += 1
        
    else:
        origem = src

    #CHAMADAS DESTINO
    if destino in exten_dict:
        destino = exten_dict[destino]

        #Contabilizando ENTRANTES
        if accountcode in entrantes_tipo:
            consolidado[destino]['entrante_total'] += 1

            #Calculando duracao
            try:
                duracao = int(billsec)
            except:
                duracao = 0

            if duracao >= 60:
                consolidado[destino]['receptivos'] += 1

            else:
                if disposition == 'NO ANSWER':
                    consolidado[destino]['entrante_nao_atendidas'] += 1
            
                elif disposition == 'BUSY':
                    consolidado[destino]['entrante_ocupado'] += 1
                    
                else:
                    consolidado[destino]['entrante_menos_1_min'] += 1

    else:
        destino = dst

    if lastapp == 'Queue':
        queue = dst
    else:
        queue = '-'

    calls += '{};{};{};{};{};{};{} \n'.format(
        data, 
        origem, 
        destino, 
        billsec, 
        disposition, 
        accountcode, 
        queue
    )

my_conn.disconnect()

#Criando arquivo consolidado
#Representante;Sainte Total;Não Atendidas;Ativos;(-)1 Min.;Entrante Total;Ocupado;Não Atendidas;Receptivas;(-)1 Min.;Tot. Contatos;Perdidas;% Perdidas
for extensao in consolidado:
    total_contatos = consolidado[extensao]['sainte_total'] + consolidado[extensao]['entrante_total']
    perdidas = consolidado[extensao]['sainte_nao_atendidas'] + consolidado[extensao]['entrante_nao_atendidas'] + consolidado[extensao]['entrante_ocupado']
    perdidas = perdidas + consolidado[extensao]['sainte_menos_1_min'] + consolidado[extensao]['entrante_menos_1_min']
    
    if total_contatos != 0:
        perdidas_porcentagem = round((perdidas*100)/total_contatos)
    else:
        perdidas_porcentagem = 0
    
    if total_contatos != 0:
        resumo_calls += '{};{};{};{};{};{};{};{};{};{};{};{};{} \n'.format(
            extensao,
            consolidado[extensao]['sainte_total'],
            consolidado[extensao]['sainte_nao_atendidas'],
            consolidado[extensao]['ativos'],
            consolidado[extensao]['sainte_menos_1_min'],
            consolidado[extensao]['entrante_total'],
            consolidado[extensao]['entrante_ocupado'],
            consolidado[extensao]['entrante_nao_atendidas'],
            consolidado[extensao]['receptivos'],
            consolidado[extensao]['entrante_menos_1_min'],
            total_contatos,
            perdidas,
            perdidas_porcentagem        
        )

filename = '{}total/arq-{}.csv'.format(path, data_query)
with open(filename, 'w') as arquivo:
    arquivo.write(calls)

filename = '{}arq-{}.csv'.format(path, data_query)
with open(filename, 'w') as arquivo:
    arquivo.write(resumo_calls)
    
