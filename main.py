import PySimpleGUI as sg
import time
from writing import *
from generatejson import *

#application layout
def set_layout(game_board_visability = True, app_setting_visability = False, game_perforance_visability = True):
    #diffrent layouts
    app_buttons = [
        [sg.Button("Start New Game"), sg.Button("Repeat Game"), sg.Button("Game Settings"), sg.Button("App Settings"), sg.Button("Quit")]
    ]

    performance_layout = [
        [sg.Text("WPM:", font=("Any 20"), key="-WPM-"), sg.Text("Accuracy:", font=("Any 20"), key="-accuracy-"), sg.Text("Time:", key="-time_elapsed-", font=("Any 20")), sg.Text("Correct/Incorrect: 0/0", key="-correct_incorrect_words-", font=("Any 20"))]
    ]

    gameboard_layout = [
        [sg.Text("Sentence to type:", font=("Any 20"))],
        [sg.Text(gametext, key="-sentence_to_write-", font=("Any 20")),],
        [sg.Text("", key="-written_text-", font=("Any 40"), size=(100, 1), justification="center")],
        [sg.InputText(key="-text-", font=("Any 20"), size=(20,1), justification="center")],
        [sg.Text("")]
    ]

    result_screen = [
        [sg.Text("Results", font=("Any 20"), size=(100, 1), justification="center")],
        [sg.Text(gametext, key="-result_given_text-", font=("Any 20"))]
    ]

    game_settings = [
        [sg.Text("Game settings", font=("Any 25"), size=(100, 1), justification="center")], 
        [sg.Text("Sentence length", font=("Any 20"), justification="center")],
        [sg.Radio("Random", 1, key="-random_sentence-", enable_events=True),
            sg.Radio("Very short", 1, key="-very_short_sentence-", enable_events=True),
            sg.Radio("Short", 1, key="-short_sentence-", enable_events=True),
            sg.Radio("Medium", 1, key="-medium_sentence-", enable_events=True),
            sg.Radio("Long", 1, key="-long_sentence-", enable_events=True),
            sg.Radio("Very long", 1, key="-very_long_sentence-", enable_events=True),
            sg.Radio("Extreamly long", 1, key="-extremely_long_sentence-", enable_events=True)]
    ]

    app_settings = [
        [sg.Text("App settings", font=("Any 25"), size=(100, 1), justification="center")],
        [sg.Text("Theme", font=("Any 20"), justification="center")],
        [sg.Combo(values=themes, default_value=selected_theme, size=(20, 1), enable_events=True, key="select_theme")]
    ]

    #masterlayout
    master_layout = [
        [sg.VPush()],
        [sg.Column(gameboard_layout, key="-COL1-", element_justification="center", visible = game_board_visability), sg.Column(game_settings, visible=False, key="-COL2-", element_justification="c"), sg.Column(app_settings, visible = app_setting_visability, key="-COL3-", element_justification="c"), sg.Column(result_screen, visible=False, key="-COL4-", element_justification="center")],
        [sg.Column(performance_layout, key="-performance_layout-", justification="center", visible = game_perforance_visability)],
        [sg.Column(app_buttons, justification="center")],
        [sg.VPush()]
    ]
    return master_layout

#change visible layout
def switch_to_start_new_game(layout):
    window[f"-COL{layout}-"].update(visible=False)
    layout = 1
    window[f"-COL{layout}-"].update(visible=True)
    window[f"-performance_layout-"].update(visible=True)
    return layout

def switch_to_repeat_game(layout):
    window[f"-COL{layout}-"].update(visible=False)
    layout = 1
    window[f"-COL{layout}-"].update(visible=True)
    window[f"-performance_layout-"].update(visible=True)
    return layout

def switch_to_game_settings(layout):
    window[f"-COL{layout}-"].update(visible=False)
    layout = 2
    window[f"-COL{layout}-"].update(visible=True)
    window[f"-performance_layout-"].update(visible=False)
    return layout

def switch_to_app_settings(layout):
    window[f"-COL{layout}-"].update(visible=False)
    layout = 3
    window[f"-COL{layout}-"].update(visible=True)
    window[f"-performance_layout-"].update(visible=False)
    return layout

def switch_to_results(layout):
    window[f"-COL{layout}-"].update(visible=False)
    layout = 4
    window[f"-COL{layout}-"].update(visible=True)
    return layout

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

#checks/creates the settings json file
ensure_settings()

#loads the json settings file
with open('settings.json', 'r') as f:
    dictionary = json.load(f)
app_theme = dictionary["app_theme"]
game_lenght = dictionary["game_lenght"]
sentence_length_beginning = game_lenght[0]
sentence_length_end = game_lenght[1]

