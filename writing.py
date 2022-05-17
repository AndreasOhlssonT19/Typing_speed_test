import json
from random import randint

#returns a random sentence from the json file
def random_question():
    with open("sentences.json") as fp:
        data = json.load(fp)
        questions = data["questions"]
        random_index = randint(0, len(questions)-1)
        return questions[random_index]["text"]

#check and generate correct random sentance
def correct_random_sentence(sentence_to_write, sentence_length_beginning, sentence_length_end):
    while True:
        if len(sentence_to_write.split()) < sentence_length_beginning or len(sentence_to_write.split()) > sentence_length_end:
            sentence_to_write = random_question()
        else:
            break
    return sentence_to_write

#checks if the word is correct
def word_is_correct(index, pastuserinput, gametextwords):
    if pastuserinput.split()[index] == gametextwords[index]:
        return True
    return False

#removes unnecessary blankspaces
def remove_space_before_word(text):
    new_begin = 0
    for character in text:
        if (character != " "): break
        new_begin += 1
    return text[new_begin:]

