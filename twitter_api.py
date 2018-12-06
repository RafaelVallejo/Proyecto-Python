#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

import json
import tweepy
import auth_credentials as cred
import optparse
import sys
from account_statistics import AccountStatistics, Tweet
import datetime
import json

def authenticate():
    """Función para autorizar acceso del script a la cuenta de Twitter
    Devuelve la sesión autorizada y disponible para usar la API de Twitter"""
    auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
    auth.set_access_token(cred.access_token, cred.access_token_secret)
    return tweepy.API(auth)

def addOptions():
    """Función que agrega opciones al script para su ejecución. Por defecto verbose es False"""
    parser = optparse.OptionParser(add_help_option = False)
    parser.add_option('-h', '--help', action='store_true', dest= 'help', default = False, help = 'Muestra las opciones disponibles.')
    parser.add_option('-c', '--usuario', dest= 'usuario', default = None, help = 'Cuenta de usuario a analizar.')
    parser.add_option('-v', '--verboso', action='store_true', dest = 'verboso', default = False, help = 'Muestra los pasos que se realizan.')
    parser.add_option('-o', '--reporte', dest= 'reporte', default = None, help = 'Indica el nombre del archivo dónde se escribirá el reporte.')
    parser.add_option('-n', '--tweets', dest = 'tweets', type = 'int', default = 1, help = 'Indica el número de tweets a analizar de 1 a 3000.')
    opts,args = parser.parse_args()
    return opts

def createVerbose(verbose, string):
    if verbose:
        print string

def printError(msg, exit = False):
    """Función que imprime mensaje de error y sale del programa
        Recibe: mensaje a mostrar y booleano que indica si se debe terminar la ejecución del programa"""
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def checkOptions(options):
    """Función que verifica el estado de ciertas de opciones para poder ejecutar el script"""
    if options.help is False:
        if options.usuario is None:
            printError('Debes especificar el usuario a analizar.', True)
    if int(options.tweets) > 3000:
        printError('El número supera el límite de 3000 tweets.', True)

def muestraAyuda():
    print 'Uso: %s [opciones]' % (sys.argv[0])
    print 'Opciones: \n\
    -h, --help      Muestra el mensaje de ayuda y las opciones disponibles.\n\
    -c, --usuario   Cuenta de usuario a analizar.\n\
    -v, --verboso   Muestra los pasos que se realizan.\n\
    -o, --reporte   Indica el nombre del archivo dónde se escribirá el reporte.\n\
    -n', '--tweets  Indica el número de tweets a analizar de 1 a 3000.'

def infoUsuario(api, usuario, verbose):
    createVerbose(verbose, "Analizando usuario")
    """Función que obtiene la información del usuario a analizar mediante la bandera -c usuario
    Recibe: api y usuario a analizar"""
    user = api.get_user(usuario)
    print 'Nombre: ' + user.name
    print'Nombre de usuario: @' + user.screen_name
    print 'Imagen de perfil: %s' % (user.profile_image_url)
    print 'Fecha de creación de la cuenta: %s' % (user.created_at.strftime("%d/%m/%Y"))
    print 'Número de tweets: %s' % (user.statuses_count)
    print 'Número de tweets agregados a favoritos: %s' % (user.favourites_count)

def hashtagsUtilizados(statistic_object, tweet, verbose):
    createVerbose(verbose, "Buscando hashtags utilizados")
    """Función que busca los hashtags utilizados en cada tweet y los va agregando a la lista de hashtags
    Recibe: lista y tweet a analizar"""
    for hashtag in tweet.entities.get('hashtags'):
        ht = '#' + hashtag['text'].encode('utf8')
        if ht not in statistic_object.list_used_hashtags:
            statistic_object.list_used_hashtags.append(ht)

def tweetsLinksToOtherSite(statistics_object, tweet, verbose):
    createVerbose(verbose, "Buscando enlaces a otros sitios")
    """Función que busca en cada tweet los enlaces a otros sitos y los agrega a la lista de tweets a otros sitios
    Recibe: lista y tweet a analizar"""
    for linkToOther in tweet.entities.get('urls'):
        statistics_object.list_of_tweets_to_other_site.append(linkToOther['expanded_url'].encode('utf8'))

