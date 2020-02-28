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

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

csv_file = "/file_being_updated_here.csv"
playlists = [] #same playlists as initial batch if positions are to be analyzed

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

with open(csv_file,'a') as my_file:
    wr = csv.writer(my_file, delimiter=',')
    wr.writerows(zip(*master))
