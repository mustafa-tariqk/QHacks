from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.list import ImageRightWidget
from kivy.uix.boxlayout import BoxLayout

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


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


class AppLayout(BoxLayout):
    global NAME

    def send_message(self, image_name):
        """
        Has to be done here to let kivy access the function
        """
        message = self.ids.msg_field.text + "          "
        # Sends the message from the app
        client_socket.send(bytes(self.ids.msg_field.text, "utf8"))

        # Reset text field
        self.ids.msg_field.text = ''
        new_message = TwoLineAvatarIconListItemAligned(text=message, secondary_text=NAME+"          ", halign='right')
        new_message.add_widget(ImageRightWidget(source=image_name))

        self.ids.msg_list.add_widget(new_message)


class MainApp(MDApp):
    global NAME

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

    def build(self):
        return AppLayout()

    def on_start(self):
        # Ping username to server
        client_socket.send(bytes(NAME, "utf8"))
        # Set Colors
        self.theme_cls.primary_palette = 'Cyan'

        # Start receiving messages
        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def new_message(self, message, image_name, name='Server'):
        new_message = TwoLineAvatarIconListItemAligned(text=message, secondary_text=name, halign='left')
        new_message.add_widget(ImageLeftWidget(source=image_name))
        self.root.ids.msg_list.add_widget(new_message)

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


# ----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
NAME = input('Enter Name: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

MainApp().run()  # Starts GUI execution.