def tweetsPerDay(dias, tweet, verbose):
    createVerbose(verbose, "Calculando los tweets por día")
    """Función que va incrementando el número de tweets que se hacen por cierto día de acuerdo al tweet que se analice
    Recibe: lista con un contador por cada uno de los días de la semana y el tweet a analizar"""
    dia = tweet.created_at.strftime("%A")
    if dia == 'Monday': dias[0] += 1
    elif dia == 'Tuesday': dias[1] += 1
    if dia == 'Wednesday': dias[2] += 1
    elif dia == 'Thursday': dias[3] += 1
    if dia == 'Friday': dias[4] += 1
    elif dia == 'Saturday': dias[5] += 1
    elif dia == 'Sunday': dias[6] += 1

def llenaDiccionarioTweetsDias(dic_tweets_dias, dias):
    """Función para llenar el diccionario que indica el número de tweets que se realizaron por cada día de la semana, de acuerdo a los tweets analizados en total
    Recibe: diccionario y lista con los contadores de los tweets por día"""
    dic_tweets_dias['Lunes'] = dias[0]
    dic_tweets_dias['Martes'] = dias[1]
    dic_tweets_dias['Miércoles'] = dias[2]
    dic_tweets_dias['Jueves'] = dias[3]
    dic_tweets_dias['Viernes'] = dias[4]
    dic_tweets_dias['Sábado'] = dias[5]
    dic_tweets_dias['Domingo'] = dias[6]

def linksToMultiMedia(statistics_object, tweet, verbose):
    createVerbose(verbose, "Buscando enlaces directos al contenido multimedia")
    """Función que busca los enlaces directos al contenido multimedia por el usuario y los almacena en la lista que contiene estos enlaces, tanto de fotos como videos
    Recibe: lista donde se almacenan los enlaces y el tweet a anlizar"""
    if 'media' in tweet.entities:
        for linkToMutimedia in tweet.extended_entities.get('media'):
            if linkToMutimedia['type'] == 'video':
                enlace = linkToMutimedia['video_info']['variants'][0]['url'].encode('utf8')
            else:
                enlace = linkToMutimedia['media_url'].encode('utf8')
            statistics_object.content_multimedia_tweets_url.append(enlace)

def fillInfoNumbers(statistics_object):
    statistics_object.tweets_mention_accout = len(statistics_object.list_tweets_mention_accout)
    statistics_object.number_of_tweets_to_other_site = len(statistics_object.list_of_tweets_to_other_site)
    statistics_object.number_used_hashtags = len(statistics_object.list_used_hashtags)


def getAllTweets(account_name, number_of_tweets, api, verbose):
    createVerbose(verbose, "Obteniendo tweets")
    """Función para obtener los n tweets que se manden en la bandera -n, por defecto será uno. Los tweets solicitados serán almacenados y devueltos en una lista.
    Recibe: api, usuario y número de tweets a obtener. Devuelve: lista con todos los tweets solicitados"""
    return [tweet for tweet in tweepy.Cursor(api.user_timeline,id=account_name).items(number_of_tweets)]

def getAllTweetsMentions(api, account_name, number_of_tweets,verbose):
    createVerbose(verbose, "Calculando menciones del usuario")
    """Función para obtener los n tweets donde se haga mención del usuario analizados, por defecto será uno. Los tweets encontrados serán almacenados y devueltos en una lista.
    Recibe: api, usuario y número de tweets a buscar. Devuelve: lista con todos los tweets donde se mencione al usuario"""
    return [tweet for tweet in tweepy.Cursor(api.search,q='@%s -RT' % account_name).items(number_of_tweets) ]

def dumpTweetToJson(tweet):
    return json.loads(json.dumps(tweet._json))

def getTweetId(tweet):
    return tweet.id_str.encode('utf8')

def getTweetDate(tweet):
    return str(tweet.created_at)

def getTweetFragment(tweet):
    return tweet.text.encode('utf8')[:31]


def urlForTweet(statistic_object, tweet, verbose):
    createVerbose(verbose, "Obteniendo la url")
    tweet_id = getTweetId(tweet)
    screen_name = tweet.author.screen_name.encode('utf8')
    url = 'https://twitter.com/%s/status/%s'%(screen_name,tweet_id)
    statistic_object.analized_tweets_url[tweet_id] = Tweet(getTweetDate(tweet), getTweetFragment(tweet), url)
    return True

