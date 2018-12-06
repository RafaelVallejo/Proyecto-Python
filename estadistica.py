#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
from datetime import datetime

def obtener_estadistica(objeto, reporte, infoUser, infoScript):
	html = '''
<!DOCTYPE html>
<html>
	<head>
		<title>Estadistica</title>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<link rel="stylesheet" href="css/bootstrap.min.css">
		<link rel="stylesheet" href="estilos/estilos.css">
		<script src="js/jquery-3.3.1.min.js"></script>
		<script src="js/jquery/jquery-ui.js"></script>
 		<script src="js/bootstrap.min.js"></script>
	</head>
	<body>

		<div class="jumbotron">
			<h3 align="center">Estadisticas<br>Fecha y hora de ejecucion: %s<br>%s</h3>
		</div>

		<div class="container">

			<div class="row mb-2">
				<div class="col-md-12">

				<h3>Estadistica</h3>
				  <div class="form-group">
				    <label for="username"><b>Informacion general de la cuenta: </b></label>
				    <p>%s</p>
				  </div>
				  <div class="form-group">
				    <label for="username">Numero de Hashtags utilizados: </label>
				    <textarea type="text" class="form-control" id="Numero_hashtags_utilizados" name = "Numero_Hashtags_utilizados" readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="username">Hashtags utilizados: </label>
				    <textarea rows="4" type="text" class="form-control" id="Hashtags_utilizados" name = "Hashtags_utilizados" readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="Tweets_Day">Tweets por día de la semana: </label>
				    <textarea rows="7" type="text" class="form-control" id="Tweets_Day" name="Tweets_Day" readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="Tweets_hour">Hora de actividad: </label>
				   <textarea type="datetime" class="form-control" id="Tweets_Hour" name="Tweets_Hour"  readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="num_sites">Número de tweets a otros sitios:  </label>
				    <textarea type="text" class="form-control" id="num_sites" name="num_sites" readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="lista_sites">Enlaces a otros sitios de los Tweets del usuario:  </label>
				    <textarea rows="4" type="text" class="form-control" id="lista_sites" name="lista_sites" readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="tweets_geolocalizacion">Tweets geolocalizados:  </label>
				    <textarea type="text" class="form-control" id="tweets_geolocalizacion" name="tweets_geolocalizacion" readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="list_geolocalizados">Lista de los tweets geolocalizados:  </label>
				    <textarea rows="4" type="text" class="form-control" id="list_geolocalizados" name="list_geolocalizados" readonly  >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="dispositivo">Tweets con informacion del dispositivo: </label>
				    <textarea class="form-control" id="dispositivo" readonly >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="Tweets_generated">Tweets generados por otras cuentas:  </label>
				    <textarea type="text" class="form-control" id="tweets_generated" name="tweets_generated" readonly>%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="List_generated">Lista de los tweets generados por otras cuentas: </label>
				    <textarea rows="4" type="text" class="form-control" id="list_generated" name="list_generated" readonly="..">%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="mention_account">Cuentas que mencionan a la cuenta analizada:  </label>
				    <textarea type="text" class="form-control" id="mention_account" name="mention_account" readonly="..">%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="list_accounts">Lista de las cuentas que mencionan a la cuenta analizada:</label>
				    <textarea rows="4" type="text" class="form-control" id="list_accounts" name="list_accounts" readonly=".." >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="url">URL Analizados: </label>
				    <textarea rows="4" type="text" class="form-control" id="url" name="url" readonly=".."  >%s</textarea>
				  </div>
				  <div class="form-group">
				    <label for="multimedia">Contendio multimedia: </label>
				    <textarea rows="4" type="text" class="form-control" id="multimedia" name="multimedia" readonly=".." >%s</textarea>
				  </div>
				</div>
			</div>
		</div>
	</body>
</html>

''' % (ImprimirFechaHoraCreacion(),
	   infoScript,
	   str(infoUser),
	   objeto.number_used_hashtags,
	   listaToCadena(objeto.list_used_hashtags),
	   imprimeDicc(objeto.tweets_for_day),
	   objeto.hour_of_max_activity,
	   objeto.number_of_tweets_to_other_site,
	   listaToCadena(objeto.list_of_tweets_to_other_site),
	   objeto.tweets_geolocalizados,
	   listaToCadena(objeto.list_of_tweets_geolocalizados),
	   objeto.tweets_with_device_info,
	   #listaToCadena(objeto.list_of_tweets_device_info),
	   objeto.tweets_generated_other_accounts,
	   listaToCadena(objeto.list_tweets_generated_other_accounts),
	   objeto.tweets_mention_accout,
	   listaToCadena(objeto.list_tweets_mention_accout),
	   imprimeDicc(objeto.analized_tweets_url, False),
	   listaToCadena(objeto.content_multimedia_tweets_url)
	   )


	with open (reporte + '.html' , 'w') as resultados:
		resultados.write(html)

def listaToCadena(lista):
	cadena = "\n".join(lista)
	return cadena
def imprimeDicc(diccionario, ambos = True):
	cadena = ''
	if ambos:
		for key,value in diccionario.items():
			cadena += "%s: %s\n" % (key,value)
	else:
		for value in diccionario.itervalues():
			cadena += "%s\n" % (value)
	return cadena

def ImprimirFechaHoraCreacion():
	return datetime.now()
