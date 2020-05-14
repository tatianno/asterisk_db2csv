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

exten_dict = exten.get_list()
calls = 'data;origem;destino;duracao;status;tipo;queue \n'

my_conn = mysql_conn()
fields = 'calldate, src, dst, channel, dstchannel, lastapp, billsec, disposition, accountcode'
query = "SELECT {} FROM cdr WHERE calldate like '{}%' and accountcode != ''".format(fields, data_query)
result = my_conn.query(query)

for (calldate, src, dst, channel, dstchannel, lastapp, billsec, disposition, accountcode) in result:
    
    data = calldate.strftime("%Y-%m-%d %H:%M:%S")
    origem = get_exten(channel)
    destino = get_exten(dstchannel)
    
    if origem in exten_dict:
        origem = exten_dict[origem]
    else:
        origem = src

    if destino in exten_dict:
        destino = exten_dict[destino]
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

filename = '{}arq-{}.csv'.format(path, data_query)
with open(filename, 'w') as arquivo:
    arquivo.write(calls)

    
