import json
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '0330be678b234217951a99b60e76042d'
client_secret = '8ad069aa1a9a471099b6427fc4f85616'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id='6c93h7EVT1iyp32k7uJTJ7' #insert your playlist id #spotify:playlist:6c93h7EVT1iyp32k7uJTJ7
#https://open.spotify.com/playlist/6c93h7EVT1iyp32k7uJTJ7?si=k3f25SF-QDG5Pgt9fPkJlA
#https://open.spotify.com/playlist/?si=KHK17MgRTXqQrYL0rkCBKg


def creategraph(pop, dance, val, instrumental, speech, live):
    import plotly.express as px
    import pandas as pd
    df = pd.DataFrame(dict(
        r=[pop, dance, val, instrumental, speech, live],
        theta=['Popularity','Danceability','Valence',
            'Instrumentalness', 'Speechiness', 'Liveness']))
    fig = px.line_polar(df, r='r', theta='theta',  line_close=True, title= "Playlist Analysis" +'\n' + "Created By Shyam Ravichandran")
    fig.update_traces(fill='toself')
    fig.show()


playlistUrl = input('Enter the URL to your Spotify Playlist: ')
playlistUrl = playlistUrl[playlistUrl.index("playlist/") + 9: playlistUrl.index("?si=")]
   # create a list of song ids
track_data=[]
popularity_data=[]
id_data = []
danceability_data = []
valence_data = []
instrumentalness_data = []
speechiness_data = []
liveness_data = []
counter =0
lenofarray = 0
milleSeconds = 0
for i in range (15):
    results = sp.playlist_tracks(playlistUrl, limit = 100, offset = lenofarray)
    for item in results['items']:
            
        if (int(item['track']['popularity']) != 0 or item['track']['id'] != None):      
            track = [ ['popularity'], [int(item['track']['popularity'])], ['name', item['track']['name']]]
            popularity_data.append(int(item['track']['popularity']))
            track_data.append(track)
            id_data.append(item['track']['id'])

        counter+=1
            
        if(counter == 100):
            lenofarray+=100
            counter = 0
        else:
            break
   
    counter = 0


for x in range(len(id_data)):
    aud_anal = sp.audio_features(id_data[x])
    for anal in aud_anal:
        if(anal != None):
            try:
                danceability_data.append(float(anal['danceability']))
                valence_data.append(float(anal['valence']))
                instrumentalness_data.append(float(anal['instrumentalness']))
                speechiness_data.append(float(anal['speechiness']))
                liveness_data.append(float(anal['liveness']))
                milleSeconds += float(anal['duration_ms'])

            except TypeError as typeerror:
                print("local file, No Data Values Assigned", typeerror)
            
        counter+=1
            
avgPop = (sum(popularity_data)/len(popularity_data) / 1.5)
avgDance = (sum(danceability_data)/len(danceability_data) * 50)
avgVal = (sum(valence_data)/len(valence_data) * 87)
avginst = (sum(instrumentalness_data)/len(instrumentalness_data) * 200)
avgspeech = (sum(speechiness_data)/len(speechiness_data) * 125)
avglive = (sum(liveness_data)/len(liveness_data) * 200)

creategraph(avgPop, avgDance, avgVal, avginst, avgspeech, avglive)

    
def msToHours(millseconds = None):
    return (millseconds / 3600000)


