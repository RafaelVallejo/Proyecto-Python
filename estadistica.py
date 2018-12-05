def obtenerEstadistica(objeto):
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
			<h3 align="center">Estadistica</h3>
		</div>

		<div class="container">

			<div class="row mb-2">
				<div class="col-md-4">

				<h3>Estadistica</h3>
				  <div class="form-group">
				    <label for="username">Hashtags utilizados: </label>
				    <input type="text" class="form-control" id="Hashtags_utilizados" name = "Hashtags_utilizados" readonly placeholder = %s>
				  </div>	
				  <div class="form-group">
				    <label for="Tweets_Day">Tweets por día de la semana: </label>
				    <input type="text" class="form-control" id="Tweets_Day" name="Tweets_Day" readonly placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="Tweets_hour">Hora de actividad: </label>
				    <input type="datetime" class="form-control" id="Tweets_Hour" name="Tweets_Hour"  readonly placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="num_sites">Número de tweets a otros sitios:  </label>
				    <input type="text" class="form-control" id="num_sites" name="num_sites" readonly placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="lista_sites">Tweets por día de la semana:  </label>
				    <input type="text" class="form-control" id="lista_sites" name="lista_sites" readonly placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="tweets_geolocalizacion">Tweets geolocalizados:  </label>
				    <input type="text" class="form-control" id="tweets_geolocalizacion" name="tweets_geolocalizacion" readonly placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="list_geolocalizados">Lista de los tweets geolocalizados:  </label>
				    <input type="text" class="form-control" id="list_geolocalizados" name="list_geolocalizados" readonly placeholder = %s >
				  </div>
				  <div class="form-group">
				    <label for="dispositivo">Tweets con informacion del dispositivo: </label>
				    <textarea class="form-control" id="dispositivo" readonly placeholder = %s></textarea>
				  </div>
				  <div class="form-group">
				    <label for="Tweets_generated">Tweets generados por otras cuentas:  </label>
				    <input type="text" class="form-control" id="tweets_generated" name="tweets_generated" readonly placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="List_generated">Lista de los tweets generados por otras cuentas: </label>
				    <input type="text" class="form-control" id="list_generated" name="list_generated" readonly=".." placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="mention_account">Cuentas mencionadas:  </label>
				    <input type="text" class="form-control" id="mention_account" name="mention_account" readonly=".." placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="list_accounts">Lista de las cuentas mencionadas </label>
				    <input type="text" class="form-control" id="list_accounts" name="list_accounts" readonly=".." placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="url">URL Analizados: </label>
				    <input type="text" class="form-control" id="url" name="url" readonly=".." placeholder = %s>
				  </div>
				  <div class="form-group">
				    <label for="multimedia">Contendio multimedia: </label>
				    <input type="text" class="form-control" id="multimedia" name="multimedia" readonly=".." placeholder = %s>
				  </div>
				</div>
			</div>	
		</div>
	</body>
</html>

''' % (objeto.used_hashtags, 
	   objeto.tweets_for_day,
	   objeto.hour_of_max_activity, 
	   objeto.number_of_tweets_to_other_site, 
	   objeto.list_of_tweets_to_other_site,
	   objeto.tweets_geolocalizados, 
	   objeto.list_of_tweets_geolocalizados,
	   objeto.tweets_with_device_info,
	   objeto.list_of_tweets_device_info,
	   objeto.tweets_generated_other_accounts 
	   objeto.list_tweets_generated_other_accounts,
	   objeto.tweets_mention_accout, 
	   objeto.list_tweets_mention_accout,
	   objeto.analized_tweets_url,
	   objeto.content_multimedia_tweets_url
	   )

		
	with open ("resultados_generados.html" , 'w') as resultados: 
		resultados.write(html)



