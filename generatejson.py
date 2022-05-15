import json

#creates new json file if settings.json is missing
def ensure_settings():
    dictionary ={ 
        "app_theme" : "DarkTeal9", 
        "game_lenght" : [0, 100]
    }

    try:
        with open('settings.json', 'r') as f:
            a=0

    except FileNotFoundError:
        with open("settings.json", "w") as outfile: 
            json.dump(dictionary, outfile)

#updates settings.json
def update_settings(selected_theme, sentence_length_beginning, sentence_length_end):
    dictionary = {}
    dictionary["app_theme"] = selected_theme
    dictionary["game_lenght"] = [sentence_length_beginning, sentence_length_end]

    with open("settings.json", "w") as outfile: 
        json.dump(dictionary, outfile)