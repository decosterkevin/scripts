import spotipy
import spotipy.util as util
import sys, getopt
import yaml

def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def main(argv):
    configFile = ''
    # THE COPIED PLAYLIST PARAMETERS
    # In the playlist you want to copy, click on .../share/copy URI link.
    # you'll find the playlist id and owner id on this form : spotify:user:owner_id:playlist:owner_playlist_id
    owner_playlist_id = '5VwZqaTQRojL3oKfemRcJz'
    owner_id = '12133416038'
    try:

        opts, args = getopt.getopt(argv, "hi:c:p:")
        print(argv)
    except getopt.GetoptError:
        print('copy_playlist.py -i <user id> -p <playlist id from owner -i> -c <config file .yaml>')
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print('copy_playlist.py -i <user id> -p <playlist id from owner -i> -c <config file .yaml>')
            sys.exit()
        elif opt in ("-i", "--id"):
            owner_id = arg
        elif opt in ("-c", "--config"):
            configFile = arg
        elif opt in ("-p", "--playlist"):
            owner_playlist_id = arg

    config = yaml.safe_load(open(configFile))
    SCOPE = 'playlist-modify-private'

    # YOUR PARAMETERS
    # usually the email adress
    username = config.get("username")

    # can be found in a "shared" link after key "user"
    user_id = config.get("user_id")

    # Neet to register your app in the Web Dev Spotify space
    spotipy_client_id = config.get("spotipy_client_id")
    spotipy_client_secret = config.get("spotipy_client_secret")

    if None in (user_id, username, spotipy_client_id, spotipy_client_secret):
        print("error in config parameters")
        sys.exit(2)

    spotipy_redirect_uri = 'http://127.0.0.1/callback/'
    token = util.prompt_for_user_token(username, SCOPE, client_id=spotipy_client_id,
                                       client_secret=spotipy_client_secret, redirect_uri=spotipy_redirect_uri)

    if __name__ == '__main__':
        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.user_playlist(owner_id, owner_playlist_id)
            name = results['name']

            new_play = sp.user_playlist_create(user_id, name, public=False)
            if (new_play is not None and new_play.get is not None):
                print("playlist created")
                new_playlist_id = new_play['id']
                tracks = get_playlist_tracks(sp,owner_id, owner_playlist_id)
                track_ids = [item['track']['id'] for item in tracks]
                print("tracks extracted")
                chunks = [track_ids[x:x + 100] for x in xrange(0, len(track_ids), 100)]

                sys.stdout.write("\rTracks adding: %d%%" % 0.0)
                sys.stdout.flush()
                for i in range(len(chunks)):
                    sys.stdout.write("\rTracks adding: %d%%" % int((i / float(len(chunks))) * 100.0))
                    sys.stdout.flush()
                    sp.user_playlist_add_tracks(user_id, new_playlist_id, chunks[i])

                sys.stdout.write("\rTracks adding: %d%%" % 100.0)

                print("\nYou can know check your new playlist within your MUSIC spotify space!")
            else:
                print("Can't create playlist")
        else:
            print("Can't get token for", username)


if __name__ == "__main__":
    main(sys.argv[1:])

