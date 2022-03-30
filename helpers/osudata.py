    import requests
    
    #for API
    response = requests.get(f'{osu.API_URL}/users/'+ arg, params=params, headers=headers)
    player = response.json()
    avatar = response.json()["avatar_url"]
    stats = response.json()["statistics"]

    #getting information via JSON
    playstyle = player.get('playstyle')
    username = player.get('username')
    accuracy = stats.get('hit_accuracy')
    perfpoints = stats.get('pp')
    playerlvl = stats.get("level")
    mapranks = stats.get('grade_counts')

    playerurl = 'https://osu.ppy.sh/u/' + str(player.get('id'))