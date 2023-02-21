from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import public_ip as ip
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from Server import get_internal_ip
import os


class SetupScreen(Screen):
    pass


class DefaultSetup(Screen):
    pass


class CustomSetup(Screen):
    internal_ip = StringProperty()
    external_ip = StringProperty()
    internal_ip = f"Internal IP: {get_internal_ip()}"
    external_ip = f"External IP: {ip.get()}"
    dialog = None

    def on_press_manual_config(self):
        print("hello")
        i_port = self.ids.i_port_input.text
        e_port = self.ids.e_port_input.text
        if not i_port.isnumeric() or not e_port.isnumeric():
            self.show_alert_dialog()

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Port values must be numbers",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release= lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()
    

class MenuScreen(Screen):
    pass


config = {
}


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
            sm.add_widget(CustomSetup(name='customsetup'))
        sm.add_widget(MenuScreen(name='menu'))

        return sm
    
    


if __name__ == '__main__':
    CloudApp().run()
