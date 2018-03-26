# Helpers

## Spotify Helpers
Using the Spotipy librairy (Spotify Python api), this project proposes some utilities function to help enhance the spotify experience

### Installation

#### First install [spotipy](https://spotipy.readthedocs.io/) - The Python Spotify API and YAML
```
sudo pip install spotipy
sudo pip3 install pyyaml
```
(Optionnal) To install pip:
```
sudo apt-get install python-setuptools python-dev build-essential
```

#### Set your dev spotify account

Go to https://beta.developer.spotify.com/ and register your application. You'll get the client_id and the client_secret. Don't forget to add the returning URI under "edit setting"/"Redirect URIs" (Add, and Save)

#### Modify the constantes parameters inside the file (client_id, client_secret, playlist_id, etc)

#### Execute the script
```
python script.py
```
### Availble scripts

* *copy_playlist*: given a playlist ID and its owner user ID, extract and copy all musics into a private personal playlist. Mostly to enable editing (eg: delete and add track)

## Automatic email sender from CSV

### Execute the script
```
python3 script.py
python3 myEmail.py -f users.csv -t options.yaml -c config.yaml
```


