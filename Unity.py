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
        speak("Hi ,Guten Morgen")
        print("Hi ,Guten Morgen")
    elif 12 <= hour < 16:
        speak("Guten Nachmittiag")
        print("Guten Nachmittiag")
    else:
        speak("Hi schön dich zu sehen, ich sehe dich zwar nich aber... ach egal guten abend")
        print("Hi schön dich zu sehen, ich sehe dich zwar nich aber... ach egal guten abend")


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


print("Loading your personal assistant Unity VI")
speak("Der Assistent fährt hoch...")
time.sleep(3)
speak("Ich bin Unity VI")
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
                speak('Der Assistent wird beendet,Man sieht sich')
                print('your personal assistant Unity VI is shutting down,Good bye')
                break
                exit()
        for word in lang_file.wikipedia:
            if word in statement:
                speak('Searching Wikipedia...')
                results = ""
                for word in filler_words:
                    if statement in word:
                        statement = statement.replace(word, "")
                        print("Vlone:" + statement)
                try:
                    wikipedia.set_lang(language)
                    print(statement)
                    results = wikipedia.summary(statement, sentences=3)
                except:
                    print(language)
                    print("Vone" + statement)
                    speak("Nichts gefunden, sorry")
                    print("Unity understood: " + statement)
                speak("Nach Wikipedia")
                print(results)
                speak(results)
        for word in lang_file.google:
                if statement in word:
                    webbrowser.open_new_tab("https://www.google.com")
                    speak("Google wird aufgerufen")
                    time.sleep(5)

        for word in lang_file.gmail:
            if statement in word:
                webbrowser.open_new_tab("gmail.com")
                speak("GMail wird aufgerufen")
                time.sleep(5)

        for word in lang_file.stadia:
            if statement in word:
                webbrowser.open_new_tab("https://stadia.google.com/u/2/home")
                speak("Stadia wird aufgerufen")
                time.sleep(5)

        for word in lang_file.clock:
            if statement in word:
                strTime = datetime.datetime.now().strftime("%H:%M")
                speak(f"es ist gerade {strTime}")

        for word in lang_file.search:
           if word in statement:
                for wrd in filler_words:
                    if wrd in statement:
                        statement = statement.replace(wrd, "")
                webbrowser.open_new_tab(statement)
                time.sleep(5)