def tweetToOtherAccounts(statistic_object, tweet, verbose):
    createVerbose(verbose, "Obteniendo tweets generados a otras cuentas")
    texto = tweet.text.encode('utf-8')
    screen_name = tweet.author.screen_name.encode('utf8')
    if texto.startswith("RT @"):
        return False
    mentions = tweet.entities.get('user_mentions')
    if not not mentions:
        statistic_object.tweets_generated_other_accounts += 1
        statistic_object.list_tweets_generated_other_accounts.append(getTweetId(tweet))
    return True


def tweetDevice(statistic_object, tweet, verbose):
    createVerbose(verbose, "Obteniendo información de los dispostivos que han ocupado esta cuenta")
    tweet_id = getTweetId(tweet)
    j = dumpTweetToJson(tweet)['source'].lower()
    if 'iphone' in j:
        statistic_object.tweets_with_device_info += 1
        statistic_object.list_of_tweets_device_info.append((tweet_id, 'iphone'))
        return 'iphone'
    elif 'android' in j:
        statistic_object.tweets_with_device_info += 1
        statistic_object.list_of_tweets_device_info.append((tweet_id,'android'))
        return 'android'
    elif 'web' in j:
        statistic_object.tweets_with_device_info += 1
        statistic_object.list_of_tweets_device_info.append((tweet_id,'web'))
        return 'web'
    elif 'windows' in j:
        statistic_object.tweets_with_device_info += 1
        statistic_object.list_of_tweets_device_info.append((tweet_id,'windows'))
        return 'windows'
    return ''

def getActivityByHour(statistic_object, tweet, verbose):
    createVerbose(verbose, "Obteniendo la actividad por hora")
    date = getTweetDate(tweet).split(' ')[1].split(':')[0]
    statistic_object.activity_by_hour[int(date)] += 1
    return True

def getHourOfActivity(statistic_object, verbose):
    createVerbose(verbose, "Obteniendo la hora con mayor actividad")
    mayor = max(statistic_object.activity_by_hour)
    size  = len(statistic_object.activity_by_hour)
    s = 0
    for i in range(size):
        if mayor == statistic_object.activity_by_hour[i]:
            statistic_object.hour_of_max_activity += '%s:00:00 - %s:59:59'%(i,i) if s == 0 else '  and  %s:00:00 - %s:59:59'%(i,i)
            s += 1
    return statistic_object.hour_of_max_activity

def tweetGeolocalization(statistic_object, tweet, verbose):
    try:
        createVerbose(verbose, "Obteniendo la localización")
        j = dumpTweetToJson(tweet)
        if not j['geo']:
            #print 'No se puede obtener la geolocalizacion'
            return False
        statistics_object.tweets_geolocalizados += 1
        statistics_object.list_of_tweets_geolocalizados.append((getTweetId(tweet),tupe(j['coordinates'])))
    except Exception as e:
        return False
    return True

def startAnalisys():

    opts = addOptions()
    checkOptions(opts)
    account_analisys = AccountStatistics()
    api = authenticate()
    verbose = opts.verboso
    if opts.help:
        muestraAyuda()
        printError('',True)
    tweets = getAllTweets(opts.usuario, opts.tweets, api, verbose)
    dias = [0, 0, 0, 0, 0, 0, 0]
    infoUsuario(api,opts.usuario, verbose)
    #print len(tweets)
    #raw_input()
    createVerbose(verbose, "Empezando a hacer el análisis")
    for tweet in tweets:
        urlForTweet(account_analisys, tweet, verbose)
        tweetToOtherAccounts(account_analisys,tweet, verbose)
        tweetDevice(account_analisys, tweet, verbose)
        tweetGeolocalization(account_analisys, tweet, verbose)
        getActivityByHour(account_analisys, tweet, verbose)
        hashtagsUtilizados(account_analisys, tweet, verbose)
        tweetsLinksToOtherSite(account_analisys, tweet, verbose)
        linksToMultiMedia(account_analisys, tweet, verbose)
        tweetsPerDay(dias, tweet, verbose)

    for tweet in getAllTweetsMentions(api, opts.usuario, opts.tweets, verbose):  # Checar limite de 100
        account_analisys.list_tweets_mention_accout.append('@'+tweet.author.screen_name.encode('utf8'))
        
    getHourOfActivity(account_analisys, verbose)
    llenaDiccionarioTweetsDias(account_analisys.tweets_for_day, dias)
    fillInfoNumbers(account_analisys)

if __name__ == '__main__':
    try:
        startAnalisys()
    except tweepy.TweepError as e:
        printError('Usuario no encontrado',True)
