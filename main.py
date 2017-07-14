import spotipy
import sys
import spotipy
import spotipy.util as util

scope = 'user-read-currently-playing playlist-modify-private'



if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))

def create_festival_playlist():
    sp = spotipy.Spotify(auth=token)
    with open('artists.txt') as f:
        artists = f.read().splitlines()
    playlist = sp.user_playlist_create(sp.me()['id'], "Ozora Full", public=False)

    playlist_contents = []
    for artist_name in artists:
        
#        if len(playlist_contents) > 200:
#            break
        artist_result = sp.search(artist_name, type='artist', limit=1).get('artists', None)
        if artist_result is None:
            print "No results found for {}".format(artist_name)
            continue

        try:
            artist_id = artist_result['items'][0]['id']
        except IndexError, KeyError:
            print "Artist ({}) has no top tracks".format(artist_name)
            continue
        top_tracks = sp.artist_top_tracks(artist_id).get('tracks', None)
        if top_tracks is None:
            continue
        top_track_ids = [track['id'] for track in top_tracks]
        playlist_contents.extend(top_track_ids)

    
    while len(playlist_contents) > 0:

        print sp.user_playlist_add_tracks(sp.me()['id'], 
                playlist['id'], tracks=playlist_contents[:99])
        playlist_contents = playlist_contents[min(99, len(playlist_contents)):]


def check_is_playing():
    if token:
        with open('artists.txt') as f:
            artists = f.read().splitlines()
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_currently_playing()

        track_artists = map(lambda a: a['name'], results['item']['artists'])
        
        for artist in track_artists:
            if artist in artists:
                print "{} is playing at Ozora.".format(artist)
                return

        print "{} is not playing at Ozora.".format(", ".join(track_artists))

    else:
        print "Can't get token for", username

if __name__ == "__main__":
    create_festival_playlist()
    check_is_playing()
