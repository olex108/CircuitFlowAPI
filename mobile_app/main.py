from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import random

class MainApp(App):
    def build(self):
        img = Image(
            source='images/lamp.png',
            size_hint=(None, None),
            size=(0.5, 0.5)
        )

        return img




        # layout = GridLayout(
        #     cols=2,
        #     rows=2,
        #     row_force_default=True,
        #     row_default_height=40,
        # )
        # layout.add_widget(Button(text='Hello World!'))
        # layout.add_widget(Button(text='Hello World!!'))
        # layout.add_widget(Button(text='Hello World!!'))
        # # layout.add_widget(Button(text='Hello World!!'))
        # return layout



        # layout = BoxLayout(
        #     padding=20,
        #     orientation='vertical'
        # )
        #
        # colors = ["red", "green", "blue", "yellow"]
        #
        # for i in range(4):
        #     btn = Button(
        #         text=str(i),
        #         size_hint=(1, 1),
        #         background_color=random.choice(colors)
        #     )
        #     layout.add_widget(btn)
        # return layout

        # label = Label(text="Планета LUXARY Electricity",
        #               size_hint=(1, 1),
        #               pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #               )
        # return label


if __name__ == '__main__':
    MainApp().run()