#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Track Spotify playlists by pulling tracks and other information daily and saving them in a csv file

Start by idenityfing your playlists. 
Get their id by Clicking "Copy Spotify URI" from the share options on Spotify Desktop
"""
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import datetime as dt
import csv

if __name__ == "__main__":
    
    # set your credentials as enviroment variables first
    sp = spotipy.Spotify(client_credentials_manager= SpotifyClientCredentials())

    csv_file = "playlist_file_name.csv" # name your file here
    playlists = []  # your spotify playlist ids here

    playlistJSON = []
    track_id = []
    artist_id = []    # this will be the primary artist
    playlist_id = []  # for tracks with more than 1 artist, call the track
    position = []
    offset = 0

    for playlist in playlists:

        while True:

            response = sp.playlist_tracks(playlist,
                                          offset= offset,
                                          fields=
                                          'items.track.id,items.track.artists')

            playlistJSON.extend(response['items'])

            offset = offset + len(response['items']) #if there 100+ tracks

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

    # only write once and append to same file with a seperate script
    with open(csv_file,'w', newline='') as result_file:
        wr = csv.writer(result_file, delimiter=',')
        wr.writerows(zip(*master))
