import requests
import json

url = "https://clubapi.handball.ch/rest/v1/clubs/296614/games"

headers = {
  'Authorization': 'Basic **Obscured for Security**'
}

response = requests.get(url, headers=headers)
data = response.json()

# Unerwünschte Zeichen am Ende entfernen
for game in data:
    if 'teamAName' in game and isinstance(game['teamAName'], str):
        game['teamAName'] = game['teamAName'].rstrip(' °')
    if 'teamBName' in game and isinstance(game['teamBName'], str):
        game['teamBName'] = game['teamBName'].rstrip(' °')


# In JSON exportieren
with open('data.json', 'w', encoding='utf-8') as json_file: 
    json.dump(data, json_file, ensure_ascii=False, indent=4)