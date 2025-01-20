import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

# JSON-Datei laden
with open('data.json', 'r', encoding='utf-8') as file:
    games = json.load(file)

# Zeitfenster definieren: -3 Tage bis +30 Tage ab heute
today = datetime.now()
start_date = today - timedelta(days=3)
end_date = today + timedelta(days=30)

# Spiele nach Datum und Uhrzeit sortieren und filtern
filtered_games = [
    game for game in games
    if start_date <= datetime.fromisoformat(game["gameDateTime"]) <= end_date
]
filtered_games.sort(key=lambda game: datetime.fromisoformat(game["gameDateTime"]))

# HTML-Tabellen-Header
html_content = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f4f4f4;
            text-align: left;
        }
        
        .heim {
            text-align: right; /* Rechte Ausrichtung für Heim-Spalte */
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        a {
            color: inherit;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        img {
            height: 16px;  /* Passt die Logogröße an die Textgröße an */
            vertical-align: middle;
            margin-left: auto;  /* Abstand zwischen Text und Logo */
        }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>Datum & Uhrzeit</th>
                <th>Liga</th>
                <th class="heim">Heim</th>
                <th>Ergebnis</th>
                <th>Gast</th>
                <th>Austragungsort</th>
            </tr>
        </thead>
        <tbody>
"""

# Zeilen für jede gefilterte Partie hinzufügen
for game in filtered_games:
    game_date = datetime.fromisoformat(game["gameDateTime"]).strftime("%d.%m.%Y, %H:%M Uhr")
    
    # Team A (Heim) und Team B (Gast) mit Logos
    team_a_logo = f"https://www.handball.ch/images/club/{game['clubTeamAId']}.png"
    team_b_logo = f"https://www.handball.ch/images/club/{game['clubTeamBId']}.png"
    team_a = f"{game['teamAName']} <img src='{team_a_logo}' alt='Logo {game['teamAName']}'>"
    team_b = f"<img src='{team_b_logo}' alt='Logo {game['teamBName']}'>{game['teamBName']}"
    
    result = f"{game['teamAScoreFT']}:{game['teamBScoreFT']}" if game['gameStatusId'] == 2 else "-"
    league = game["leagueLong"]

    # Google Maps URL generieren
    query = urlencode({"q": f"{game['venueAddress']}, {game['venueCity']}"})
    maps_url = f"https://www.google.com/maps?{query}"
    venue_link = f'<a href="{maps_url}" target="_blank">{game["venue"]}</a>'

    # Spiel Link erstellen
    game_id = game["gameId"]
    handball_url = f"https://www.handball.ch/de/matchcenter/spiele/{game_id}"
    result_link = f'<a href="{handball_url}" target="_blank">{result}</a>'

    html_content += f"""
        <tr>
            <td>{game_date}</td>
            <td>{league}</td>
            <td class="heim">{team_a}</td>
            <td>{result_link}</td>
            <td>{team_b}</td>
            <td>{venue_link}</td>
        </tr>
    """

# Abschluss der HTML-Datei
html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# HTML-Datei speichern
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML-Datei wurde erfolgreich erstellt!")
