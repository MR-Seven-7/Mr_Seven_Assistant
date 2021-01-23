'''
Things to do --
- Send an Email -- Not Secure, Leave it
- Start application/Open files with the Keystroke/Commands you specifY. -- Done 
- Play music from the default directories (can be changed)  -- Done
- Run a Command in Windows Terminal/Command Propmpt. -- Done
- Search Wikipedia for you. -- Done
- Remind you something (Works Only if the program is running, at the time specified). -- Can't Handle It Along with other processes
- Start a timer for you. -- Cancelled
- Open website for you. -- Done
- Reply to some other basic questions, like "What's the time?" or "What's your name?" -- A few done
- Search Youtube -- Done
'''


# Importing Required Modules
from threading import Thread
import webbrowser as wb
from random import randint
import datetime
import os
import json
import pyttsx3 as ps
import wikipedia as wiki
import speech_recognition as sr
import youtubesearchpython as yt_search
#import goslate as gs
# from pynput.keyboard import Listener, Key
# from googlesearch import search
from googlesearch import search

languages = ["en-us", "en-In"]

musicDir = os.path.join(os.path.expanduser("~"), "Music")

default_settings = {
    "name":"Jarvis",
    "voice":0,
    "rate":200,
    "language":languages[0],
    "music dir":musicDir
}

try:
    with open('file/config.txt', 'r') as f:
        settings = json.loads(f.readline().replace("'", '"'))
except:
    with open('file/config.txt', 'w') as f:
        f.writelines(str(default_settings))
        settings = default_settings

try:
    with open('file/commands.txt', 'r') as f:
        x = f.readlines()
        try:
            openCommands = json.loads(x[0].replace("'", '"'))
        except:
            openCommands = {}

        try:
            runCommands = json.loads(x[1].replace("'", '"'))
        except:
            runCommands = {}

except Exception as e:
    print(e)
    with open('file/commands.txt', 'w') as f:
        openCommands = {}
        runCommands = {}

def updateSettings(voice):
    with open('file/config', 'r') as f:
        settings = f.readlines()
        settings = dict(settings)
        
    with open('file/config', 'w') as f:
        f.write(settings)

# Function to Speak up the result
def speak(string):
    '''Speak the string given as parameter'''
    speak = ps.init('sapi5')
    voices = speak.getProperty('voices')
    rate = speak.getProperty('rate')
    speak.setProperty('rate', settings["rate"])
    speak.setProperty('voice', voices[settings["voice"]].id)
    speak.say(string)
    speak.runAndWait()

# Funtion to Recognize the Command Given by speaking
def recognize():
    '''Recognize the voice'''
    recognizer = sr.Recognizer()
    if settings['microphone'] != 'default':
        with sr.Microphone(settings['microphone']) as source:
            recognizer.pause_threshold = 1
            print("Listening...")
            audio = recognizer.listen(source)
    else:
        with sr.Microphone() as source:
            recognizer.pause_threshold = 1
            print("Listening...")
            audio = recognizer.listen(source)
    try:
        print('Trying to recognize...')
        text = recognizer.recognize_google(audio, language=settings["language"])
        # translator = gs.Goslate()
        # text = translator.translate(text, 'En')
        print(text)
        return text
    except Exception as e:
        print(e)
        print("Unable to understand, Mind speaking that again, sir?")
        return "None"

