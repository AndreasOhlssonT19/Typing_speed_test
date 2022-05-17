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
        [sg.Text(sentence_to_write, key="-sentence_to_write-", font=("Any 20")),],
        [sg.Text("", key="-all_inputted_text-", font=("Any 40"), size=(100, 1), justification="center")],
        [sg.InputText(key="-currently_inputted_text-", font=("Any 20"), size=(20,1), justification="center")],
        [sg.Text("")]
    ]

    result_screen = [
        [sg.Text("Results", font=("Any 20"), size=(150, 1), justification="center")],
        [sg.Text(sentence_to_write, key="-result_given_text-", font=("Any 20"))]
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
            sg.Radio("Extremely long", 1, key="-extremely_long_sentence-", enable_events=True)]
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
def switch_layout(layout, switch_layout, toggle_performance_layout):
    window[f"-COL{layout}-"].update(visible=False)
    layout = switch_layout
    window[f"-COL{layout}-"].update(visible=True)
    window[f"-performance_layout-"].update(visible=toggle_performance_layout)
    return layout

#update performance layout
def update_performance_layout():
    window["-WPM-"].update("WPM: " + str(round(((len(past_inputted_text) / 5) / (time.time() - start_time)) * 60)))
    window["-accuracy-"].update("Accuracy: " + str(round(correct_words / sentence_to_write_lenght * 100)) + " %")
    window["-time_elapsed-"].update("Time: " + str(round(time.time() - start_time)))
    window["-correct_incorrect_words-"].update("Correct/Incorrect: {0}/{1}".format(int(correct_words),int(incorrect_words)))

#checks/creates the settings json file
ensure_settings()

#loads the json settings file
with open('settings.json', 'r') as f:
    dictionary = json.load(f)
app_theme = dictionary["app_theme"]
sentence_lenght = dictionary["sentence_lenght"]
sentence_length_beginning = sentence_lenght[0]
sentence_length_end = sentence_lenght[1]

#all change sentence lenght events
get_sentence_events = ["-random_sentence-", "-very_short_sentence-", "-short_sentence-", "-medium_sentence-", "-long_sentence-", "-very_long_sentence-", "-extremely_long_sentence-"]

#initial sentance
sentence_to_write = random_question()
sentence_to_write = correct_random_sentence(sentence_to_write, sentence_length_beginning, sentence_length_end)
sentence_to_write_words = sentence_to_write.split()
sentence_to_write_lenght = int(len(sentence_to_write_words))

#inputted user text variables
past_inputted_text = ""
number_of_writen_words = 0
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
    currently_inputted_text = values["-currently_inputted_text-"]

    #removes unnecessary blankspaces
    currently_inputted_text = remove_space_before_word(currently_inputted_text)

    #detects new words, adds them to a list and checks if the word is correct
    if " " in currently_inputted_text:
        past_inputted_text = past_inputted_text + currently_inputted_text
        currently_inputted_text = ""
        number_of_writen_words += 1
        if word_is_correct(len(past_inputted_text.split())-1, past_inputted_text, sentence_to_write_words):
            correct_words += 1
        else:
            incorrect_words += 1
        window["-currently_inputted_text-"].update("")

    #prevents written words from exceeding specified character limit 
    currently_inputted_text = currently_inputted_text[:19]

    #prevents past inputted words from exceeding specified character limit
    if len(past_inputted_text.split()) > 10:
        past_inputted_text = past_inputted_text.split(' ', 1)[1]

    #updates the performance layout
    if is_game_active == True:
        update_performance_layout()

    #buttons that switch layout    
    if event == "Start New Game":
        sentence_to_write = random_question()
        sentence_to_write = correct_random_sentence(sentence_to_write, sentence_length_beginning, sentence_length_end)
        window["-sentence_to_write-"].update(sentence_to_write)
        sentence_to_write_words = sentence_to_write.split()
        sentence_to_write_lenght = int(len(sentence_to_write_words))
        currently_inputted_text = ""
        past_inputted_text = ""
        number_of_writen_words = 0
        correct_words = 0
        incorrect_words = 0
        start_time = time.time()
        is_game_active = True
        layout = switch_layout(layout, 1, True)
    
    elif event == "Repeat Game":
        currently_inputted_text = ""
        past_inputted_text = ""
        number_of_writen_words = 0
        correct_words = 0
        incorrect_words = 0
        start_time = time.time()
        is_game_active = True
        layout = switch_layout(layout, 1, True)

    elif event == "Game Settings":
        is_game_active = False
        layout = switch_layout(layout, 2, False)

    elif event == "App Settings":
        is_game_active = False
        layout = switch_layout(layout, 3, False)

    #switch to results when the sentance is written
    if sentence_to_write_lenght == number_of_writen_words and is_game_active == True:
        is_game_active = False
        window["-result_given_text-"].update(sentence_to_write)
        update_performance_layout()
        layout = switch_layout(layout, 4, True)

    #updates inputed text
    window["-all_inputted_text-"].update(past_inputted_text + currently_inputted_text)
    window["-currently_inputted_text-"].update(currently_inputted_text)

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