# coding: utf-8
# author: ura1020

import urllib.parse
import logging
import requests
import json

def response_param(uri, key):
  parsed = urllib.parse.urlparse(uri)
  query = parsed.query if parsed.query else parsed.path
  params = dict(urllib.parse.parse_qsl(query))
  return params[key]

def google_code(client_id, redirect_uri):
  encoded = urllib.parse.urlencode({
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': "https://www.googleapis.com/auth/userinfo.profile",
    'response_type': 'code',
  })
  return "https://accounts.google.com/o/oauth2/auth?%s" % encoded

def google_access_token(code, client_id, client_secret, uri):
  encoded = urllib.parse.urlencode({
    'code': urllib.parse.unquote(code),
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': uri,
    'grant_type': 'authorization_code'
  })
  logging.debug("urlencode: %s" % encoded)
  res = requests.post("https://accounts.google.com/o/oauth2/token",
  data=encoded,
  headers={
    'Content-Type': 'application/x-www-form-urlencoded'
  })
  ret = json.loads(res.text)
  logging.debug(ret)
  return ret

def google_user_id(access_token):
  res = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
  params={
    'access_token': access_token
  })
  ret = json.loads(res.text)
  logging.debug(ret)
  return ret

import random, time
import hmac, hashlib, base64

def quote(source):
  return urllib.parse.quote(source, '~')

def twitter_request_token(oauth_consumer_key, oauth_consumer_secret, oauth_callback):
  url = 'https://api.twitter.com/oauth/request_token'
  method = 'POST'
  params = {
    'oauth_consumer_key': oauth_consumer_key,
    'oauth_callback': oauth_callback,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(int(time.time())),
    'oauth_nonce': str(random.getrandbits(64)),
    'oauth_version': '1.0'
  }

  base_string = '%s&%s&%s' % (method,quote(url),quote('&'.join('%s=%s' % (quote(key), quote(params[key])) for key in sorted(params))))
  logging.debug("base_string %s" % base_string)
  params['oauth_signature'] = base64.b64encode(hmac.new(bytes(oauth_consumer_secret+'&', 'UTF-8'), bytes(base_string, 'UTF-8'), hashlib.sha1).digest()).decode('utf-8')
  logging.debug("oauth_signature %s" % params['oauth_signature'])

  res = requests.post("%s?oauth_callback=%s" % (url, quote(oauth_callback)),
  headers={
    'Authorization': 'OAuth %s' % ",".join("%s=\"%s\"" % (quote(key), quote(params[key])) for key in sorted(params) if key != 'oauth_callback')
  })
  logging.debug(res.text)
  return res.text

def twitter_authorize_url(oauth_token):
  return "https://api.twitter.com/oauth/authorize?oauth_token=%s" % oauth_token

def twitter_access_token(oauth_token, oauth_verifier):
  res = requests.post('https://api.twitter.com/oauth/access_token?oauth_token=%s&oauth_verifier=%s' % (oauth_token, oauth_verifier))
  logging.debug(res.text)
  return res.text

def facebook_auth_url(client_id, redirect_uri):
  def _create_state():
    return str(random.getrandbits(64))

  return "https://www.facebook.com/dialog/oauth?" + "&".join(["%s=%s" % (key, quote(value)) for key, value in {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'state': _create_state()
  }.items()])

def facebook_access_token(client_id, client_secret, redirect_uri, code):
  res = requests.get("https://graph.facebook.com/v6.0/oauth/access_token",
  params={
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'client_secret': client_secret,
    'code': code
  })
  ret = json.loads(res.text)
  logging.debug(ret)
  return ret

def facebook_user_id(access_token):
  res = requests.get("https://graph.facebook.com/me",
  params={
    'access_token': access_token
  })
  ret = json.loads(res.text)
  logging.debug(ret)
  return ret

def instagram_auth_url(client_id, redirect_uri):
  return "https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code" % (client_id, redirect_uri)

def instagram_access_token(client_id, client_secret, redirect_uri, code):
  res = requests.post("https://api.instagram.com/oauth/access_token",
  data={
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code',
    'redirect_uri': redirect_uri,
    'code': code
  })
  ret = json.loads(res.text)
  logging.debug(ret)
  return ret

def yahoo_authorization(client_id, redirect_uri):
  def _create_state():
    return str(random.getrandbits(64))

  return "https://auth.login.yahoo.co.jp/yconnect/v2/authorization?" + "&".join(["%s=%s" % (key, quote(value)) for key, value in {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': 'openid profile',
    'state': _create_state()
  }.items()])

def yahoo_v2_token(client_id, client_secret, redirect_uri, code):
  def _create_basic(client_id, client_secret):
    return base64.b64encode(bytes("%s:%s" % (client_id, client_secret), 'utf-8')).decode('utf-8')

  encoded = urllib.parse.urlencode({
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'code': code,
  })
  logging.debug("urlencode: %s" % encoded)

  res = requests.post("https://auth.login.yahoo.co.jp/yconnect/v2/token",
  data=encoded,
  headers={
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % _create_basic(client_id,client_secret)
  })
  ret = json.loads(res.text)
  logging.debug(ret)
  return ret

def yahoo_v1_attribute(access_token):
  res = requests.get("https://userinfo.yahooapis.jp/yconnect/v1/attribute",
  params={
    'schema': 'openid',
  },
  headers={
    'Authorization': 'Bearer %s' % access_token
  })
  ret = json.loads(res.text)
  logging.debug(ret)
  return ret

def yahoo_request_token(oauth_consumer_key, oauth_consumer_secret, redirect_uri):
  url = 'https://auth.login.yahoo.co.jp/oauth/v2/get_request_token'
  method = 'POST'
  params = {
    'oauth_consumer_key': oauth_consumer_key,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(int(time.time())),
    'oauth_nonce': str(int(time.time())),
    'oauth_version': '1.0',
    'oauth_callback': redirect_uri,
  }

  base_string = '%s&%s&%s' % (method,quote(url),quote('&'.join('%s=%s' % (quote(key), quote(params[key])) for key in sorted(params))))
  logging.debug("base_string %s" % base_string)
  params['oauth_signature'] = base64.b64encode(hmac.new(bytes(oauth_consumer_secret+'&', 'UTF-8'), bytes(base_string, 'UTF-8'), hashlib.sha1).digest()).decode('utf-8')
  logging.debug("oauth_signature %s" % params['oauth_signature'])

  res = requests.get(url,
  headers={
    'Authorization': 'OAuth %s' % ",".join("%s=\"%s\"" % (key, params[key]) for key in sorted(params))
  })
  logging.debug(res.text)
  return res.text
