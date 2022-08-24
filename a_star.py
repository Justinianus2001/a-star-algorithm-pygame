from color import Color
from cell import Cell
import copy
import math
import os
import pygame
import random
import sys

class AStar:
    width = 1360
    height = 680
    cell = 10
    find_running = False
    running = True
    FPS = 60
    open_set = []
    close_set = []
    move_x = [-1, -1, -1, 0, 0, 1, 1, 1]
    move_y = [-1, 0, 1, -1, 1, -1, 0, 1]
    #move_x = [-1, 0, 0, 1]
    #move_y = [0, -1, 1, 0]
    path = []
    start_time = None

    def __init__(self):
        from pygame import mixer
        self.pygame = pygame
        self.mixer = mixer

    def init(self):
        self.init_pygame()
        self.init_setting()
        self.init_arena()

    def init_pygame(self):
        self.pygame.init()
        self.pygame.display.set_caption('Pygame A* Algorithm')
        self.size = (self.width, self.height)
        self.screen = self.pygame.display.set_mode(self.size, self.pygame.FULLSCREEN)
        self.clock = self.pygame.time.Clock()

    def init_setting(self):
        self.play_ico  = self.pygame.transform.scale(self.pygame.image.load(os.getcwd() + '/icon/play.ico') , (50, 50))
        self.pause_ico = self.pygame.transform.scale(self.pygame.image.load(os.getcwd() + '/icon/pause.ico'), (50, 50))
        self.exit_ico  = self.pygame.transform.scale(self.pygame.image.load(os.getcwd() + '/icon/exit.ico') , (50, 50))
        self.clear_ico = self.pygame.transform.scale(self.pygame.image.load(os.getcwd() + '/icon/clear.ico'), (50, 50))
        self.font      = self.pygame.font.SysFont('sans', 50)
        self.title     = self.font.render('Time:', True, Color.BLACK)

    def init_arena(self):
        self.table = [[Cell(row, col, random.randint(0, 10) <= 5) for col in range(self.width // self.cell)] for row in range(self.height // self.cell)]
        for col in range(self.width // self.cell):
            for row in range(self.height // self.cell):
                self.table[row][col].add_neighbor(self.height // self.cell, self.width // self.cell, self.table)
        self.table[0][0].isObstacle = False
        self.table[67][135].isObstacle = False

    def get_a_star_heuristic(self, current, end):
        return abs(current.x - end.x) + abs(current.y - end.y)
        #return max(abs(current.x - end.x), abs(current.y - end.y))
        #return math.sqrt((current.x - end.x)**2 + (current.y - end.y)**2)

    def update_arena(self):
        current = None
        if self.find_running:
            if len(self.open_set) > 0:
                winner = 0
                for i in range(len(self.open_set)):
                    if self.open_set[i].f  < self.open_set[winner].f:
                        winner = i
                current = self.open_set[winner]
                if current == self.end:
                    self.find_running = False
                elif self.get_a_star_heuristic(current, self.end) < self.distance:
                    self.distance = self.get_a_star_heuristic(current, self.end)
                    self.save_pos = (current.x, current.y)
                del self.open_set[winner]
                self.close_set.append(current)
                for i in range(len(self.move_x)):
                    if (0 <= current.x + self.move_x[i] < self.height // self.cell
                        and 0 <= current.y + self.move_y[i] < self.width // self.cell
                        and not self.table[current.x + self.move_x[i]][current.y + self.move_y[i]].isObstacle):
                        Next = self.table[current.x + self.move_x[i]][current.y + self.move_y[i]]
                        if Next not in self.close_set:
                            temp_g = current.g + 1
                            new_path = False
                            if Next in self.open_set:
                                if temp_g < Next.g:
                                    Next.g = temp_g
                                    new_path = True
                            else:
                                Next.g = temp_g
                                new_path = True
                                self.open_set.append(Next)
                            if new_path:
                                Next.h = self.get_a_star_heuristic(Next, self.end)
                                Next.f = Next.g + Next.h
                                Next.parent = current
            else:
                near_x, near_y = self.save_pos
                current = self.table[near_x][near_y]
                self.find_running = False
        if current != None:
            self.path = []
            temp = current
            while temp != None:
                self.path.append(temp)
                temp = temp.parent
        for col in range(self.width // self.cell):
            for row in range(self.height // self.cell):
                rect = self.pygame.Rect(col * self.cell, row * self.cell, self.cell, self.cell)
                self.pygame.draw.rect(self.screen, Color.BLACK, rect, not self.table[row][col].isObstacle)
        for val in self.close_set:
            rect = self.pygame.Rect(val.y * self.cell, val.x * self.cell, self.cell, self.cell)
            self.pygame.draw.rect(self.screen, Color.RED, rect, 0)
        for val in self.open_set:
            rect = self.pygame.Rect(val.y * self.cell, val.x * self.cell, self.cell, self.cell)
            self.pygame.draw.rect(self.screen, Color.GREEN, rect, 0)
        for val in self.path:
            rect = self.pygame.Rect(val.y * self.cell, val.x * self.cell, self.cell, self.cell)
            self.pygame.draw.rect(self.screen, Color.BLUE, rect, 0)

    def run(self):
        while self.running:
            if self.start_time != None and self.find_running:
                self.title = self.font.render('Time: ' + '{:,}'.format((self.pygame.time.get_ticks() - self.start_time) / 1000) + 's', True, Color.BLACK)
            self.screen.fill(Color.GREY)
            self.update_arena()
            self.clock.tick(self.FPS)
            (mouseX, mouseY) = self.pygame.mouse.get_pos()
            for event in self.pygame.event.get():
                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if 100 < mouseX < 150 and 700 < mouseY < 750:
                            self.init_arena()
                            self.close_set = []
                            self.open_set = []
                            self.path = []
                        elif 300 < mouseX < 350 and 700 < mouseY < 750:
                            self.find_running = not self.find_running
                            if self.find_running:
                                self.start_time = self.pygame.time.get_ticks()
                            self.distance = math.inf
                            self.save_pos = (-1, -1)
                            self.start = self.table[0][0]
                            self.end = self.table[67][135]
                            self.start.isObstacle = False
                            self.end.isObstacle = False
                            self.open_set = [self.start]
                            self.close_set = []
                        elif 500 < mouseX < 550 and 700 < mouseY < 750:
                            self.running = False
            self.screen.blit(self.clear_ico, (100, 700))
            self.screen.blit(self.pause_ico if self.find_running else self.play_ico, (300, 700))
            self.screen.blit(self.exit_ico , (500, 700))
            self.screen.blit(self.title    , (630, 700))
            self.pygame.display.flip()
        self.pygame.quit()
        sys.exit()
