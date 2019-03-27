# Loui2's wrapper for placing messages in message queues of application.
import win32con, win32api, win32gui, win32process, psutil, time


class AppMessenger():
    def __init__(self, process_name=None):
        self.app_name = process_name  # Name of target process
        self.process_list = []  # List of processes with name self.app_name
        self.pid = None     # Pid of target HWND
        self.hwnd = []  # Target HWND's
        self.hwnd_children = []  # HWND of target process windows (childs)
        self.hwnd_children_classname = []  # Class names of target process HWND windows
        self.process_childs = []  # list of lists of self.hwnd_children & self.hwnd_children_classname
        if process_name is not None:
            self.get_process_list(process_name)

    def get_process_list(self, name=None, setup=True):
        """ Gets a list of processes running with the name
        pre: name is a string representing the process name
        post: returns a list of processes"""
        if len(self.process_list) > 0:  # Reinitialize for new process
            self.__init__(None)

        self.process_list = [item for item in psutil.process_iter() if item.name() == name]
        if len(self.process_list) == 1 and setup:  # One process found
            self.one_process_setup()
        else:
            return self.process_list

    def get_process_pid(self, process=None):
        """ Gets the pid of a process from the process list
        pre: process is an element of self.process_list (or any process list)
        post: returns a integer representing pid """
        if process is None:  # Sets default parameters (for when client does not specify parameter(s))
            process = self.process_list[0]

        self.pid = process.pid
        return self.pid

    def get_process_hwnd(self, pid=None):
        """ Gets HWND of pid
        pre: pid is an integer representing the processes PID
        post: returns a list of HWND """
        if pid is None:  # Sets default parameters (for when client does not specify parameter(s))
            pid = self.pid

        self.hwnd = []
        win32gui.EnumWindows(self._enum_window_callback, pid)
        return self.hwnd

    def get_hwnd_children(self, hwnd=None):
        """ Gets the "windows" inside a process
        """
        HWND = hwnd
        if HWND is None:  # Sets default parameters (for when client does not specify parameter(s))
            HWND = self.hwnd[0]

        win32gui.EnumChildWindows(HWND, self._enum_child_windows_callback, None)
        return self.hwnd_children

    def get_hwnd_children_classname(self, hwnd=None):
        HWND = hwnd
        if HWND is None:  # Sets default parameters (for when client does not specify parameter(s))
            HWND = self.hwnd[0]

        win32gui.EnumChildWindows(HWND, self._enum_child_windows_classname_callback, None)
        return self.hwnd_children_classname

    def get_hwnd_title(self, hwnd_list=None):
        """ Gets the titles (captions) of a hwnd list
        pre: hwnd_list is a list of HWND
        post: returns a list of titles (captions)
        """
        if hwnd_list is None:  # Sets default parameters (for when client does not specify parameter(s))
            hwnd_list = self.hwnd

        return [win32gui.GetWindowText(item) for item in hwnd_list]

    def post_message(self, HWND=None, WM_KEYDOWN=None, WPARAM=None, LPARAM=None):
        """Good old PostMessage"""
        hwnd = HWND
        if hwnd is None:  # Sets default parameters (for when client does not specify parameter(s))
            hwnd = self.hwnd[0]

        win32gui.PostMessage(hwnd, WM_KEYDOWN, WPARAM, LPARAM)

    def send_message(self, HWND=None, WM_KEYDOWN=None, WPARAM=None, LPARAM=None):
        """Good old SendMessage"""
        hwnd = HWND
        if hwnd is None:  # Sets default parameters (for when client does not specify parameter(s))
            hwnd = self.hwnd[0]
        win32gui.PostMessage(hwnd, WM_KEYDOWN, WPARAM, LPARAM)

    def _enum_window_callback(self, hwnd, pid):
        """ Helper function of self.get_hwnd
        This function is used in the first parameter of win32gui.EnumWindows()
        """
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid == current_pid and win32gui.IsWindowVisible(hwnd):
            self.hwnd.append(hwnd)

    def _enum_child_windows_callback(self, hwnd, param):
        self.hwnd_children.append(hwnd)
        return True

    def _enum_child_windows_classname_callback(self, hwnd, param):
        name = win32gui.GetClassName(hwnd)
        self.hwnd_children_classname.append(name)
        return True

    def one_process_setup(self, process=None):
        """ Takes a target process and retrieves everything needed for messaging."""
        if process is None:  # Sets default parameters (for when client does not specify parameter(s))
            process_to_setup = self.process_list[0]
        else:
            process_to_setup = process

        self.pid = self.get_process_pid(process_to_setup)
        pid = self.pid
        self.hwnd = self.get_process_hwnd(pid)
        hwnd = self.hwnd[0]
        try:
            self.hwnd_children = self.get_hwnd_children(hwnd)
            self.hwnd_children_classname = self.get_hwnd_children_classname(hwnd)
        except:
           # print("An error occurred getting child windows. There may not be any child windows for this process.")
            pass

    def get_current_process_childs(self):  # TODO: Allow a string with process name to be passed.
        """ Gets the current targets child windows"""
        if self.app_name is None:
            print("No process to get children window from. "
                  "Please use self.get_process_lists() or pass process name as string parameter for class.")
            return None
        else:
            childs = []  # List of child windows
            for i in range(0, len(self.hwnd_children)):
                temp_combined = list()
                # Create a list containing an HWND and its classname
                temp_combined.append(self.hwnd_children_classname[i])
                temp_combined.append((self.hwnd_children[i]))
                # Append the list to our childs list
                childs.append(temp_combined)
            self.process_childs = childs
            return self.process_childs

    def help(self):
        """TODO: Displays help information"""
        pass

# ----------------------------------------
#   Extra Features
# ----------------------------------------
    def post_key(self, key=win32con.VK_RETURN, hwnd=None):
        """ Uses PostMessage to send a key"""
        HWND = hwnd
        if HWND is None:
            HWND = self.hwnd[0]
        win32gui.PostMessage(HWND, win32con.WM_KEYDOWN, key, 0)
        win32gui.PostMessage(HWND, win32con.WM_KEYUP, key, 0)

    def post_write(self, string=None, hwnd=None):
        """ TODO: Uses PostMessage to write"""
        HWND = hwnd
        if HWND is None:
            HWND = self.hwnd[0]
        pass

    def post_left_click(self, x=0, y=0, hwnd=None):
        """ Uses PostMessage to send a click to a coordinate"""
        HWND = hwnd
        if HWND is None:
            HWND = self.hwnd[0]

        win32gui.PostMessage(HWND, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        win32gui.PostMessage(HWND, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))