# Asterik DB para CSV
Script para consulta de chamadas no banco de dados no Asterisk e transformar em um arquivo csv
para a data selecionada

## Instalacao
Instalar pre requisitos
pip install -r requeriments.txt

Incluir script no cron para execução automatica
0 23 * * *root /usr/bin/python3 <path_script>/main.py

## Para obter dados de uma data especifica
python3 main.py '2020-02-03'

## Para obter dados de hoje
python3 main.py 