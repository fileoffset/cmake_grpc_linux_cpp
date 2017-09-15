#!/usr/bin/env python2
import math, random
import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line, Ellipse
from kivy.core.window import Window 

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

class Cell:
    def __init__(self, layer, rect, i, j):
        self.layer = layer
        self.rect = rect
        self.i = i
        self.j = j

class Quadrant:
    def __init__(self, layer, rect, x_ratio, y_ratio):
        self.layer = layer
        self.rect = rect
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio

        # now we have a rectangle for our layer, split it into quadrants based on the ratio args
        xStep = rect.size[0] / x_ratio
        yStep = rect.size[1] / y_ratio

        self.cells = [ Cell(layer, Rect(rect.pos[0] + (i * xStep), rect.pos[1] + (j * yStep), xStep, yStep), i, j) for i in range(x_ratio) for j in range(y_ratio) ]


class RectProjection:
    def __init__(self, rect_src, rect_dest, layers, x_ratio, y_ratio):
        self.rect_src=rect_src
        self.rect_dest=rect_dest
        self.layers=layers
        self.quadrants = [ self.getQuadrantForLayer(layer, x_ratio, y_ratio) for layer in range(self.layers - 1, -1, -1) ]
        
    def getQuadrantForLayer(self, layer, x_ratio, y_ratio):
        rect_src = self.rect_src
        rect_dest = self.rect_dest

        if layer == 0:
            rect = rect_src
        elif layer == self.layers - 1:
            rect = rect_dest
        else:
            # project top left corner of src -> dest
            theta = math.atan((rect_dest.y - rect_src.y) / (rect_dest.x - rect_src.x))
            hyp = (((rect_dest.y - rect_src.y) / math.sin(theta)) / (self.layers - 1)) * layer
            x = rect_src.x + (math.cos(theta) * hyp)
            y = rect_src.y + (math.sin(theta) * hyp)
            
            # project bottom right corner of src -> dest
            theta = math.atan((rect_src.top - rect_dest.top) / (rect_src.right - rect_dest.right))
            hyp = (((rect_src.top - rect_dest.top) / math.sin(theta)) / (self.layers - 1)) * layer
            width = rect_src.right - (math.cos(theta) * hyp) - x
            height = rect_src.top - (math.sin(theta) * hyp) - y 
                
            rect = Rect(x, y, width, height)

#       print(rect)
        return Quadrant(layer, rect, x_ratio, y_ratio)

    def getCells(self):
        return [ c for q in self.quadrants for c in q.cells ]

class Level:
    COLORS = [
        Color(1, 0, 1),
        Color(0, 1, 1),
        Color(.2, 1, 0),
        Color(1, .5, 0),
        Color(.5, 0, 1), 
    ]

    DIFFICULTY = {
        1 : {
            'playable' : 3,
            'colors' : 3,
            'speed' : 10,
        }
    }

    def __init__(self, difficulty=1):
        self.difficulty = Level.DIFFICULTY[difficulty]

    def __getattr__(self, item):
        if item == 'playable':
            return self.difficulty[item]
        elif item == 'colors':
            return self.difficulty[item]
        elif item == 'speed':
            return self.difficulty[item]

    def getRandomColor(self):
        return Level.COLORS[random.randint(0, self.difficulty['colors'] - 1)]

class Captive:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def getDrawables(self):
        return [ self.color, Ellipse(pos=self.rect.pos, size=self.rect.size) ]

