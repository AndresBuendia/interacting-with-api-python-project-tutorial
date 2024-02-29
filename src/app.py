from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt

id_ = os.environ.get("CLIENT_ID")
secret = os.environ.get("CLIENT_SECRET")

credentials = SpotifyClientCredentials(client_id=id_, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=credentials)

Blindg_uri = 'spotify:artist:7jxJ25p0pPjk0MStloN6o6'
results = sp.artist_top_tracks(Blindg_uri)
#print(results)

# Creamos un diccionario, imprimimos los datos de las mejores 10 canciones y los agregamos al diccionario
tracks_data = []
for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('popularity    : ' + str(track['popularity']) + ' sobre 100')
    duration_seconds = track['duration_ms'] / 1000
    minutes = int(duration_seconds // 60)
    seconds = int(duration_seconds % 60)
    print('duration: ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds')
    tracks_data.append({
        'Name': track['name'],
        'Popularity': track['popularity'],
        'Duration': f'{minutes} minutes {seconds} seconds',
        'Duration seconds': duration_seconds
    })
    print()

#Creamos el Data Frame y lo ordenamos  por popularidad
df = pd.DataFrame(tracks_data)
df_sorted = df.sort_values(by='Popularity', ascending=False)

# Cogemos los 3 más populares y los imprimimos.
top_3 = df_sorted.head(3)
print(top_3)

# Añadimos una nueva columna con la relación popularidad/duración
df['Ratio Popularity/Duration'] = df['Popularity'] / df['Duration seconds']

#print(df)

# Realizamos scatter plot de duración y popularidad
plt.figure(figsize=(10, 6))
plt.scatter(df['Duration seconds'], df['Popularity'])
plt.title('Relación entre Duración y Popularidad de las Canciones')
plt.xlabel('Duración (segundos)')
plt.ylabel('Popularidad')
plt.show()
