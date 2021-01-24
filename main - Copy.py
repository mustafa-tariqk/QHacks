from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.list import ImageRightWidget
from kivy.uix.boxlayout import BoxLayout
import json

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import emotion_display
import text_analysis

# Global variables
HOST = ''
PORT = 33000
NAME = ''
client_socket = socket(AF_INET, SOCK_STREAM)
BUFSIZ = 1024


class TwoLineAvatarIconListItemAligned(TwoLineAvatarIconListItem):
    """
    Basically OneLineAvatarIconListItem but this time with alignment
    """

    def __init__(self, halign, **kwargs):
        super(TwoLineAvatarIconListItem, self).__init__(**kwargs)
        self.ids._lbl_primary.halign = halign
        self.ids._lbl_secondary.halign = self.ids._lbl_primary.halign


class Tab(FloatLayout, MDTabsBase):
    """Class implementing content for a tab."""
    pass


class AppLayout(Screen):
    global NAME
    global BUFSIZ, client_socket, HOST, PORT, NAME

    def receive(self):

        """Handles receiving of messages."""
        while True:
            msg = ''
            print("Receiving")
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")

                if msg is not None:
                    try:
                        incoming_msg = msg.split(':')
                        if incoming_msg[0] != NAME:
                            self.new_message(incoming_msg[1], "profile_pic\Moose.png", name=incoming_msg[0])
                    except:
                        self.new_message(msg, "profile_pic\Ammar.png")

            except OSError:  # Possibly client has left the chat.
                print("broken")
                break

    def on_pre_enter(self, *args):
        global BUFSIZ, client_socket, HOST, PORT, NAME

        # Ping username to server
        client_socket.send(bytes(NAME, "utf8"))

        # Start receiving messages
        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def send_message(self, image_name):
        """
        Has to be done here to let kivy access the function
        """
        message = self.ids.msg_field.text
        message+=emotion_display.main(message)
        message+= "          "


        # Sends the message from the app
        client_socket.send(bytes(self.ids.msg_field.text, "utf8"))

        # Reset text field
        self.ids.msg_field.text = ''
        new_message = TwoLineAvatarIconListItemAligned(text=message, secondary_text=NAME + "          ", halign='right')
        new_message.add_widget(ImageRightWidget(source=image_name))

        self.ids.msg_list.add_widget(new_message)

    def new_message(self, message, image_name, name='Server'):
        """
        Compose a message to showcase in the app
        """
        new_message = TwoLineAvatarIconListItemAligned(text=message, secondary_text=name, halign='left')
        new_message.add_widget(ImageLeftWidget(source=image_name))
        self.ids.msg_list.add_widget(new_message)


class SignInServer(Screen):
    def sign_in(self):
        global HOST, PORT
        HOST = self.ids.host_field.text
        PORT = self.ids.port_field.text

        # ----Now comes the sockets part----
        if not HOST:
            HOST = 'localhost'
        else:
            HOST = int(PORT)

        if not PORT:
            PORT = 33000
        else:
            PORT = int(PORT)

        ADDR = (HOST, PORT)

        client_socket.connect(ADDR)


class SignIn(Screen):
    def validate_login(self):
        global NAME
        with open("sign_in_details.json", 'r') as f:
            sign_in_dict = json.load(f)

        if self.ids.username_field.text not in sign_in_dict.keys():
            self.ids.username_field.hint_text = "This is not a valid username"
            #self.ids.username_field.line_color_normal = "Red"

        else:
            if self.ids.password_field.text == sign_in_dict[self.ids.username_field.text]["password"]:
                self.manager.current = "signin"
                NAME = sign_in_dict[self.ids.username_field.text]["name"]

            else:
                self.ids.password_field.hint_text = "This is not a valid password"
                #self.ids.password_field.line_color_normal = "Red"


class MainApp(MDApp):
    global NAME

    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignIn(name='password'))
        sm.add_widget(SignInServer(name='signin'))
        sm.add_widget(AppLayout(name='app'))

        return sm

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        """Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """

        pass

MainApp().run()  # Starts GUI execution.
