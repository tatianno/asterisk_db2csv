#!/bin/bash

#Script para instalacao de automatizacao de relatorios
DIR=$(pwd)
DIR_WWW='/var/www'

#Criando diretorios para guardar o csv
mkdir $DIR/csv
mkdir $DIR/csv/total

#Criando link de acesso aos arquivos gerados
ln -s $DIR/php/ $DIR_WWW/asterisk_db2csv

#Configuracoes iniciais
echo "<?php

\$autenticacao = array(
        'username' => 'gnew',
        'password' => 'mmlp@2020'
);

\$dir_csv = '$DIR/csv';" > $DIR/php/config.php
