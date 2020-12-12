import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')
filler_words = ["nach", "bitte", "mir", "suche", "bei", "recherchiere", "zu", "Hey", "Unity"]


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hi ,Guten Morgen")
        print("Hi ,Guten Morgen")
    elif hour >= 12 and hour < 16:
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
            statement = r.recognize_google(audio, language='de-de')
            print(f"user said:{statement}\n")

        except Exception as e:
            #speak("Keine Ahnung was du meinst")
            return "None"
        return statement


print("Loading your personal assistant Unity VI")
speak("Der Assistent fährt hoch...")
time.sleep(3)
speak("Ich bin Unity VI")
wishMe()

if __name__ == '__main__':

    while True:

        statement = takeCommand().lower()
        if statement == 0:
            continue

        if "bye" in statement or "tschau" in statement or "ende" in statement:
            speak('Der Assistent wird beendet,Man sieht sich')
            print('your personal assistant Unity VI is shutting down,Good bye')
            break
        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = ""
            for word in filler_words:
                if word in statement:
                    statement = statement.replace(word, "")
            try:
                wikipedia.set_lang("de")
                results = wikipedia.summary(statement, sentences=3)
            except:
                speak("Nichts gefunden, sorry")
                print("Unity understood: " + statement)
            speak("Nach Wikipedia")
            print(results)
            speak(results)
        elif 'youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube wird aufgerufen")
            time.sleep(5)

        elif 'google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google wird aufgerufen")
            time.sleep(5)

        elif 'gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("GMail wird aufgerufen")
            time.sleep(5)
        elif 'stadia' in statement:
            webbrowser.open_new_tab("https://stadia.google.com/u/2/home")
            speak("Stadia wird aufgerufen")
            time.sleep(5)
        elif 'uhr' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"es ist gerade {strTime}")
        elif 'suche' in statement:
            statement = statement.replace("suche", "")
            for word in filler_words:
                if word in statement:
                    statement = statement.replace(word, "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)


        else:
            if statement != "none":
                speak("Sprich deutsch")




