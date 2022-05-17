import json

#creates new json file if settings.json is missing
def ensure_settings():
    dictionary ={ 
        "app_theme" : "DarkTeal9", 
        "sentence_lenght" : [0, 100]
    }

    try:
        with open('settings.json', 'r') as f:
            a=0

    except FileNotFoundError:
        with open("settings.json", "w") as outfile: 
            json.dump(dictionary, outfile)

#change length of the sentence
def get_sentence_length(event):
    global sentence_length_beginning, sentence_length_end
    get_sentence_dict = {
        "-random_sentence-": (0, 100),
        "-very_short_sentence-": (0, 5),
        "-short_sentence-": (5, 10),
        "-medium_sentence-": (10,15),
        "-long_sentence-": (15, 20),
        "-very_long_sentence-": (20, 25),
        "-extremely_long_sentence-": (25, 30)
    }
    if (event in get_sentence_dict.keys()):
        sentence_length_beginning, sentence_length_end = get_sentence_dict[event]
        return (sentence_length_beginning, sentence_length_end)

#updates settings.json
def update_settings(selected_theme, sentence_length_beginning, sentence_length_end):
    dictionary = {}
    dictionary["app_theme"] = selected_theme
    dictionary["sentence_lenght"] = [sentence_length_beginning, sentence_length_end]

    with open("settings.json", "w") as outfile: 
        json.dump(dictionary, outfile)