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
        a {
            color: inherit;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        img {
            height: 1.5em;  /* Passt die Logogröße an die Textgröße an */
            vertical-align: middle;
        }
        .logo-row {
            width: 4em;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        .img-container {
            width: 4em;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .heim {
            text-align: right;
        }
        .score {
            text-align: center;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        tbody > tr {
            border: none;
            border-top: 1px grey solid; 
        }
        td {
            border: none;
        }
        .no-border {
            border-top: none;
        }
        tbody > tr:first-child {
            border-top: 2px black solid
        }
        tr:last-child {
            border-bottom: 1px grey solid
        }
        tr.no-border > td {
            padding-top: 0;
        }
    </style>
</head>
<body>
    <table class="table table-hover">
        <thead>
            <tr>
                <th>Datum</th>
                <th>Liga</th>
                <th class="heim">Heim</th>
                <th></th>
                <th class="score">Ergebnis</th>
                <th></th>
                <th class="gast">Gast</th>
                <th>Austragungsort</th>
            </tr>
        </thead>
        <tbody>
"""


previous_date = None
# Zeilen für jede gefilterte Partie hinzufügen
for game in filtered_games:
    game_datetime = datetime.fromisoformat(game["gameDateTime"])
    
    if previous_date and previous_date.date() == game_datetime.date():
        row_class = "no-border" 
        indent = "&nbsp;" * 19
        game_date = indent + game_datetime.strftime("%H:%M Uhr")
    else: 
        row_class = ""
        game_date = game_datetime.strftime("%d.%m.%Y, %H:%M Uhr")
    
    # Team A (Heim) und Team B (Gast) mit Logos
    team_a_logo = f"https://www.handball.ch/images/club/{game['clubTeamAId']}.png"
    team_b_logo = f"https://www.handball.ch/images/club/{game['clubTeamBId']}.png"
    
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
        <tr class="{row_class}">
            <td>{game_date}</td>
            <td>{league}</td>
            <td class="heim">{game['teamAName']}</td>
            <td class="logo-row"><div class='img-container'><img src='{team_a_logo}' alt='Logo {game['teamAName']}'></div></td>
            <td class="score">{result_link}</td>
            <td class="logo-row"><div class='img-container'><img src='{team_b_logo}' alt='Logo {game['teamBName']}'></div></td>
            <td class="gast">{game['teamBName']}</td>
            <td>{venue_link}</td>
        </tr>
    """
    previous_date = game_datetime

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

