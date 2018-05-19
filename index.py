import os
import json
import requests

# Config
output_folder = './fpl-data'  # Name of output folder
team_ids = []  # Teams whose data we want (strings)
league_ids = []  # Leagues whose data we want (strings)
base_endpoint = 'https://fantasy.premierleague.com/drf'

def save_data(filepath, endpoint):
    r = requests.get(base_endpoint + endpoint)

    dirs = filepath.rsplit('/', 1)[0]

    if not os.path.exists(dirs):
        os.makedirs(dirs)

    with open(filepath, 'w') as outfile:
        json_string = json.loads(r.text)
        json.dump(json_string, outfile, indent=4)
        print('saved ' + filepath)


# General endpoints
sources = [
    {
      'endpoint': '/bootstrap-static',
      'filepath': '/general/main'
    },
    {
      'endpoint': '/teams',
      'filepath': '/general/teams'
    },
    {
      'endpoint': '/elements',
      'filepath': '/general/players'
    },
    {
      'endpoint': '/events',
      'filepath': '/general/gameweeks'
    },
    {
      'endpoint': '/game-settings',
      'filepath': '/general/settings'
    }
]

# Team stats
for t_id in team_ids:
    sources.append({
        'endpoint': '/entry/' + t_id,
        'filepath': '/teams/' + t_id + '/main'
    })

    sources.append({
        'endpoint': '/entry/' + t_id + '/history',
        'filepath': '/teams/' + t_id + '/history'
    })

    sources.append({
        'endpoint': '/entry/' + t_id + '/transfers',
        'filepath': '/teams/' + t_id + '/transfers'
    })

    for event_id in range(1, 39):
        e_id = str(event_id)

        sources.append({
            'endpoint': '/entry/' + t_id + '/event/' + e_id + '/picks',
            'filepath': '/teams/' + t_id + '/picks/gameweek-' + e_id
        })

# Gameweek stats
for event_id in range(1, 39):
    e_id = str(event_id)

    sources.append({
        'endpoint': '/event/' + e_id + '/live',
        'filepath': '/gameweeks/gameweek-' + e_id
    })

# League stats
for l_id in league_ids:
    sources.append({
        'endpoint': '/leagues-classic-standings/' + l_id,
        'filepath': '/leagues/' + l_id + '-standings'
    })

for source in sources:
    filepath = output_folder + source['filepath'] + '.json'
    save_data(filepath, source['endpoint'])
