#!/usr/bin/env python2
import math, random, sys, argparse, grpc
import generated.game_pb2_grpc as game_rpc
import generated.game_pb2 as game_pb2

# everything kivy
import kivy
kivy.require('1.1.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line, Ellipse
from kivy.core.window import Window 
from kivy.uix.button import Button

def DEBUG(s):
    print(s)

class Rect(Rectangle):
    def __init__(self, x, y, width, height):
        Rectangle.__init__(self, pos=(x, y), size=(width, height))

    def __getattr__(self, item):
        if item == 'x':
            return self.pos[0]
        elif item == 'y':
            return self.pos[1]
        elif item == 'width':
            return self.size[0]
        elif item == 'height':
            return self.size[1]
        elif item == 'right':
            return self.pos[0] + self.size[0]
        elif item == 'top':
            return self.pos[1] + self.size[1]

        raise AttributeError(self, "Couldn't find attribute: %r" % item)
#       return Rectangle.__getattr__(self, item)

    def __setattr__(self, item, value):
        if item == 'x':
            self.pos[0] = value
        elif item == 'y':
            self.pos[1] = value
        elif item == 'width':
            self.size[0] = value
        elif item == 'height':
            self.size[1] = value
        elif item == 'right':
            self.size[0] = value - self.pos[0]
        elif item == 'top':
            self.size[1] = value - self.pos[1]

        return Rectangle.__setattr__(self, item, value)

    def __str__(self):
        return 'Rect[%r, %r]' % (self.pos, self.size)

    def contains(self, pos):
        return self.x <= pos[0] <= self.right and self.y <= pos[1] <= self.top

    @staticmethod
    def Scale(rect, percent):
        wdiff = rect.width * (1 - percent)
        hdiff = rect.height * (1 - percent)
        return Rect(rect.x + (wdiff / 2), rect.y + (hdiff / 2), rect.width * percent, rect.height * percent)

class Level:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty

    def __getattr__(self, item):
        if self.difficulty and item in ('speed'):
            return self.difficulty[item]

class Player:
    def __init__(self, x, y, width, height, level, canvas, player):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.canvas = canvas
        self.player = player
        
    def update(self, dt):
        pass

    def on_touch_down(self, touch):
        pass

class GameBoard:
    def __init__(self, x, y, width, height, canvas):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas = canvas

    def update(self, dt):
        pass

    def on_touch_down(self, touch):
        pass

class CaptiveGame(Widget):
    def __init__(self):
        Widget.__init__(self)
        
        # setup config from command line args
        parser = argparse.ArgumentParser(description='Test Game Client')
        parser.add_argument('server_host', metavar='host', type=str, help='server host', default='127.0.0.1')
        parser.add_argument('server_port', metavar='port', type=int, help='server port', default='50051')

        args = parser.parse_args()

        if not args.server_host or not args.server_port:
            args.print_help()   
            sys.exit(1)

        self.host = args.server_host
        self.port = args.server_port      
        
        self.init()

    def init(self):
        DEBUG('Connecting to server [%s:%s]' % (self.host, self.port))

        # grab the minimum config from argv
        self._Channel = grpc.insecure_channel('%s:%s' % (self.host, self.port))
        self._Stub = game_rpc.GameServiceStub(self._Channel)
    
        # setup the default objects that we are going to pass updates to later
        self.__initLevels()
        self.__initPlayers()

        self.updatees = []

        self.canvas.add(Color(1,1,1))

        # we need the list of levels from the server to start
        self.getLevelList()

    def build(self):
        # return a Button() as a root widget
        return Button(text='hello world')

    def __initLevels(self, levels = []):
        self._Levels = levels

    def __initPlayers(self, players = []):
        self._Players = players

    def update(self, dt):
        for c in self.updatees:
            c.update(dt)

    def on_touch_down(self, touch):
        print(touch)
        # if any children want to swallow the event, they can return True
        for c in self.updatees:
            if c.on_touch_down(touch):
                return

    def getLevelList(self):
        # ask the server for level list, and wait for response
        action = game_pb2.Action()
        action.get_levels.SetInParent()
        action.get_levels.client_version = '1.0'
        print('Action: %r' % action)
        reply = self._Stub.DoAction(action)
        if reply:
            print('Reply: %r' % reply)

class CaptiveApp(App):
    def build(self):
        game = CaptiveGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game
        #return Button(text='hello world')

if __name__ == '__main__':
    CaptiveApp().run()
