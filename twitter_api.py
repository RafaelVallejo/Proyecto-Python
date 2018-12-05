#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

import tweepy
import auth_credentials as cred
import optparse
import sys
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


def infoCuenta(api):
    me = api.me()
    print 'Nombre: ' + me.name
    print'Nombre de usuario: @' + me.screen_name
    print 'Imagen de perfil: %s' % (me.profile_image_url)
    print 'Fecha de creación de la cuenta: %s' % (me.created_at)
    print 'Número de tweets: %s' % (me.statuses_count)
    print 'Número de tweets agregados a favoritos: %s' % (me.favourites_count)
def infoUsuario(api, usuario):
    user = api.get_user(usuario)
    print 'Nombre: ' + user.name
    print'Nombre de usuario: @' + user.screen_name
    print 'Imagen de perfil: %s' % (user.profile_image_url)
    print 'Fecha de creación de la cuenta: %s' % (user.created_at)
    print 'Número de tweets: %s' % (user.statuses_count)
    print 'Número de tweets agregados a favoritos: %s' % (user.favourites_count)


def getAllTweets(account_name):
    return [tweet for tweet in tweepy.Cursor(api.user_timeline,id=account_name).items()]

def dumpTweetToJson(tweet):
    return json.dumps(tweet._json)

def printTweetInfo(tweet):
    print "Name:", tweet.author.name.encode('utf8')
    print "Screen-name:", tweet.author.screen_name.encode('utf8')
    print "Tweet created:", tweet.created_at
    print "Tweet:", tweet.text.encode('utf8')
    print "Retweeted:", tweet.retweeted
    print "Favourited:", tweet.favorited
    print "Location:", tweet.user.location.encode('utf8')
    print "Time-zone:", tweet.user.time_zone
    print "Geo:", tweet.geo
    print "//////////////////"

if __name__ == '__main__':
    opts = addOptions()
    checkOptions(opts)
    api = authenticate()
    #infoCuenta(api)
    if opts.help:
        muestraAyuda()
    else:
        infoUsuario(api,opts.usuario)
        public_tweets = api.user_timeline(id=opts.usuario,count=10)
        for tweet in public_tweets:
            for hashtag in tweet.entities.get('hashtags'):
                print '#%s' % (hashtag['text'])
