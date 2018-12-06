#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

import json
import tweepy
import auth_credentials as cred
import optparse
import sys
from acount_statistics import AccountStatistics, Tweet
def authenticate():
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
    opts,args = parser.parse_args()
    return opts

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


def muestraAyuda():
    print 'Uso: %s [opciones]' % (sys.argv[0])
    print 'Opciones: \n\
    -h, --help      Muestra el mensaje de ayuda y las opciones disponibles.\n\
    -c, --usuario   Cuenta de usuario a analizar.\n\
    -v, --verboso   Muestra los pasos que se realizan.\n\
    -o, --reporte   Indica el nombre del archivo dónde se escribirá el reporte.'

def infoUsuario(api, usuario):
    user = api.get_user(usuario)
    print 'Nombre: ' + user.name
    print'Nombre de usuario: @' + user.screen_name
    print 'Imagen de perfil: %s' % (user.profile_image_url)
    print 'Fecha de creación de la cuenta: %s' % (user.created_at)
    print 'Número de tweets: %s' % (user.statuses_count)
    print 'Número de tweets agregados a favoritos: %s' % (user.favourites_count)

def hashtagsUtilizados(api, usuario):
    public_tweets = getAllTweets(usuario)
    lista_hashtags = []
    for tweet in public_tweets:
        for hashtag in tweet.entities.get('hashtags'):
            lista_hashtags.append('#' + hashtag['text'].encode('utf8'))
    lista_hashtags = list(set(lista_hashtags))
    return lista_hashtags

def getAllTweets(account_name, number_of_tweets, api):
    try:
        return [tweet for tweet in tweepy.Cursor(api.user_timeline,id=account_name).items(number_of_tweets)]
    except tweepy.TweepError as e:
        printError('Usuario no encontrado',True)

def dumpTweetToJson(tweet):
    return json.loads(json.dumps(tweet._json))

def getTweetId(tweet):
    return tweet.id_str.encode('utf8')

def getTweetDate(tweet):
    return str(tweet.created_at)

def getTweetFragment(tweet):
    return tweet.text.encode('utf8')[:31]


def urlForTweet(statistic_object, tweet):
    tweet_id = getTweetId(tweet)
    screen_name = tweet.author.screen_name.encode('utf8')
    url = 'https://twitter.com/%s/status/%s'%(screen_name,tweet_id)
    statistic_object.analized_tweets_url[tweet_id] = Tweet(getTweetDate(tweet), getTweetFragment(tweet), url)
    return True

def tweetToOtherAccounts(statistic_object, tweet):
    texto = tweet.text.encode('utf-8')
    screen_name = tweet.author.screen_name.encode('utf8')
    if texto.startswith("RT @"):
        return False
    mentions = tweet.entities.get('user_mentions')
    if not not mentions:
        statistic_object.tweets_generated_other_accounts += 1
        statistic_object.list_tweets_generated_other_accounts.append(getTweetId(tweet))
    return True


def tweetDevice(statistic_object, tweet):
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

def getActivityByHour(statistic_object, tweet):
    date = getTweetDate(tweet).split(' ')[1].split(':')[0]
    statistic_object.activity_by_hour[int(date)] += 1
    return True

def getHourOfActivity(statistic_object):
    mayor = max(statistic_object.activity_by_hour)
    size  = len(statistic_object.activity_by_hour)
    s = 0
    for i in range(size):
        if mayor == statistic_object.activity_by_hour[i]:
            statistic_object.hour_of_max_activity += '%s:00:00 - %s:59:59'%(i,i) if s == 0 else '  and  %s:00:00 - %s:59:59'%(i,i)
            s += 1
    return statistic_object.hour_of_max_activity

def tweetGeolocalization(statistic_object, tweet):
    try:

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
    if opts.help:
        muestraAyuda()
        printError('',True)
    tweets = getAllTweets(opts.usuario, 20, api)

    #print len(tweets)
    #raw_input()
    for tweet in tweets:
        urlForTweet(account_analisys, tweet)
        tweetToOtherAccounts(account_analisys,tweet)
        tweetDevice(account_analisys, tweet)
        tweetGeolocalization(account_analisys, tweet)
        getActivityByHour(account_analisys, tweet)
    
    """for k,v in account_analisys.analized_tweets_url.items():
        print '%s   %s'%(k,v)


    print '\n\n****************************************************'
    for tw in account_analisys.list_tweets_generated_other_accounts:
        print account_analisys.analized_tweets_url[tw]
    print account_analisys.tweets_generated_other_accounts
    print len(account_analisys.list_tweets_generated_other_accounts)
    print '\n\n****************************************************'
    print account_analisys.tweets_with_device_info
    print len(account_analisys.list_of_tweets_device_info)
    for e in account_analisys.list_of_tweets_device_info:
        print e[1]
    print '\n\n****************************************************'"""
    getHourOfActivity(account_analisys)
        
 
if __name__ == '__main__':
    startAnalisys()
    
