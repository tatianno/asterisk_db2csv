<?php
#Dados de autenticacao
require_once('config.php');


if (!isset($_SERVER['PHP_AUTH_USER'])) {
    header('WWW-Authenticate: Basic realm="My Realm"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Falha na autenticacao';
    exit;
} else {
	if ($autenticacao['username'] == $_SERVER['PHP_AUTH_USER'] and $autenticacao['password'] == $_SERVER['PHP_AUTH_PW']){
		if (isset($_GET['date'])){
			$file = 'arq-'.$_GET['date'].'.csv';
			$file_arq = "$dir_csv/$file";
			if (file_exists($file_arq)){
				header('Content-Description: File Transfer');
				header('Content-Type: application/csv');
				header('Content-Disposition: attachment; filename='.basename($file));
				header('Content-Transfer-Encoding: binary');
				header('Expires: 0');
				header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
				header('Pragma: public');
				header('Content-Length: ' . filesize($file_arq));
				ob_clean();
				flush();
				readfile($file_arq);
			} else {
				header('HTTP/1.0 404 Not Found');
				echo('Arquivo nao encontrado');
			}
		} else {
			header('HTTP/1.0 401 Bad Request');
			echo('Arquivo nao informado');
		}
	} else {
		header('HTTP/1.0 401 Unauthorized');
		echo "Falha na autenticacao";
	}
	
}
?>
