# coding: utf-8
# author: ura1020

# できるだけプリミティブでシンプルなOAuth認証処理2020年版

from __init__ import *
import logging
logging.basicConfig(level=logging.DEBUG)

selected = input('Please select your auth site\n1 google\n2 twitter\n3 facebook\n4 instagram\n5 yahoo japan\n\n')

if selected in ['1', 'google','g']:
  logging.info('Authorization at google')
  logging.info('-- reference')
  logging.info('https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps?hl=ja\n')

  CLIENT_ID = input('CLIENT_ID: ')
  CLIENT_SECRET = input('CLIENT_SECRET: ')
  CALLBACK_URL = input('CALLBACK_URL: ')

  url = google_code(client_id=CLIENT_ID,redirect_uri=CALLBACK_URL)
  logging.info("Please go here and authorize, %s" % url)

  response_url = input('Paste the full redirect URL here: ')
  code = response_param(response_url,'code')
  logging.debug("code = %s" % code)

  response = google_access_token(code=code, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, uri=CALLBACK_URL)
  response = google_user_id(access_token=response['access_token'])
  logging.info("Your google's user_id is '%s'" % response['id'])

if selected in ['2','twitter','tw','t']:
  logging.info('Authorization at twitter')
  logging.info('-- reference')
  logging.info('https://developer.twitter.com/ja/docs/basics/authentication/overview\n')

  API_KEY = input('API_KEY: ')
  API_SECRET_KEY = input('API_SECRET_KEY: ')
  CALLBACK_URL = input('CALLBACK_URL: ')
  response = twitter_request_token(oauth_consumer_key=API_KEY, oauth_consumer_secret=API_SECRET_KEY, oauth_callback=CALLBACK_URL)

  oauth_token = response_param(response,'oauth_token')
  oauth_token_secret = response_param(response,'oauth_token_secret')
  url = twitter_authorize_url(oauth_token=oauth_token)
  logging.info("Please go here and authorize, %s" % url)

  response_url = input('Paste the full redirect URL here: ')
  oauth_token = response_param(response_url, 'oauth_token')
  oauth_verifier = response_param(response_url, 'oauth_verifier')
  response = twitter_access_token(oauth_token=oauth_token, oauth_verifier=oauth_verifier)
  user_id = response_param(response, 'user_id')
  logging.info("Your twitter's user_id is '%s'" % user_id)

if selected in ['3','facebook','fb','f']:
  logging.info('Authorization at facebook')
  logging.info('-- reference')
  logging.info('https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow?locale=ja_JP\n')

  APP_ID = input('APP_ID: ')
  APP_SECRET = input('APP_SECRET: ')
  CALLBACK_URL = input('CALLBACK_URL: ')
  url = facebook_auth_url(client_id=APP_ID,redirect_uri=CALLBACK_URL)
  logging.info("Please go here and authorize, %s" % url)

  response_url = input('Paste the full redirect URL here: ')
  code = response_param(response_url, 'code')
  logging.debug("code = %s" % code)

  response = facebook_access_token(client_id=APP_ID,client_secret=APP_SECRET,redirect_uri=CALLBACK_URL,code=code)
  response = facebook_user_id(access_token=response['access_token'])
  logging.info("Your facebook's user_id is '%s'" % response['id'])

if selected in ['4','instagram','insta','i']:
  logging.info('Authorization at instagram')
  logging.info('-- reference')
  logging.info('https://www.instagram.com/developer/authentication/\n')

  CLIENT_ID = input('CLIENT_ID: ')
  CLIENT_SECRET = input('CLIENT_SECRET: ')
  REDIRECT_URL = input('REDIRECT_URL: ')
  url = instagram_auth_url(client_id=CLIENT_ID,redirect_uri=REDIRECT_URL)
  logging.info("Please go here and authorize, %s" % url)

  response_url = input('Paste the full redirect URL here: ')
  code = response_param(response_url, 'code')

  response = instagram_access_token(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URL,code=code)
  logging.info("Your instagram's user_id is '%s'" % response['user']['id'])

if selected in ['5','yahoo','y']:
  logging.info('Authorization at yahoo japan')
  logging.info('-- reference')
  logging.info('https://developer.yahoo.co.jp/other/oauth/\n')
