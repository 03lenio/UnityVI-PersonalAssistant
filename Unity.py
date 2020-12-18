import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
from python_json_config import ConfigBuilder
# create config parser
builder = ConfigBuilder()

config = builder.parse_config('config.json')
lang_file = 0
language = config.assistant.language
print(language)

if language == "de":
    lang_file = builder.parse_config('lang_de.json')
elif language == "en":
    lang_file = builder.parse_config('lang.json')
else:
    lang_file = builder.parse_config('lang_de.json')


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')

if language == "de":
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_ZIRA_11.0')
elif language == "en":
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
else:
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')


filler_words = lang_file.filler_words
print(filler_words)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(lang_file.good_morning)

    elif 12 <= hour < 16:
        speak(lang_file.good_noon)

    else:
        speak(lang_file.good_evening)



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



speak(lang_file.booting)
time.sleep(3)
speak(lang_file.intro)
wishMe()
print(lang_file.bye)
if __name__ == '__main__':

    while True:

        statement = takeCommand().lower()
        if statement == 0:
            continue

        for word in lang_file.bye:
            if statement in word:
                print(lang_file.bye)
                speak(lang_file.shutdown)
                break
                exit()
        for word in lang_file.wikipedia:
            if word in statement:
                speak(lang_file.searching_wiki)
                results = ""
                for word in filler_words:
                    if statement in word:
                        statement = statement.replace(word, "")
                try:
                    wikipedia.set_lang(language)
                    print(statement)
                    results = wikipedia.summary(statement, sentences=3)
                except:
                    print(language)
                    speak(lang_file.wiki_404)
                    print("Unity understood: " + statement)
                speak(lang_file.from_wiki)
                print(results)
                speak(results)
        for word in lang_file.google:
                if statement in word:
                    for wrd in filler_words:
                        if statement in wrd:
                            statement = statement.replace(wrd, "")
                    webbrowser.open_new_tab("https://www.google.com")
                    speak(lang_file.google_executed)
                    time.sleep(5)

        for word in lang_file.gmail:
            if statement in word:
                for wrd in filler_words:
                    if statement in wrd:
                        statement = statement.replace(wrd, "")
                webbrowser.open_new_tab("gmail.com")
                speak(lang_file.gmail_executed)
                time.sleep(5)

        for word in lang_file.stadia:
            if statement in word:
                for wrd in filler_words:
                    if statement in wrd:
                        statement = statement.replace(wrd, "")
                webbrowser.open_new_tab("https://stadia.google.com/u/2/home")
                speak(lang_file.stadia_executed)
                time.sleep(5)

        for word in lang_file.clock:
            if statement in word:
                strTime = datetime.datetime.now().strftime("%H:%M")
                speak(str(lang_file.clock_msg) + strTime)

        for word in lang_file.search:
           if word in statement:
                for wrd in filler_words:
                    if wrd in statement:
                        statement = statement.replace(wrd, "")
                webbrowser.open_new_tab(statement)
                time.sleep(5)