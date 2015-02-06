import kivy 
#import ipdb
import sys

import time
import os
import json

from subprocess import call


from kivy.app import App
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Ellipse, Line
from kivy.utils import get_color_from_hex
from random import randint
from kivy.config import Config

import gtk
import ipdb
import feedparser

# ----------- Global objects -------------


MAX_ELEMENTS_X = 1
SCREEN_WIDTH = gtk.gdk.screen_width() 
SCREEN_HEIGHT = gtk.gdk.screen_height()
WINDOW_HEIGHT = SCREEN_HEIGHT
WINDOW_WIDTH = SCREEN_WIDTH/3
ELEMENT_WIDTH = WINDOW_WIDTH/MAX_ELEMENTS_X
ELEMENT_HEIGHT = 100
MAX_ELEMENTS_Y = int(WINDOW_HEIGHT/ELEMENT_HEIGHT)

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', 0)
Config.set('graphics', 'left', SCREEN_WIDTH - WINDOW_WIDTH)
Config.set('graphics', 'height', SCREEN_HEIGHT)
Config.set('graphics', 'width', WINDOW_WIDTH)
Config.write()


# ----------- Functions ------------------


# ----------- Classes --------------------

class Element(Button):
    def __init__(self, **kwargs):
        super(Element, self).__init__(**kwargs)
        for key, value in kwargs.iteritems():      # styles is a regular dictionary
            if key == "feed":
                self.feed = value
        self.width = ELEMENT_WIDTH
        self.height = ELEMENT_HEIGHT
        self.bind(size=self.setter('text_size'))

        def callback(self):
            print(self.feed["link"])
            call(["firefox", self.feed["link"]])

        self.bind(on_press=callback)



class GUI(Widget):
    #this is the main widget that contains the game. 
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        args = {}
        self.elements = []
        self.update(args)

    def update(self, args):
        #This update function is the main update function for the game
        #All of the game logic has its origin here 
        #events are setup here as well
        # everything here is executed every 60th of a second.
        print "Fetching feed"
        self.feed = feedparser.parse('http://www.theguardian.com/uk/rss')
        # self.feed = feedparser.parse('http://www.reddit.com/r/python/.rss')
        print "Feed fetched."
        for elem in self.elements:
            self.remove_widget(elem)
        self.render_feed()

    def render_feed(self):
        for i,item in enumerate(self.feed["entries"]):
            if i < 7:
                str = word_wrap(item["title"],35)
                elem = Element(text=str, font_name="assets/Montserrat-Bold.ttf", feed=self.feed["entries"][i])
                elem.x = Window.width/2 - elem.width/2
                elem.y = SCREEN_HEIGHT - 100 - (ELEMENT_HEIGHT * i)
                self.elements.append(elem)
                self.add_widget(elem)

class HeadlinesApp(App):
    def build(self):
        Window.set_title("Headlines")
        parent = Widget()
        app = GUI()
        Clock.schedule_interval(app.update, 60) 
        parent.add_widget(app)
        return parent

def word_wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

if __name__ == '__main__' :
    HeadlinesApp().run()