import pandas as pd
import numpy as np
import spotify_audio_features

merged = pd.read_csv('merged_table.csv')
arr = np.array(merged.values.tolist())

spotifyApi = spotify_audio_features.SpotifyAPI()
# groupedPerYear = {}
flatten_arr = []
winners = []

unknown_tracks = []
for row in arr:
    currentYear = row[0]
    if str(row[8]) == '' or str(row[8]) == None or str(row[8]) == 'nan': # ignore rows that don't have features
        continue
    # if groupedPerYear.get(currentYear) is None:
    #     groupedPerYear.update({currentYear: [row]})
    # else:
    #     groupedPerYear[currentYear].append(row)

    f = row[6:17]
    final = [(row[0])]
    final.extend(f)
    flatten_arr.append(f)
    if str(row[4]) == "1st":
        winners.append(1)
    else:
        winners.append(0)

################ get audio features for missing tracks and save them in an array to update merge_tables.csv
# entries, audio_features = spotifyApi.get_audio_features(unknown_tracks)

# saved_arr = []
# for index,row in enumerate (entries):
#     if(audio_features[index] is None):
#         print(index)
#         continue
#     row[6] = float(audio_features[index]['danceability'])
#     row[7] = float(audio_features[index]['energy'])
#     row[8] = float(audio_features[index]['key'])
#     row[9] = float(audio_features[index]['loudness'])
#     row[10] = float(audio_features[index]['mode'])
#     row[11] = float(audio_features[index]['speechiness'])
#     row[12] = float(audio_features[index]['acousticness'])
#     row[13] = float(audio_features[index]['instrumentalness'])
#     row[14] = float(audio_features[index]['liveness'])
#     row[15] = float(audio_features[index]['valence'])
#     row[16] = float(audio_features[index]['tempo'])

#     saved_arr.append(row)

# with open("my_array", "w", encoding="utf-8") as txt_file:
#     for line in saved_arr:
#         txt_file.write(",".join(line) + "\n") 

################################################################################################################

flatten_arr = np.array(flatten_arr).astype(float)

songPredict = spotifyApi.get_audio_features_single_track('Break a broken heart Andrew Lambrou')
arr =  [float(songPredict[0]['danceability']), float(songPredict[0]['energy']), float(songPredict[0]['key']), float(songPredict[0]['loudness']),
float(songPredict[0]['mode']), float(songPredict[0]['speechiness']), float(songPredict[0]['acousticness']),float(songPredict[0]['instrumentalness']),
float(songPredict[0]['liveness']), float(songPredict[0]['valence']), float(songPredict[0]['tempo'])]
arr = np.array(arr).astype(float)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.neural_network import MLPClassifier

X_train_val, X_test, y_train_val, y_test = train_test_split(flatten_arr, winners, test_size=0.15)

clf = RandomForestClassifier(n_estimators=150)
clf.fit(X_train_val, y_train_val)
accuracy = clf.score(X_test, y_test)
print(clf.predict([arr]))
print(f'Random Forest Accuracy: {accuracy}')
print('--------')

clf = tree.DecisionTreeClassifier(max_depth=6)
clf.fit(X_train_val, y_train_val)
accuracy = clf.score(X_test, y_test)
print(clf.predict([arr]))
print(f'Decision Tree Accuracy: {accuracy}')

print('--------')
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X_train_val, y_train_val)
accuracy = clf.score(X_test, y_test)
print(clf.predict([arr]))
print(f'NN Accuracy: {accuracy}')
