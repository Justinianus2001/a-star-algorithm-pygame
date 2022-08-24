#!/usr/bin/env python3
import os
try:
    import pygame
except ImportError:
    os.system('start cmd /c pip3 install pygame')
    import pygame
from a_star import AStar
import py_compile

def setup():
    py_compile.compile('main.py')

if __name__ == '__main__':
    setup()
    game = AStar()
    game.init()
    game.run()
