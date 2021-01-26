# Imports
import pygame as pg
import pygame.freetype
import pygame_gui as pgui
import win32gui
import win32con
from pynput.keyboard import Key, Listener
import pynput
from os import environ
from assitant import *
from ctypes import windll
from threading import Thread
# from time import sleep

user32 = windll.user32
pid = os.getpid()
with open('file/pid.txt', 'w') as f:
    f.write(str(pid))

status_color = (0, 0, 0)

# Main Function
def main():
    pg.freetype.init()
    medium_font = pg.freetype.Font("file/Basic-Regular.ttf", 18)
    small_font = pg.freetype.Font("file/Basic-Regular.ttf", 16)
    large_font = pg.freetype.Font("file/Basic-Regular.ttf", 40)
    
    
    def show_text(font, window, pos, text, color):
        font.render_to(window, pos, text, color)

    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    scr_width, scr_height = 323, 30
    # Intialize pygame Window
    environ['SDL_VIDEO_WINDOW_POS'] = str(((screensize[0]-scr_width)//2))+",0"
    pg.init()
    win = pg.display.set_mode((scr_width, scr_height), pg.NOFRAME)

    # Creating UI Elements
    if settings['theme'] == 'light':
        manager = pgui.UIManager((scr_width, scr_height), 'file/light_theme.json')
        color = (255, 255, 255)
    else:
        manager = pgui.UIManager((scr_width, scr_height), 'file/dark_theme.json')
        color = (0, 0, 0)
    command_textbox = pgui.elements.UITextEntryLine(relative_rect=pg.Rect(5, int(2.5), 200, 30), manager=manager, object_id="command_textbox")
    exec_button = pgui.elements.UIButton(relative_rect=pg.Rect(206, int(2.5), 35, int(29.5)), text="E", manager=manager)
    mic_button = pgui.elements.UIButton(relative_rect=pg.Rect(int(241.5), int(2.5), 35, int(29.5)), text="M", manager=manager)
    close_button = pgui.elements.UIButton(relative_rect=pg.Rect(276, int(2.5), 35, int(29.5)), text="X", manager=manager)

    # Pin Window to top
    hwnd = win32gui.GetForegroundWindow()
    if settings['pos'] == "top":
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600, 300, 0, 0, win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)
    
    # Declaring Variables
    clock = pg.time.Clock()
    run = True

    # Function to draw window
    def redraw_ui():
        win.fill(color)
        pg.draw.circle(win, status_color, (316, 15), 5)
        manager.draw_ui(win)
        pg.display.update()

    # Function to show status
    def show_status(color):
        global status_color
        status_color = color
        pg.draw.circle(win, color, (316, 15), 5)
        pg.display.update()
    def exec_cmd(cmd):
        command_textbox.set_text('')
        print("Processing...")
        show_status((255, 255, 0))
        status = execute_command(cmd)
        if status[0] == True:
            if status[1] == "successful":
                speak("here you go")
                show_status((0, 255, 0))
            else:
                speak(status[1])
                show_status((0, 255, 0))
        elif status[0] == False:
            speak(status[1])
            show_status((255, 0, 0))
    def on_press(key):
        if not(run):
            return False
        pass
    
    def on_release(key):
        if not(run):
            return False
        if key == Key.alt_gr:
            try:
                # speak("Yes sir!")
                show_status((0, 0, 255))
                exec_cmd(recognize())
            except Exception as e:
                print(e)
                speak("Couldn't access Microphone!")
    def activate_on_keypress():
        with Listener(on_press=on_press, on_release=on_release) as listener:
	        listener.join()

    activate = Thread(target=activate_on_keypress)
    activate.daemon = True
    activate.start()

    # Main Loop
    while run:
        if settings['pos'] == "bottom":
            win32gui.SetWindowPos(hwnd, 1, 600, 300, 0, 0, win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)
        time_delta = clock.tick(20)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # run = False
                # break
                pass
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    exec_cmd(command_textbox.text)
                if event.key == pg.K_TAB:
                    try:
                        # speak("Yes sir!")
                        show_status((0, 0, 255))
                        exec_cmd(recognize())
                    except Exception as e:
                        print(e)
                        speak("Couldn't access Microphone!")

                if event.key == pg.K_ESCAPE:
                    run = False
                    break
            elif event.type == pg.USEREVENT:
                if event.user_type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_element == close_button:
                        run = False
                        break
                    elif event.ui_element == exec_button:
                        exec_cmd(command_textbox.text)
                    elif event.ui_element == mic_button:
                        try:
                            # speak("Yes sir!")
                            show_status((0, 0, 255))
                            exec_cmd(recognize())
                        except Exception as e:
                            print(e)
                            speak("Couldn't access Microphone!")
                        
                    

            manager.process_events(event)
        redraw_ui()
        manager.update(time_delta)



if __name__ == '__main__':
    main()