from PostMessage_Wrapper import *

"""
A little note from me (Loui2). PostMessage()/SendMessage() may seem like overkill, however 
the reason I use it is because it allows you to interact with applications WITHOUT 
the application having to be focused!

Meaning Gtuner can be minimized and you can still execute a script via a PostMessage()/SendMessage() left click!
"""

def execute_script():
    # Coordinate may need to be adjusted. 
    # Use Spy++ (VS 2017 tool) > Monitor Gtuner messages > Click on Gtuner script execution play button and see the coordinates of the click message
    messenger.post_left_click(569, 39) 
    
if __name__ == '__main__':
    messenger = AppMessenger('Gtuner.exe') # Sets up the process for messaging
    
    if len(messenger.hwnd) > 0:
        print(messenger.app_name, "process was found!", "PostMessage Wrapper Initialized.")
    else:
        print(messenger.app_name, "process was not found. Please run", messenger.app_name, "and restart the script.")