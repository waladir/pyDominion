import sys
import os

import pygame
from pygame.locals import *
#import pygame_menu

import time

from libs.classes.game import Game
from libs.classes.player import Player
from libs.classes.card import Card

from libs.expansions import expansions
from libs.cards import cards

pygame.init()
FPS = 30
FramePerSec = pygame.time.Clock()
pygame.display.set_caption('pyDominion')

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN.fill(pygame.Color(0, 0, 0))

# def create_game_dialog():
#     global main_menu
#     global SCREEN
#     err = False
   
#     input_data = main_menu.get_input_data()
#     if 'players_name' not in input_data or len(input_data['players_name']) < 3:
#         err = True
#         err_menu = pygame_menu.Menu('pyDominion', 600, 200, theme=pygame_menu.themes.THEME_DARK)
#         err_menu.add.label(title = 'Jméno hráče musí mít alespoň 3 znaky!')
#         err_menu.add.button('OK', pygame_menu.events.EXIT)
#         err_menu.mainloop(SCREEN) 
        
#     if not err:  
#         players_count = int(input_data['players_count'][0][1])
#         player_name = input_data['players_name']
#         player = Player(name = player_name, index = 1)
#         testplayer = Player(name = 'PLAYER2', index = 2)
#         players = [player, testplayer]

#         game = Game(2, players, 'Dominion')
#         main_menu.toggle()
#         SCREEN.fill((40, 0, 40))

def create_game():
    global SCREEN
    global game
   
    players_count = 2
    player = Player('waladir', 1)
    otherplayer = Player('PLAYER2', 2)
    players = [player, otherplayer]

    game = Game(2, players, 'Dominion')


############################ MAIN ############################

cards_set = ['Dílna', 'Obchodnice', 'Důl', 'Hradní příkop', 'Kovárna', 'Milice', 'Přestavba', 'Sklepení', 'Trh', 'Vesnice']

game = None
create_game()
game.start(SCREEN, cards_set)

while 1 == 1:
    game.switch_player = False
    game.do_round()
    while game.switch_player == False:
        # main_menu = pygame_menu.Menu('pyDominion', 400, 300, theme=pygame_menu.themes.THEME_DARK)
        # main_menu.add.text_input(title = 'Jméno hráče:  ', textinput_id = 'players_name')
        # main_menu.add.selector(title = 'Počet hráčů :  ', selector_id = 'players_count', items = [('2', 2), ('3', 3), ('4', 4)])
        # main_menu.add.button('Start', create_game)
        # main_menu.add.button('Konec', pygame_menu.events.EXIT)
        # main_menu.mainloop(SCREEN)  

        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()    
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos 
            if event.type == pygame.MOUSEBUTTONDOWN:            
                if event.button == 3:
                    x, y = event.pos 
                    game.desk.show_card_detail(x, y)
                if event.button == 1:
                    x, y = event.pos 
                    game.desk.activate_card(x, y) 
                    game.desk.action_button_click(x, y)               
        game.desk.detect_hover(x, y)   

