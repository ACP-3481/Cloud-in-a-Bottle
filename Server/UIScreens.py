from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField
import os
from kivy.properties import StringProperty
from Server import get_internal_ip, check_port
import public_ip as ip
import socket
import threading

i_ip = get_internal_ip()
e_ip = ip.get()
i_port = None
e_port = None
destination_folder = ""
config = {
}
class SetupScreen(Screen):
    dialog = None
    def on_press_default_button(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Default Setup not implemented yet",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release= lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()


class DefaultSetup(Screen):
    pass


class DialogContent(MDBoxLayout):
    pass

class FolderSelectionScreen(Screen):
    dialog=None
    def __init__(self, **kwargs):
        super(FolderSelectionScreen, self).__init__(**kwargs)
        self.layout = MDFloatLayout()

        self.title = MDLabel(text="Choose a Folder to Store Cloud Storage Files", pos_hint={'center_x': 0.5,'center_y': 0.9}, width=self.width, halign='center', font_style='H4')
        self.layout.add_widget(self.title)

        # Create a button to open the file manager
        self.file_manager_button = MDRaisedButton(text="Select Folder", on_release=lambda _: self.show_file_manager(), pos_hint={'center_x': 0.5,'center_y': 0.8})
        self.layout.add_widget(self.file_manager_button)

        # Create a label to display the selected folder path
        self.folder_path_label = MDLabel(text="No folder selected yet", pos_hint={'center_x': 0.5,'center_y': 0.5}, width=self.width, halign='center')
        self.layout.add_widget(self.folder_path_label)

        # Create a button to go to the next screen
        self.next_button = MDRaisedButton(text="Next", on_release=self.go_to_next_screen, disabled=True, pos_hint={'center_x': 0.5,'center_y': 0.2})
        self.layout.add_widget(self.next_button)

        self.add_widget(self.layout)

    def show_file_manager(self, *args):
        # Create a file manager instance
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_folder_path,
        )
        self.file_manager.add_widget(
            MDIconButton(
                icon="folder-plus",
                on_press=lambda _: self.show_dialog()
            )
                
        )
        if len(args) == 0:
            self.file_manager.show(os.getcwd().replace('\\', '/'))  # Start the file manager at the root directory
        else:
            self.file_manager.show(args[0])
    

    def dialog_ok(self):
        folder_name = self.dialog.content_cls.ids.folder_name_field.text
        folder_path = self.file_manager.current_path + "/" + folder_name
        os.mkdir(folder_path)
        self.exit_file_manager()
        self.show_file_manager(folder_path)
        self.dialog.dismiss()
        

    def show_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Dialog Title",
                type="custom",
                content_cls=DialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release= lambda _: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", on_release= lambda _: self.dialog_ok()
                    ),
                ],
            )
        self.dialog.open()
    

    def select_folder_path(self, path):
        # Update the folder path label with the selected path
        self.folder_path_label.text = f"Selected folder: {path}"

        # Enable the "Next" button
        self.next_button.disabled = False

        self.exit_file_manager()

    def exit_file_manager(self, *args):
        # Close the file manager
        self.file_manager.close()

    def go_to_next_screen(self, *args):
        # Get a reference to the screen manager
        screen_manager = self.parent

        # Find the index of this screen in the screen manager
        self_index = screen_manager.screens.index(self)

        # Go to the next screen in the screen manager
        screen_manager.current = screen_manager.screens[self_index + 1].name

class CustomSetup(Screen):
    internal_ip = StringProperty()
    external_ip = StringProperty()
    internal_ip = f"Internal IP: {i_ip}"
    external_ip = f"External IP: {e_ip}"
    dialog = None

    def on_press_manual_config(self):
        print("hello")
        internal_port = self.ids.i_port_input.text
        external_port = self.ids.e_port_input.text
        if not internal_port.isnumeric() or not external_port.isnumeric():
            self.show_alert_dialog("Port values must be numbers")
            return
        global i_port
        global e_port
        i_port = int(internal_port)
        e_port = int(external_port)
        self.manager.current = 'port_forwarding'

    def on_press_upnp_button(self):
        self.show_alert_dialog("Upnp not implemented yet")

    def show_alert_dialog(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release= lambda _: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()

class PortForwardingScreen(Screen):
    pass

class PortForwardingInfoScreen(Screen):
    pass

class PortForwardingStepOneScreen(Screen):
    pass

class PortForwardingStepTwoScreen(Screen):
    pass

class PortForwardingStepThreeScreen(Screen):
    pass

class PortForwardingStepFourScreen(Screen):
    pass

class PortForwardingStepFiveScreen(Screen):
    pass

def handle_client_connection(client_socket):
    while True:
        # Receive data from the client
        request = client_socket.recv(1024)
        if not request:
            break
        # Do something with the data
        response = 'You sent: {}'.format(request.decode())
        # Send a response back to the client
        client_socket.send(response.encode())
    # Close the socket connection
    client_socket.close()

thread_open = False
def accept_connections():
    global thread_open
    thread_open = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((i_ip, i_port))

    # Set a timeout on the socket object before calling accept()
    server_socket.settimeout(10.0)  # Timeout of 5 seconds

    # Listen for incoming connections
    server_socket.listen()
    while True:
        if not thread_open:
            break
        try:
            # Wait for a client connection with timeout
            client_socket, client_address = server_socket.accept()
            print('Accepted connection from {}:{}'.format(client_address[0], client_address[1]))
            # Start a new thread to handle the connection
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
            client_thread.start()
        except socket.timeout:
            print('Socket timed out waiting for client connections.')
            # Continue waiting for new connections
            continue

accept_thread = threading.Thread(target=accept_connections)
class PortForwardingCheckScreen(Screen):
    port_status = StringProperty()
    def on_enter(self, *args):
        global thread_open
        global port_status
        accept_thread.start()
        port_open = check_port(e_ip, e_port)
        if not port_open:
            thread_open = False
        port_status = f"{i_ip} {e_ip}"
        return super().on_pre_enter(*args)

class MenuScreen(Screen):
    pass
