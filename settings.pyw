import pygame as pg
import pygame_gui as pgui
import pygame.freetype
import pyttsx3 as ps
import speech_recognition as sr
from tkinter import *
from tkinter.filedialog import askdirectory
import os
from os import environ
import json
import subprocess as s
from ctypes import windll
user32 = windll.user32

# Main Function
def main():
    pg.freetype.init()
    medium_font = pg.freetype.Font("file/Basic-Regular.ttf", 18)
    small_font = pg.freetype.Font("file/Basic-Regular.ttf", 16)
    large_font = pg.freetype.Font("file/Basic-Regular.ttf", 40)

    def show_text(font, window, pos, text, color):
        font.render_to(window, pos, text, color)

    # Intialize pygame Window
    pg.init()
    scr_width, scr_height = 350, 580 + 70
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # Intialize pygame Window
    environ['SDL_VIDEO_WINDOW_POS'] = str(((screensize[0]-scr_width)//2))+",0"
    win = pg.display.set_mode((scr_width, scr_height))
    pg.display.set_caption("Settings")

    # Variables
    speak = ps.init('sapi5')
    voices = speak.getProperty('voices')
    voice_names = [voice.name for voice in voices]
    musicDir = os.path.join(os.path.expanduser("~"), "Music")
    languages = ["en-us", "en-In"]
    microphone_names = []
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        microphone_names.append(name)
    microphone_names.append('Default')
    from assitant import default_settings


    try:
        with open('file/config.txt', 'r') as f:
            settings = json.loads(f.readline().replace("'", '"'))
    except:
        with open('file/config.txt', 'w') as f:
            f.writelines(str(default_settings))
            settings = default_settings

    # Creating UI Elements
    if settings['theme'] == 'light':
        manager = pgui.UIManager((scr_width, scr_height), 'file/light_theme.json')#
        color = (255, 255, 255)
        font_color = (0, 0, 0)
        bar_color = (0, 0, 0)
    else:
        manager = pgui.UIManager((scr_width, scr_height), 'file/dark_theme.json')
        color = (0, 0, 0)
        font_color = (255, 255, 255)
        bar_color = (128, 128, 128)
    # theme_slct = pgui.elements.UISelectionList(relative_rect=pg.Rect(0, 0, 350, 47), item_list=[('Dark Theme', 'dark'), ('Light Theme', 'light')], manager=manager, allow_double_clicks=True, starting_height=1)
    quit_btn = pgui.elements.UIButton(relative_rect=pg.Rect(315, 40, 30, 30), text="X", manager=manager, object_id="quit_btn")
    theme_slct = pgui.elements.UIDropDownMenu(relative_rect=pg.Rect(0, 185 + 70, 350, 30), starting_option='Light Theme' if settings['theme'] == 'light' else 'Dark Theme', options_list=["Dark Theme", "Light Theme"], object_id="theme_slct", manager=manager)
    voice_menu = pgui.elements.UIDropDownMenu(relative_rect=pg.Rect(0, 130 + 70, 350, 30), options_list=voice_names, manager=manager, object_id='voice_menu', starting_option=voice_names[settings['voice']])
    lang_menu = pgui.elements.UIDropDownMenu(relative_rect=pg.Rect(0, 75 + 70, 175, 30), options_list=languages, manager=manager, object_id='lang_menu', starting_option=settings['language'])
    pos_names = ['Normal', 'At Bottom', 'On Top']
    if settings['pos'] == 'none':
        start_value_pos = 0
    elif settings['pos'] == 'bottom':
        start_value_pos = 1
    else:
        start_value_pos = 2
    pos_menu = pgui.elements.UIDropDownMenu(relative_rect=pg.Rect(175, 75 + 70, 175, 30), options_list=pos_names, manager=manager, object_id='pos_menu', starting_option=pos_names[start_value_pos])
    voice_rate_scroller = pgui.elements.UIHorizontalSlider(relative_rect=pg.Rect(0,20 + 70, 350, 30), start_value=settings['rate'], value_range=(100, 400), manager=manager, object_id="rate_scroller")
    musicDir_textbox = pgui.elements.UITextEntryLine(relative_rect=pg.Rect(0, 240 + 70, 320, 30), manager=manager, object_id='music_dir_textbox')
    musicDir_textbox.set_text(settings['music dir'])
    musicDir_browse = pgui.elements.UIButton(relative_rect=pg.Rect(320, 240 + 70, 30, 30), text="...", manager=manager, object_id="musicDir_browse")
    microphone_menu = pgui.elements.UIDropDownMenu(relative_rect=pg.Rect(0, 295 + 70, 350, 30), options_list=microphone_names, starting_option="Default", manager=manager, object_id="microphone_menu")
    apply_button = pgui.elements.UIButton(relative_rect=pg.Rect(0, 340 + 70, 350, 30), text="Apply", manager=manager, object_id="apply_btn")
    terminal_command_key_textbox = pgui.elements.UITextEntryLine(relative_rect=pg.Rect(0, 440 + 70, 100, 30), manager=manager, object_id='terminal_command_key_textbox')
    terminal_command_value_textbox = pgui.elements.UITextEntryLine(relative_rect=pg.Rect(105, 440 + 70, 195, 30), manager=manager, object_id='terminal_command_value_textbox')
    terminal_command_add = pgui.elements.UIButton(relative_rect=pg.Rect(305, 440 + 70, 45, 30), manager=manager, object_id='terminal_command_add', text="Add")
    launch_command_key_textbox = pgui.elements.UITextEntryLine(relative_rect=pg.Rect(0, 540 + 70, 100, 30), manager=manager, object_id='launch_command_key_textbox')
    launch_command_value_textbox = pgui.elements.UITextEntryLine(relative_rect=pg.Rect(105, 540 + 70, 195, 30), manager=manager, object_id='launch_command_value_textbox')
    launch_command_add = pgui.elements.UIButton(relative_rect=pg.Rect(305, 540 + 70, 45, 30), manager=manager, object_id='launch_command_add', text="Add")
    # command_textbox = pgui.elements.UITextEntryLine(relative_rect=pg.Rect(5, 2.5, 200, 30), manager=manager, object_id="command_textbox")
    # exec_button = pgui.elements.UIButton(relative_rect=pg.Rect(206, 2.5, 35, 29.5), text="E", manager=manager)
    # mic_button = pgui.elements.UIButton(relative_rect=pg.Rect(241.5, 2.5, 35, 29.5), text="M", manager=manager)
    # close_button = pgui.elements.UIButton(relative_rect=pg.Rect(276, 2.5, 35, 29.5), text="X", manager=manager)

    def redraw_ui():
        win.fill(color)
        pg.draw.rect(win, bar_color, (0, 30, 350, 10))
        show_text(medium_font, win, (5, 5 + 70), 'Voice Rate :', font_color)
        show_text(medium_font, win, (100, 5 + 70), str(voice_rate_scroller.get_current_value()), font_color)
        show_text(medium_font, win, (5, 55 + 70), 'Language :', font_color)
        show_text(medium_font, win, (180, 55 + 70), 'Position :', font_color)
        show_text(medium_font, win, (5, 110 + 70), 'Voice :', font_color)
        show_text(medium_font, win, (5, 165 + 70), 'Theme :', font_color)
        show_text(medium_font, win, (5, 220 + 70), 'Music Directory :', font_color)
        show_text(medium_font, win, (5, 275 + 70), 'Microphone :', font_color)
        pg.draw.rect(win, bar_color, (0, 380 + 70, 350, 10))
        show_text(medium_font, win, (5, 400 + 70), 'Terminal Command :', font_color)
        show_text(medium_font, win, (5, 420 + 70), 'Key', font_color)
        show_text(medium_font, win, (105, 420 + 70), 'Value', font_color)
        pg.draw.rect(win, bar_color, (0, 480 + 70, 350, 10))
        show_text(medium_font, win, (5, 500 + 70), 'Launch Command :', font_color)
        show_text(medium_font, win, (5, 520 + 70), 'Key', font_color)
        show_text(medium_font, win, (105, 520 + 70), 'Value', font_color)
        manager.draw_ui(win)
        pg.display.update()

    # Declaring Variables
    clock = pg.time.Clock()
    run = True

    def killProcess(pid):
        s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)

    # Main Loop
    while run:
        time_delta = clock.tick(20)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
                break

            if event.type == pg.USEREVENT:
                if event.user_type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_object_id == "rate_scroller":
                        settings['rate'] = event.value

                if event.user_type == pgui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_object_id == "lang_menu":
                        settings['language'] = event.text

                    if event.ui_object_id == "voice_menu":
                        for index, voice in enumerate(voices):
                            if voice.name == event.text:
                                settings['voice'] = index

                    if event.ui_object_id == "theme_slct":
                        if event.text == "Dark Theme":
                            settings['theme'] = "dark"
                        elif event.text == "Light Theme":
                            settings['theme'] = "light"

                    if event.ui_object_id == "microphone_menu":
                        if event.text == "Default":
                            settings['microphone'] = 'default'
                        for index, mic in enumerate(sr.Microphone.list_microphone_names()):
                            if mic == event.text:
                                settings['microphone'] = index

                    if event.ui_object_id == "pos_menu":
                        if event.text == "On Top":
                            settings['pos'] = "top"
                        elif event.text == "At Bottom":
                            settings['pos'] = "bottom"
                        elif event.text == "Normal":
                            settings['pos'] = "none"

                if event.user_type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "quit_btn":
                        run = False
                        break
                    if event.ui_object_id == 'musicDir_browse':
                        tkinter_window = Tk()
                        tkinter_window.withdraw()
                        filename = askdirectory(title="Music Directory")

                        if filename:
                            name = filename[:]
                            musicDir_textbox.set_text(name)
                
                    if event.ui_object_id == 'apply_btn':
                        settings['music dir'] == musicDir_textbox.text
                        print(settings)
                        with open('file/config.txt', 'w') as f:
                            f.writelines(str(settings))

                        with open('file/pid.txt', 'r') as f:
                            pid = int(f.read())

                        killProcess(pid)
                        os.startfile(__file__.replace('settings.pyw', 'main.pyw'))
                        os.startfile(__file__)
                        exit()

                    if event.ui_object_id == 'terminal_command_add':
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
                        
                        if terminal_command_key_textbox.text.strip() != '' and terminal_command_value_textbox.text.strip():
                            runCommands[terminal_command_key_textbox.text] = terminal_command_value_textbox.text
                            try:
                                x[1] = runCommands
                            except:
                                try:
                                    x = [openCommands, runCommands]
                                except:
                                    x = [{}, runCommands]
                            with open('file/commands.txt', 'w') as f:
                                f.writelines(str(line) for line in x)
                        terminal_command_key_textbox.set_text('')
                        terminal_command_value_textbox.set_text('')
                    
                    if event.ui_object_id == 'launch_command_add':
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
                        
                        if launch_command_key_textbox.text.strip() != '' and launch_command_value_textbox.text.strip():
                            openCommands[launch_command_key_textbox.text] = launch_command_value_textbox.text#.replace('"', '')
                            try:
                                x[0] = openCommands
                            except:
                                try:
                                    x = [openCommands, runCommands]
                                except:
                                    x = [openCommands, {}]
                            with open('file/commands.txt', 'w') as f:
                                f.write(str(x[0]) + '\n' + str(x[1]))
                        launch_command_key_textbox.set_text('')
                        launch_command_value_textbox.set_text('')

            manager.process_events(event)
        redraw_ui()
        manager.update(time_delta)


if __name__ == "__main__":
    main()