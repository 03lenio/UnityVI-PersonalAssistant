import nltk
import pyttsx3
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow as tf
import random
import json
import speech_recognition as sr
from python_json_config import ConfigBuilder

# create config parser
builder = ConfigBuilder()

# parse config
config = builder.parse_config('config.json')
language = config.ai.language
lang_file = 0
print(language)

if language == "de":
    with open('intents_de.json', encoding="utf-8") as file:
        data = json.load(file)
        lang_file = builder.parse_config('lang_de.json')
elif language == "en":
    with open('intents.json') as file:
        data = json.load(file)
        lang_file = builder.parse_config('lang.json')
else:
    with open('intents.json') as file:
        data = json.load(file)
        lang_file = builder.parse_config('lang.json')



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')

if language == "de":
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_ZIRA_11.0')
elif language == "en":
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
else:
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            r_language = language
            statement = r.recognize_google(audio, language=r_language + "-" + r_language)
            print(f"user said:{statement}\n")

        except Exception as e:
            # speak("Keine Ahnung was du meinst")
            return "None"
        return statement


words = []
labels = []
docs_x = []
docs_y = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chat():
    speak(lang_file.chatbot_intro)
    while True:
        inp = takeCommand()
        if inp.lower() in lang_file.chatbot_quit:
            print("this should break")
            from Unity import comprehend
            comprehend()
            break

        if inp != "None":
            results = model.predict([bag_of_words(inp, words)])
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            print(random.choice(responses))
            speak(random.choice(responses))



chat()