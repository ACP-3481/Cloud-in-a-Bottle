from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import os
from UIScreens import *



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
