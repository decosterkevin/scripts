import spotipy
import spotipy.util as util
import sys, getopt
import yaml

spotipy_redirect_uri = 'http://127.0.0.1/callback/'
SCOPE = 'playlist-modify-private'
default_playlist_name = "new_playlist"


class SpotifyAPI:


    def __init__(self, username, user_id,spotipy_client_id,spotipy_client_secret):
        self.username = username
        self.user_id = user_id
        self.spotipy_client_id=spotipy_client_id
        self.spotipy_client_secret = spotipy_client_secret


    def initialize(self):
        token = util.prompt_for_user_token(self.username, SCOPE, client_id=self.spotipy_client_id,
                                           client_secret=self.spotipy_client_secret, redirect_uri=spotipy_redirect_uri)
        if token:
            self.sp = spotipy.Spotify(auth=token)

    def get_playlist_tracks(self, user_id, playlist_id):
        results_init = self.sp.user_playlist_tracks(user_id, playlist_id)
        results = results_init['tracks']
        tracks = results['items']
        if(results['next'] is not None):
            while results['next']:
                results = self.sp.next(results)
                tracks.extend(results['items'])

        track_ids = [item['track']['id'] for item in tracks]
        return track_ids

    def add_entry2playlist(self,new_play, owner_id, owner_playlist_id):

        new_playlist_id = new_play['id']
        track_ids = self.get_playlist_tracks(owner_id, owner_playlist_id)

        print("tracks extracted")
        chunks = [track_ids[x:x + 100] for x in range(0, len(track_ids), 100)]

        sys.stdout.write("\rTracks adding: %d%%" % 0.0)
        sys.stdout.flush()

        for i in range(len(chunks)):
            sys.stdout.write("\rTracks adding: %d%%" % int((i / float(len(chunks))) * 100.0))
            sys.stdout.flush()
            self.sp.user_playlist_add_tracks(self.user_id,new_playlist_id, chunks[i])

        sys.stdout.write("\rTracks adding: %d%%" % 100.0)

    def copy_playlist(self,owner_id, owner_playlist_id):
        new_play = self.sp.user_playlist_create(user=self.user_id, name=default_playlist_name, public=False)
        if (new_play is not None and new_play.get is not None):
            print("playlist created")
            self.add_entry2playlist(new_play, owner_id, owner_playlist_id)
            print("\nYou can know check your new playlist within your MUSIC spotify space!")
        else:
            print("Can't create playlist")

    def merge_playlists(self,owner_ids, owner_playlist_ids):
        if (len(owner_ids) is len(owner_playlist_ids)):
            new_play = self.sp.user_playlist_create(user=self.user_id, name=default_playlist_name, public=False)
            if (new_play is not None and new_play.get is not None):
                print("playlist created")
                for id, playlist in zip(owner_ids, owner_playlist_ids):
                    self.add_entry2playlist(new_play, id, playlist)
                    print("\nPlaylist merged with success")
            else:
                print("Can't create playlist")


def main(argv):
    configFile = ''
    paramFile=''
    fct='copy'
    try:
        opts, args = getopt.getopt(argv, ":c:p:")
        print(argv)
    except getopt.GetoptError:
        print('helpers.py -c <config file .yaml> -p <params file .yaml>' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('helpers.py -c <config file .yaml> -p <params file .yaml>' )
            sys.exit()
        elif opt in ("-c", "--config"):
            configFile = arg
        elif opt in ("-p", "--playlist"):
            paramFile = arg

    print(args)
    for a in args:
        if a == 'copy':
            fct='copy'
        elif a == 'merge':
            fct = 'merge'
    print(fct)
    config = yaml.safe_load(open(configFile))
    params = yaml.safe_load(open(paramFile))

    # YOUR PARAMETERS
    username = config.get("username")
    user_id = config.get("user_id")
    spotipy_client_id = config.get("spotipy_client_id")
    spotipy_client_secret = config.get("spotipy_client_secret")

    if None in (user_id, username, spotipy_client_id, spotipy_client_secret):
        print("error in config file")
        sys.exit(2)


    spotifyAPI = SpotifyAPI( username,user_id, spotipy_client_id, spotipy_client_secret)

    owner_playlist_ids= params.get("playlists")
    owner_ids=params.get("ids")
    if None in (owner_playlist_ids, owner_ids):
        print("error in  parameters file")
        sys.exit(2)

    spotifyAPI.initialize()

    if __name__ == '__main__':
        if fct is "copy":
            print("COPYING")
            spotifyAPI.copy_playlist(owner_ids[0], owner_playlist_ids[0])
        elif fct is "merge":
            print("MERGING")
            spotifyAPI.merge_playlists(owner_ids, owner_playlist_ids)


if __name__ == "__main__":
    main(sys.argv[1:])

