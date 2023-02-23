from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import public_ip as ip
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from Server import get_internal_ip, check_port
import os
from threading import Thread, Lock
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
import os


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


class FolderSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(FolderSelectionScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.title = MDLabel(text="Choose a Folder to Store Cloud Storage Files", pos_hint={'center_x': 0.5,'center_y': 0.9}, width=self.width, halign='center', font_style='H4')
        self.layout.add_widget(self.title)

        # Create a button to open the file manager
        self.file_manager_button = MDRaisedButton(text="Select Folder", on_release=self.show_file_manager, pos_hint={'center_x': 0.5,'center_y': 0.8})
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
        self.file_manager.show(os.getcwd().replace('\\', '/'))  # Start the file manager at the root directory

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
    
class PortForwardingCheckScreen(Screen):
    port_status = f"{i_ip} {e_ip}"

class MenuScreen(Screen):
    pass


def server_code():

    def receive_file(client):
        filename, filesize, size_a, size_r = client.recv(4096).decode().strip().split("|")

        with open(f"{destination_folder}{filename}", "wb") as f:
            for i in range(int(size_a)):
                bytes_read = client.recv(4096)
                f.write(bytes_read)
            bytes_read = client.recv(int(size_r))
            f.write(bytes_read)
            print("file recieved")




class CloudApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        with open(f"{os.getcwd()}\\Server\\config.txt", "r") as f:
            for line in f:
                if "=" in line:
                    config_text = line.strip().split("=")
                    config[config_text[0]] = config_text[1]
        print(config)
        sm = ScreenManager()
        if config['first_setup'] in ['True', 'true', '1', 't']:
            sm.add_widget(SetupScreen(name='setup'))
            sm.add_widget(DefaultSetup(name='defaultsetup'))
            sm.add_widget(FolderSelectionScreen(name='folder_select'))
            sm.add_widget(CustomSetup(name='customsetup'))
            sm.add_widget(PortForwardingScreen())
            sm.add_widget(PortForwardingInfoScreen())
            sm.add_widget(PortForwardingStepOneScreen())
            sm.add_widget(PortForwardingStepTwoScreen())
            sm.add_widget(PortForwardingStepThreeScreen())
            sm.add_widget(PortForwardingStepFourScreen())
            sm.add_widget(PortForwardingStepFiveScreen())
            sm.add_widget(PortForwardingCheckScreen(name="port_forwarding_check"))
        sm.add_widget(MenuScreen(name='menu'))

        return sm
    
    


if __name__ == '__main__':
    CloudApp().run()
