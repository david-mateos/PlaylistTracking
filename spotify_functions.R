library(httr)

### set your Spotify credentials with Sys.setenv() first ####

getToken <- function(){
  response <- POST(
    'https://accounts.spotify.com/api/token',
    accept_json(),
    authenticate(Sys.getenv("SPOTIFY_CLIENT_ID"),
                 Sys.getenv("SPOTIFY_SECRET")),
    body = list(grant_type = 'client_credentials'),
    encode = 'form',
    verbose()
  )
  token <- content(response)$access_token
  bearer <- paste("Authorization: Bearer", token, sep = " ")
  return(bearer)
}

getArtist <- function(artist_id){
  call <- paste("https://api.spotify.com/v1/artists/", artist_id, sep="")
  response <- content(GET(call, accept_json(), 
                          add_headers(Authorization= token)))
  return(response)
}

getTrack <- function(track_id){
  call <- paste("https://api.spotify.com/v1/tracks/", track_id, sep="")
  response <- content(GET(call, accept_json(), 
                          add_headers(Authorization= token)))
  return(response)
}

getArtists <- function(artist_ids){
  if (length(artist_ids)<=50){
    ids <- paste(artist_ids, collapse = ",")
    call <- paste("https://api.spotify.com/v1/artists/?ids=", ids, sep="")
    response <- content(GET(call, accept_json(), add_headers(Authorization= token)))
    return(response)
  }
  else{ 
    return("Can only get 50 artists at a time")
  }
}

getTracks <- function(track_ids){
  if (length(track_ids)<=50){
    ids <- paste(track_ids, collapse = ",")
    call <- paste("https://api.spotify.com/v1/tracks/?ids=", ids, sep="")
    response <- content(GET(call, accept_json(), add_headers(Authorization= token)))
    return(response)
  }
  else{ 
    return("Can only get 50 tracks at a time")
  }
}

getPlaylist <- function(playlist_id){
  call <- paste("https://api.spotify.com/v1/playlists/", playlist_id, sep="")
  response <- content(GET(call, accept_json(), 
                          add_headers(Authorization= token)))
  return(response)
}

# compare a playlist from one day to a previous day, return tracks that have appeared
# requires a dataset with different days of playlist data and getToken and getTrack 
# from above to name the track ids
newPlaylistTracks <- function(dataset, pl_id, from, to){
  
  set2 <- dataset %>%
    filter(playlist_id== pl_id) %>%
    filter(date_checked== to) %>%
    select(track_id)
  set1 <- dataset %>%
    filter(playlist_id== pl_id) %>%
    filter(date_checked== from) %>%
    select(track_id)
  setdiff <- setdiff(set2,set1) %>% 
               rowwise() %>%
               mutate(track = getTrack(track_id)$name) %>%
               select(track, track_id)
  return(setdiff)
}

# Test Functions with some real Spotify IDs
test_artist_ids <- c("5cj0lLjcoR7YOSnhnX0Po5","1cNDP5yjU5vjeR8qMf4grg")
test_track_ids <- c("0nbXyq5TXYPCO7pr3N8S4I", "3Dv1eDb0MEgF93GpLXlucZ")
test_playlist_id <- c("4oLzRc3J5ywu7lEF3sfJ1a")

token <<- getToken() # get Authorized first

# Get Information on onw Artist
getArtist(test_artist_ids[1])$name             # name
getArtist(test_artist_ids[1])$followers$total  # followers
unlist(getArtist(test_artist_ids[1])$genres)   # genres

# Get Information on upto 50 Artists
getArtists(test_artist_ids)$artists[[2]]$name            # 2nd Artist's name
unlist(getArtists(test_artist_ids)$artists[[1]]$genres)  # the 1st Artist's genres

# Get Information on upto 50 Tracks
getTracks(test_track_ids)$tracks[[1]]$name     # name of the 1st track
getTracks(test_track_ids)$tracks[[2]]$artists  # the artists on the 2nd track

# Get Info on a Playlist
getPlaylist(test_playlist_id)$name             # playlist name
getPlaylist(test_playlist_id)$tracks$total     # total tracks on playlist
getPlaylist(test_playlist_id)$followers$total  # number of followers
