#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update the file created in the initialization 
script. This script should be scheduled to run every 24 hrs at least
"""
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import datetime as dt
import csv
import os

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) # make sure credentials are env vars
playlists = [] # same playlists as initial batch if positions are to be analyzed

playlistJSON = []
track_id = []
artist_id = []
playlist_id = []
position = []
offset = 0

for playlist in playlists:
    
    while True:
        
        response = sp.playlist_tracks(playlist,
                                      offset=offset,
                                      fields=
                                      'items.track.id,items.track.artists')
        #remove positions where there is a video. uncomment if your playlists have videos
        #response['items'] = [s for s in response['items'] if s['track'] != None]
        playlistJSON.extend(response['items'])
        
        offset = offset + len(response['items']) # if there 100+ tracks
        
        if len(response['items']) == 0:
            break
       
    for i, track in enumerate(playlistJSON):
        
        track_id.append(track['track']['id'])
        artist_id.append(track['track']['artists'][0]['id'])
        playlist_id.append(playlist)
        position.append(i+1)
        
    offset = 0    
    playlistJSON = []


today = dt.datetime.today().strftime('%Y-%m-%d')
date_checked = [today]*len(position)

master = track_id, artist_id, playlist_id, position, date_checked

file_updating = 'file.csv' # the csv you are updating
file_path = os.getcwd()+'/'+file_updating

with open(file_path,'a') as my_file:
    wr = csv.writer(my_file, delimiter=',')
    wr.writerows(zip(*master))