# Function to interpret and execute the command
def execute_command(command):
    ''' This Function tries to figure out what user has commanded/requested for and execute it accordingly.'''
    if command == False:
        return (False, "Couldn't Understand!")
    real_command = command
    command = command.capitalize()
    command = command.replace(settings["name"], '')
    command = command.lower()
    command = command.replace(" ", '')

    for cmds in openCommands:
        cmds_check = cmds.replace(" ", "")
        cmds_check = cmds_check.lower()
        if command == cmds_check:
            try:
                os.startfile(openCommands[cmds])
                return (True, "successful")
            except:
                return (False, "Couldn't Load File!")
    for cmds in runCommands:
        cmds_check = cmds.replace(" ", "")
        cmds_check = cmds_check.lower()
        if cmds_check in command:
            ("Found Command")
            command_to_run = runCommands[cmds] + " " + command.replace(cmds_check, "")
            os.system('start ' + runCommands[cmds] + " " + command_to_run)
            return (True, "successful")

    if command == 'settings' or command == 'opensettings' or command == 'setting' or command=='opensetting':
        # os.startfile(__file__.replace('assitant.py', 'settings.pyw'))
        os.startfile('settings.pyw')
        return (True, "successful")
    if command == 'quit' or command == 'exit' or command == 'close' or command=='bye' or command=='byebye':
        exit()
        return "Bye Have a nice day"
    if "play" in command:
        command = command.replace("play", "")
        command = command.replace("songs", "")
        command = command.replace("song", "")
        command = command.strip()
        music_dir = os.listdir(settings["music dir"])
        if music_dir == "None":
            music_dir = os.environ['Music']
        if "some" in command or command == '':
            music_dir = os.listdir(settings["music dir"])
            for files in music_dir:
                if not(".mp3" in files or ".wav" in files or ".flac" in files):
                    music_dir.remove(files)
            if len(music_dir) > 0:
                song_to_play = music_dir[randint(0, len(music_dir) - 1)]
                music_path = os.path.join(settings["music dir"], song_to_play)
                if ".mp3" in song_to_play or ".flac" in song_to_play or ".wav" in song_to_play:
                    os.startfile(music_path)
                    return (True, "successful")
            else:
                search_results = yt_search.SearchVideos(keyword=command + "song", mode="dict", max_results=1)
                results = search_results.result()
                link = results["search_result"][0]["link"]
                wb.open(link)
                return (True, "successful")


        else:
            command = command.replace("music", "")
            command = command.replace("songs", "")
            command = command.replace("song", "")
            music_dir = os.listdir(settings["music dir"])
            for songs in music_dir:
                if not(".mp3" in songs or ".wav" in songs or ".flac" in songs):
                    continue
                songs = songs.lower()
                songs_check = songs.replace(" ", "")
                if command in songs_check:
                    os.startfile(os.path.join(settings["music dir"], songs))
                    return (True, "successful")

        search_results = yt_search.SearchVideos(keyword=command + "song", mode="dict", max_results=1)
        results = search_results.result()
        link = results["search_result"][0]["link"]
        wb.open(link)
        return (True, "successful")

    if "open" in command:
        search_results = search(real_command.replace("open", ""))
        wb.open(search_results[0])
        return (True, "successful")

    if "wiki" in command or "wikipedia" in command:
        query_to_search = real_command.lower()
        query_to_search = query_to_search.replace("wikipedia", "")
        query_to_search = query_to_search.replace("wiki", "")
        query_to_search = query_to_search.replace("search", "")
        query_to_search = query_to_search.replace("for", "")
        try:
            return (True, "According to wikipidea," + wiki.summary(title=query_to_search, sentences=2, auto_suggest=False))
        except:
            return (True, "According to wikipidea," + wiki.summary(title=query_to_search, sentences=2, auto_suggest=True))
        else:
            return (False, "Couldn't search wikipedia")

    if "time" in command:
        return (True, datetime.datetime.now().strftime("%I:%M %p"))

    if "date" in command:
        return (True, datetime.datetime.now().strftime("%A, %B %d, %Y"))

    if "whatisyourname" in command:
        return (True, "Jarvis")
    
    if "whoareyou" in command:
        return (True, "Jarvis, Your Assistant Sir!")

    if "howareyou" in command:
        return (True, "Pretty Well")

    if "goodmorning" in command:
        if datetime.datetime.now().strftime("%p") == "AM":
            return (True, "Good Morning sir")
        else:
            return (True, "Are You sure its morning")
    
    if "goodafternoon" in command:
        if datetime.datetime.now().strftime("%p") == "PM":
            hour = int(datetime.datetime.now().strftime("%I"))
            if hour < 4:
                return (True, "Good afternoon sir")
            elif hour < 7:
                return (True, "evening suits the time better" )
            else:
                return (True, "are you sure its afternoon")
        else:
            return (True, "Are You sure its afternoon")
            
    if "goodevening" in command:
        if datetime.datetime.now().strftime("%p") == "PM":
            hour = int(datetime.datetime.now().strftime("%I"))
            if hour > 4 and hour < 8:
                return (True, "Good evening sir")
            elif hour > 8:
                return (True, "its more like night time" )
            else:
                return (True, "are you sure its evening")
        else:
            return (True, "Are You sure its evening")

    if "goodnight" in command:
        if datetime.datetime.now().strftime("%p") == "PM":
            hour = int(datetime.datetime.now().strftime("%I"))
            if hour > 6 and hour < 1:
                return (True, "Good night sir")
            elif hour > 1:
                return (True, "better go get sleep sir" )
            else:
                return (True,"are you sure its night")
        else:
            return (True, "Are You sure its night")

    if "good" in command or "like" in command:
        return (True, "You Made My Day")

    if "canyou" in command:
        return (False, "Sorry to disappoint, Unfortunately I can't")

    if "whatis" in command:
        query_to_search = real_command.lower()
        query_to_search = query_to_search.replace("wikipedia", "")
        query_to_search = query_to_search.replace("wiki", "")
        query_to_search = query_to_search.replace("search", "")
        query_to_search = query_to_search.replace("for", "")
        try:
            return (True,"According to wikipidea," + wiki.summary(title=query_to_search, sentences=2, auto_suggest=False))
        except:
            return (True,"According to wikipidea," + wiki.summary(title=query_to_search, sentences=2, auto_suggest=True))
        else:
            return (False, "Couldn't search wikipidea")

    if "whois" in command or "whowas" in command:
        query_to_search = real_command.lower()
        query_to_search = query_to_search.replace("wikipedia", "")
        query_to_search = query_to_search.replace("wiki", "")
        query_to_search = query_to_search.replace("search", "")
        query_to_search = query_to_search.replace("for", "")
        try:
            return (True,"According to wikipidea," + wiki.summary(title=query_to_search, sentences=2, auto_suggest=False))
        except:
            return (True,"According to wikipidea," + wiki.summary(title=query_to_search, sentences=2, auto_suggest=True))
        else:
            return (False, "Couldn't search wikipedia")

    if "hi" in command:
        return (True, "Hi ,good to see you")

    if "hello" in command:
        return (True, "Hi ,good to see you")

    
    return (False, "Sorry, I can't help you with that!")

if __name__ == "__main__":
    query = recognize()
    print(query)
    result = execute_command(query)
    speak(result)   
