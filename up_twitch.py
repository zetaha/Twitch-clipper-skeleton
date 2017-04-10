from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import requests
import os
import config
from oauth2client.tools import argparser

## cliend_id and client_secret are obtained at
## dev.twitch.tv
client_id = config.client_id
client_secret= config.client_secret
redirect_uri = config.redirect_uri
scope = config.scope
## path to the video and your title of choice
## 
filepath = config.filepath
title = config.title

def read_in_chunks(file_object,chunksize=18241024):
	while True:
		data = file_object.read(chunksize)
		if not data:
			break
		yield data 

#############################################################
## Script flow:
## 1. auth2.0 procedure for obtaining the token.
##    the token has scopes channel_editor for uploading 
##    and channel_read for retrieving channel_id
## 2. A POST request creates a video on twitch.
## 3. Video upload in chunks 5mb < chunck.size< 25mb
##    with a series of PUT requests.
## 4. A POST request completes the video. 
## 5. Video needs to be processed before it's publicly available
##############################################################
## See https://dev.twitch.tv/docs/v5/guides/video-upload/
## for a complete list of params that can be passed at the video 
## creation and the required formats/bitrate that the video must 
## comply to. 
##############################################################

def auth_web(client_id, redirect_uri,scope,client_secret):
	## This is a standard OAuth2.0 authentication procedure for a web app
	## adapted for twitch API. 
	## see https://requests-oauthlib.readthedocs.io/en/latest/  
	oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,scope=scope)
	auth_url = config.auth_url 
	authorization_url, state = oauth.authorization_url(auth_url,access_type="offline",approval_prompt = "force")

	print ('Please go to %s and authorize access.' % authorization_url)

	authorization_response = input('Enter the full callback URL')

	token_n_scopes = oauth.fetch_token(
        'https://api.twitch.tv/kraken/oauth2/token',
        authorization_response=authorization_response,
        # Twitch specific extra parameter used for client
        # authentication
        client_secret=client_secret)

	return token_n_scopes["access_token"]



def create_video(client_id,token,title):
	headers = { 'client_id' : client_id,
             'oauth_token' : token
             }

	r =requests.get('https://api.twitch.tv/kraken/channel/',headers)
	print('Debug: video created?')
	print(r)
	qq = r.json()
	idd = str(qq["_id"])
	print('debug: channel id: ' +idd)
	channel_id = myid
	headers = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Authorization': 'OAuth '+ token,
    'Client-ID': client_id
    }
	params = {
    'channel_id': channel_id,
    'title': title
    }
	r =requests.post('https://api.twitch.tv/kraken/videos' ,headers=headers,params=params)
	q = r.json()
	return q 


def uploader(token_upload,url_upload,filepath):
	filesize = os.path.getsize(filepath)
	f = open(filepath,'rb')
	part = 1
	headers = {
		'Content-Length' : str(filesize)
		}
	for piece in read_in_chunks(f):
		params = {
		'upload_token' : token_upload, 
		'part' : str(part)}
		part = part+1
		r = requests.put(url_upload,headers=headers,params=params,data=piece)
		print(r)
		print('debug: part ' + str(part-1) + ' done!' ) 



if __name__ == '__main__':

	token = auth_web(client_id,redirect_uri,scope,client_secret)
	q = create_video(client_id,token,title)
	token_upload = q["upload"]["token"]
	url_upload =q["upload"]["url"]
	uploader(token_upload,url_upload,filepath)

	params = {
	'upload_token' : token_upload, 
	}
	r = requests.post(url_upload + '/complete',params=params)
	if (r.status_code ==200):
		print("upload successful")
		print(r.json())