get_sentence_events = ["-random_sentence-", "-very_short_sentence-", "-short_sentence-", "-medium_sentence-", "-long_sentence-", "-very_long_sentence-", "-extremely_long_sentence-"]

#initial sentance
gametext = random_question()
while True:
    if len(gametext.split()) < sentence_length_beginning or len(gametext.split()) > sentence_length_end:
        gametext = random_question()
    else:
        break
gametextwords = gametext.split()
gametextwordslenght = int(len(gametextwords))

#inputted user text variables
pastuserinput = ""
correct_words = 0
incorrect_words = 0

#current state of the game
is_game_active = True

#time
start_time = time.time()

#application theme
themes = sg.theme_list()
selected_theme = app_theme
current_them = sg.theme()
sg.theme(selected_theme)

#creates the window
window = sg.Window("Typing Test", set_layout(), size=(1000, 300), resizable=True)

#currently visible layout
layout = 1

#creates the event loop
while True:
    event, values = window.read(timeout = 100)

    #the writing functionality
    userinputtext = values["-text-"]

    #removes unnecessary blankspaces
    userinputtext = remove_space_before_word(userinputtext)

    #detects new words, adds them to a list and checks if the word is correct
    if " " in userinputtext:
        pastuserinput = pastuserinput + userinputtext
        userinputtext = ""
        if word_is_correct(len(pastuserinput.split())-1, pastuserinput, gametextwords):
            correct_words += 1
        else:
            incorrect_words += 1
        window["-text-"].update("")

    #prevents written words from exceeding specified character limit 
    userinputtext = userinputtext[:19]

    #updates inputed text
    window["-written_text-"].update(pastuserinput + userinputtext)
    window["-text-"].update(userinputtext)

    #updates the performance layout
    characters = len(pastuserinput)

    if is_game_active == True:
        window["-WPM-"].update("WPM: " + str(round(characters*60 / (5*(time.time() - start_time)))))
        window["-accuracy-"].update("Accuracy: " + str(round(correct_words / gametextwordslenght * 100)) + " %")
        window["-time_elapsed-"].update("Time: " + str(round(time.time() - start_time)))
        window["-correct_incorrect_words-"].update("Correct/Incorrect: {0}/{1}".format(int(correct_words),int(incorrect_words)))

    #buttons that switch layout    
    if event == "Start New Game":
        gametext = random_question()
        while True:
            if len(gametext.split()) < sentence_length_beginning or len(gametext.split()) > sentence_length_end:
                gametext = random_question()
            else:
                break
        window["-sentence_to_write-"].update(gametext)
        gametextwords = gametext.split()
        gametextwordslenght = int(len(gametextwords))
        userinputtext = ""
        pastuserinput = ""
        correct_words = 0
        incorrect_words = 0
        start_time = time.time()
        is_game_active = True
        layout = switch_to_start_new_game(layout)

    elif event == "Repeat Game":
        userinputtext = ""
        pastuserinput = ""
        correct_words = 0
        incorrect_words = 0
        start_time = time.time()
        is_game_active = True
        layout = switch_to_repeat_game(layout)

    elif event == "Game Settings":
        is_game_active = False
        layout = switch_to_game_settings(layout)

    elif event == "App Settings":
        is_game_active = False
        layout = switch_to_app_settings(layout)

    #switch to results when the sentance is written
    if gametextwordslenght == len(pastuserinput.split()) and is_game_active == True:
        is_game_active = False
        layout = switch_to_results(layout)
        window["-result_given_text-"].update(gametext)
        window["-WPM-"].update("WPM: " + str(round(characters*60 / (5*(time.time() - start_time)))))
        window["-accuracy-"].update("Accuracy: " + str(round(correct_words / gametextwordslenght * 100)) + " %")
        window["-time_elapsed-"].update("Time: " + str(round(time.time() - start_time)))

    #change length of the sentence
    if event in get_sentence_events:
        (sentence_length_beginning, sentence_length_end) = get_sentence_length(event)

    #allowes the user to change theme
    if event == "select_theme":
        selected_theme = values["select_theme"]
        window.close()
        sg.theme(selected_theme)
        window = sg.Window("Typing Test", set_layout(False, True, False), size=(1000, 300), resizable=True)

    #updates the settings json file
    if event == "select_theme" or event in get_sentence_events:
        update_settings(selected_theme, sentence_length_beginning, sentence_length_end)

    #end program if user closes window or presses the quit button
    if event == "Quit" or event == sg.WIN_CLOSED:
        break

window.close()