class PlayerSupply:
    def __init__(self, x, y, width, height, level, canvas, player, onSelected=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.canvas = canvas
        self.player = player
        self.selected = False
        self.onSelected = onSelected
        
    def init(self, rects):
        self.rects = rects
        self.captives = [ Captive(rect=Rect.Scale(rect, 0.8), color=self.level.getRandomColor()) for rect in self.rects ] 
        self.playableCaptives = self.captives[-self.level.playable:]

        self.__addToCanvas()

    def __addToCanvas(self):
        self.canvas.add(Color(1, 1, 1))

        for rect in self.rects:
            self.canvas.add(Line(rectangle=(rect.pos[0], rect.pos[1], rect.size[0], rect.size[1])))

        self.canvas.add(Color(1, 1, 0))

        for captive in self.playableCaptives:
            self.canvas.add(captive.rect)

        for captive in self.captives:
            for drawable in captive.getDrawables():
                self.canvas.add(drawable)

    def update(self, dt):
        pass

    def select(self, captive):
        if self.selected:
            return self.deselect(captive)

        self.selected = captive
        self.canvas.add(Color(1, 0, 0))
        self.canvas.add(Line(rectangle=(captive.rect.pos[0], captive.rect.pos[1], captive.rect.size[0], captive.rect.size[1])))

        if self.onSelected:
            self.onSelected(self, self.selected)

    def deselect(self, captive):
        self.canvas.add(Color(1, 1, 1))
        self.canvas.add(Line(rectangle=(self.selected.rect.pos[0], self.selected.rect.pos[1], self.selected.rect.size[0], self.selected.rect.size[1])))
        self.selected = None

    def on_touch_down(self, touch):
        # see if we pressed on any captives in the supply
        for captive in self.playableCaptives:
            if captive.rect.contains(touch.pos):
                return self.select(captive)


class GameBoard:
    X_RATIO = 10
    Y_RATIO = 8

    def __init__(self, x, y, width, height, canvas, get_next_captive=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas = canvas
        self.getSelectedCaptive = get_next_captive
        self.projection = RectProjection(rect_src=Rect(self.x, self.y, self.width, self.height), 
                                         rect_dest=Rect(self.x + 100, self.y + 50, self.width - 200, self.height - 100), 
                                         layers=3,
                                         x_ratio=GameBoard.X_RATIO,
                                         y_ratio=GameBoard.Y_RATIO)
        self.captives = {}

        self.__addToCanvas()

    def __addToCanvas(self):
        colors = [
            Color(1, 0, 0),
            Color(0, 1, 0),
            Color(0, 0, 1),
            Color(.5, .5, .5),
        ]

        for cell in self.projection.getCells():
            captive = self.getCaptive(cell.i, cell.j)

            if captive:
                print('captive: %r' % captive)
                self.canvas.add(captive.color)
            else:
                print('cell.layer: %r' % cell.layer)
                self.canvas.add(colors[cell.layer])

            self.canvas.add(Line(rectangle=(cell.rect.pos[0], cell.rect.pos[1], cell.rect.size[0], cell.rect.size[1])))

    def update(self, dt):
        pass

    def getCaptive(self, i, j):
        return self.captives.get(i, {}).get(j, None)

    def setCaptive(self, x, y, captive):
        self.captives.setdefault(i, {}).setdefault(j, None)
        self.captives[i][j] = captive

    def on_touch_down(self, touch):
        captive = self.getSelectedCaptive()

        if not captive:
            return

        # see if we pressed on any rects in the projection, start with the uppermost layer
        for level in range(self.projection.layers):
            # work out if the touch is inside any of the rects in this layer
            quadrant = self.projection.getQuadrantForLayer(level)
            cell = quadrant.getCellAtPoint(pos[0], pos[1])

            if cell:
                if not self.getCaptive(cell.x, cell.y):
                    self.setCaptive(cell, captive)
                else:
                    return

class CaptiveGame(Widget):
    def init(self):
        xRatio = 10
        yRatio = 8
        xStep = Window.width / xRatio
        yStep = Window.height / yRatio
        self.selected = None
        self.level = Level()
        self.player1 = PlayerSupply(x=0, y=0, width=Window.width, height=Window.height, level=self.level, canvas=self.canvas, player=1)
        self.player2 = PlayerSupply(x=0, y=0, width=Window.width, height=Window.height, level=self.level, canvas=self.canvas, player=2)
        self.gameBoard = GameBoard(x=xStep, y=yStep, width=Window.width - (2 * xStep), height=Window.height - (2 * yStep), canvas=self.canvas, get_next_captive=self.getSelected)

        self.childs = [ self.player1, self.player2, self.gameBoard ]

        self.player1.init(rects=[ Rect(0, i * yStep, xStep, yStep) for i in range(1, yRatio) ] +
                                [ Rect(i * xStep, 0, xStep, yStep) for i in range(0, int(xRatio / 2)) ])
        self.player2.init(rects=[ Rect(xStep * (xRatio - 1), i * yStep, xStep, yStep) for i in range(1, yRatio) ] +
                                [ Rect((i) * xStep, 0, xStep, yStep) for i in range(xRatio - 1, int(xRatio / 2) - 1, -1) ])
#
    def update(self, dt):
        for c in self.childs:
            c.update(dt)

    def getSelected(self):
        return self.selected

    def on_touch_down(self, touch):
        print(touch)
        # if any children want to ack handling of the event, just return True
        for c in self.childs:
            if c.on_touch_down(touch):
                return

    def on_player_supply_selected(self, instance, captive):
        self.selected = (instance, captive)

class CaptiveApp(App):
    def build(self):
        game = CaptiveGame()
        game.init()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    CaptiveApp().run()
