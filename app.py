delay=0.1
from pynput import mouse, keyboard
from datetime import datetime, timedelta
import time
import threading
import pyautogui
import colorama

# Global variables to store the triple-click position and click times
triple_click_position = None
click_times = []
tracking_active = False  # Flag to indicate if tracking should continue

# Create a mouse controller instance
mouse_controller = mouse.Controller()

def on_click(x, y, button, pressed):
    global triple_click_position, click_times, tracking_active

    if pressed:
        # Record the time of the click
        click_times.append(datetime.now())
        
        # Keep only the last 3 click times
        click_times = click_times[-3:]
        
        # Check for triple-click (three left-clicks within 500 ms)
        if len(click_times) == 3 and (click_times[-1] - click_times[0] <= timedelta(milliseconds=500)):
            # Detected a triple-click
            triple_click_position = (x, y)
            print("\033[H\033[J")
            print(colorama.Fore.CYAN + r"""
                       _________         _________ _______ _________            _______  _______  _______ 
                       \__   __/|\     /|\__   __/(  ____ \\__   __/  |\     /|(  ___  )/ ___   )(  ____ \
                          ) (   | )   ( |   ) (   | (    \/   ) (     | )   ( || (   ) |\/   )  || (    \/
                          | |   | | _ | |   | |   | (_____    | |     | (___) || (___) |    /   )| (__    
                          | |   | |( )| |   | |   (_____  )   | |     |  ___  ||  ___  |   /   / |  __)   
                          | |   | || || |   | |         ) |   | |     | (   ) || (   ) |  /   /  | (      
                          | |   | () () |___) (___/\____) |   | |     | )   ( || )   ( | /   (_/\| (____/\
                          )_(   (_______)\_______/\_______)   )_(     |/     \||/     \|(_______/(_______/
                              Halklar hükümetlerinden korkmamalı, hükümetler halktan korkmalı.                                                          
 """)
            print(colorama.Fore.YELLOW + 'codded by TwistHaze on GitHub')
            print(f'Triple-click detected at X: {x} Y: {y}')
            print(colorama.Fore.RED + 'Right-click to stop auto-clicker.')
            tracking_active = True  # Start auto-clicker
            click_times.clear()  # Clear click times to avoid multiple detections
        
        # Check for right-click to stop auto-clicker
        if button == mouse.Button.right and tracking_active:
            tracking_active = False  # Stop auto-clicker
            print('Right-click detected. Stopping auto-clicker.')
            print("\n")
            #clearn terminal text
            print("\033[H\033[J")
            print('1. Left-click three times to find the position & start auto-clicker.')
            print('2. Right-click to stop auto-clicker.')

def on_release(key):
    global tracking_active

    if key == keyboard.Key.ctrl_c:
        print('Position tracking stopped by user.')
        return False  # Stop listener
    elif key == keyboard.Key.esc:
        tracking_active = False  # Stop auto-clicker if ESC key is pressed

def mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def keyboard_listener():
    with keyboard.Listener(on_release=on_release) as key_listener:
        key_listener.join()

def main():
    global tracking_active, triple_click_position

    print(colorama.Fore.CYAN + r"""
                       _________         _________ _______ _________            _______  _______  _______ 
                       \__   __/|\     /|\__   __/(  ____ \\__   __/  |\     /|(  ___  )/ ___   )(  ____ \
                          ) (   | )   ( |   ) (   | (    \/   ) (     | )   ( || (   ) |\/   )  || (    \/
                          | |   | | _ | |   | |   | (_____    | |     | (___) || (___) |    /   )| (__    
                          | |   | |( )| |   | |   (_____  )   | |     |  ___  ||  ___  |   /   / |  __)   
                          | |   | || || |   | |         ) |   | |     | (   ) || (   ) |  /   /  | (      
                          | |   | () () |___) (___/\____) |   | |     | )   ( || )   ( | /   (_/\| (____/\
                          )_(   (_______)\_______/\_______)   )_(     |/     \||/     \|(_______/(_______/
                              Halklar hükümetlerinden korkmamalı, hükümetler halktan korkmalı.                                                          
 """)
    print(colorama.Fore.YELLOW + '                       Contact Me?')
    print(colorama.Fore.YELLOW + '     Discord: 404wg    -----------    Instagram 404wg     ')
    print('')
    print(colorama.Fore.RED + '1. Left-click three times to find the position & start auto-clicker.')
    print(colorama.Fore.RED + '2. Right-click to stop auto-clicker.')

    mouse_thread = threading.Thread(target=mouse_listener)
    keyboard_thread = threading.Thread(target=keyboard_listener)

    mouse_thread.start()
    keyboard_thread.start()

    try:
        while True:
            # Get current mouse position using pyautogui
            x, y = pyautogui.position()

            # Check if triple-click was detected
            if triple_click_position is not None:
                tx, ty = triple_click_position
                # print(f'OLD Triple-click detected at X: {tx} Y: {ty}')

                # Start auto-clicker loop until right-click detected or tracking_active is False
                while tracking_active:
                    # print(f'Auto-clicking at X: {tx} Y: {ty}')
                    mouse_controller.position = (tx, ty)
                    mouse_controller.click(mouse.Button.left, 1)
                    time.sleep(delay)  # Adjust delay between clicks as needed
            
            time.sleep(delay)  # Reduce CPU usage while waiting for events

    except KeyboardInterrupt:
        print('Position tracking stopped.')

    mouse_thread.join()
    keyboard_thread.join()

if __name__ == "__main__":
    main()
