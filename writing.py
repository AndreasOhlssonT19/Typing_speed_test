import json
from random import randint

#check writing
def word_is_correct(index, pastuserinput, gametextwords):
    if pastuserinput.split()[index] == gametextwords[index]:
        return True
    return False

def remove_space_before_word(text):
    new_begin = 0
    for character in text:
        if (character != " "): break
        new_begin += 1
    return text[new_begin:]

#returns a random sentence from the json file
def random_question():
    with open("sentences.json") as fp:
        data = json.load(fp)
        questions = data["questions"]
        random_index = randint(0, len(questions)-1)
        return questions[random_index]["text"]