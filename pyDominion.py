import sys
import os

import pygame
from pygame.locals import *
import pygame_menu

import time
import json

import debug

from libs.classes.game import Game
from libs.classes.player import Player
from libs.classes.card import Card

from libs import expansions
from libs.api import call_api
from libs.events import get_events
from libs import cards_set_builder
from libs import cards_sets

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd
from libs.library.Seaside import Seaside

pygame.init()
FPS = 30
FramePerSec = pygame.time.Clock()
pygame.display.set_caption('pyDominion')

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN.fill(pygame.Color(0, 0, 0))

def do_game():
    x = 0
    y = 0
    last_ts = 0
    global game

    while 1 == 1:
        ts = int(time.time())             
        if ts-last_ts > 1:
            get_events(game.get_me())
            last_ts = ts
        for event in pygame.event.get():
            game.check_events(event)
            if event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                if game.desk.select_area == True:
                    game.desk.select_area_offset = game.desk.select_area_offset + 1                        
                    if game.desk.select_area_offset + game.desk.select_area_count > len(game.desk.select_area_piles):
                        game.desk.select_area_offset = len(game.desk.select_area_piles) - game.desk.select_area_count
                    game.desk.changed.append('select_area')
                else:
                    game.desk.players_hand_offset = game.desk.players_hand_offset + 1                        
                    if game.desk.players_hand_offset + game.desk.players_hand_count > len(game.desk.player.hand):
                        game.desk.players_hand_offset = len(game.desk.player.hand) - game.desk.players_hand_count
                    game.desk.changed.append('players_hand')
                game.desk.draw()
            if event.type == pygame.KEYDOWN and event.key == K_LEFT:
                if game.desk.select_area == True:
                    game.desk.select_area_offset = game.desk.select_area_offset - 1                        
                    if game.desk.select_area_offset < 0:
                        game.desk.select_area_offset = 0
                    game.desk.changed.append('select_area')                        
                else:
                    game.desk.players_hand_offset = game.desk.players_hand_offset - 1
                    if game.desk.players_hand_offset < 0:
                        game.desk.players_hand_offset = 0
                    game.desk.changed.append('players_hand')
                game.desk.draw()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos 
            if event.type == pygame.MOUSEBUTTONDOWN:            
                if event.button == 3:
                    x, y = event.pos 
                    game.desk.show_card_detail(x, y)
                if event.button == 1:
                    x, y = event.pos 
                    game.desk.click_on_pile(x, y) 
                    game.desk.action_button_click(x, y)               
                    game.desk.click_on_info(x, y) 
        game.desk.detect_hover(x, y)  
        if game.state == 'end' :
            player = game.desk.player
            if len(player.results) == game.players_count:
                game.players_count = -1
                player.results = sorted(player.results, key=lambda d: d['points'], reverse = True)
                game.desk.changed.append('results')
                game.desk.draw()

def choose_cards_set():
    global main_menu
    global cards_set
    global game
    input_data = main_menu.get_input_data()
    selected_set = input_data['cards_set'][0][1]
    sets = cards_sets.cards_sets
    for set in sets:
        for set_name in set:
            if set_name == selected_set:
                cards_set = set[set_name]['cards']
    create_game_select_cards()    
    
def select_cards_set():
    global SCREEN
    global main_menu
    global selected_expansions
    sets = cards_sets.cards_sets
    items = []
    for cards_set in sets:
        match = 0
        for set_name in cards_set:
            for expansion in selected_expansions:
                if expansion in cards_set[set_name]['expansions']:
                    match = match + 1
            if match == len(cards_set[set_name]['expansions']):
                items.append((set_name, set_name))
    main_menu = pygame_menu.Menu('pyDominion', 600, 400, theme=pygame_menu.themes.THEME_DARK)
    if len(items) > 0:
        main_menu.add.selector(title = 'Sada karet :  ', selector_id = 'cards_set', items = items)
    main_menu.add.button('Vybrat', choose_cards_set)
    main_menu.add.button('Vlastní sada karet', create_game_select_cards)
    main_menu.add.button('Konec', pygame_menu.events.EXIT)
    main_menu.mainloop(SCREEN)  

def choose_expansions():
    global main_menu
    global selected_expansions

    input_data = main_menu.get_input_data()
    for expansion in input_data:
        if input_data[expansion] == True:
            selected_expansions.append(expansion)
    select_cards_set()

def select_expansions():
    global SCREEN
    global main_menu
    global selected_expansions

    selected_expansions = []

    main_menu = pygame_menu.Menu('pyDominion', 500, 400, theme=pygame_menu.themes.THEME_DARK)
    available_expansions = expansions.expansions
    for expansion in available_expansions:
        if available_expansions[expansion]['enabled'] == True:
            main_menu.add.toggle_switch(title = available_expansions[expansion]['name'], default = available_expansions[expansion]['default_state'], state_text = ('Vyp', 'Zap'), toggleswitch_id = expansion)
    main_menu.add.button('Vybrat', choose_expansions)
    main_menu.add.button('Konec', pygame_menu.events.EXIT)
    main_menu.mainloop(SCREEN)  


def create_game_select_cards():
    global SCREEN
    global game
    global selected_expansions
    global cards_set

    sorted_cards = {}
    cards = {}
    selected_cards = None

    if 'cards_set' in globals() and len(cards_set) == 10:
        selected_cards = cards_set

    for expansion in selected_expansions:
        expansion_cards = globals()[expansion].get_cards(kingdom_card = True)
        cards = {**cards, **expansion_cards}    

    sorted_card_names = sorted(cards, key=lambda x: cards[x]['price'])
    for card_name in sorted_card_names:
        sorted_cards.update({ card_name :cards[card_name] })
    cards_set = cards_set_builder.select_cards_to_cards_set(SCREEN, sorted_cards, selected_cards)
    create_game()    

def start_game():
    global SCREEN
    global game
    global selected_expansions
    global cards_set

    players = []
    input_data = main_menu.get_input_data()
    players = []
    data = call_api({ 'function' : 'create_game', 'name' : input_data['game_name'], 'player' : input_data['players_name'], 'players_count' : int(input_data['players_count'][0][1]), 'expansions' : json.dumps(selected_expansions), 'cards_set' : json.dumps(cards_set) })
    player = Player(input_data['players_name'], 1)
    players.append(player)
    game = Game(data['id'], int(input_data['players_count'][0][1]), players, selected_expansions)
    game.create(SCREEN, cards_set)
    do_game()    

def join_game():
    global main_menu
    global SCREEN
    global game

    input_data = main_menu.get_input_data()
    game_id = input_data['game'][0][1]
    data = call_api({ 'function' : 'join_game', 'id' : game_id, 'player' : input_data['players_name'] })    
    idx = 1
    players = []
    for player_name in data['players']:
        player = Player(player_name, idx)
        idx = idx + 1
        players.append(player)
    me = player_name
    game = Game(data['id'], int(data['players_count']), players, data['expansions'])
    game.join_game(SCREEN, data['cards_set'], 1, me)
    do_game()

def list_games():
    global SCREEN
    global main_menu
    games = []
    main_menu = pygame_menu.Menu('pyDominion', 600, 300, theme=pygame_menu.themes.THEME_DARK)
    data = call_api({ 'function' : 'list_games' })
    for game in data:
        games.append((game['name'], game['id']))
    if len(games) == 0:
        main_menu.add.label(title = 'Není založená žádna hra,')
        main_menu.add.label(title = 'ke které se lze připojit')
        main_menu.add.button('Vytvořit hru', select_expansions)
        main_menu.add.button('Konec', pygame_menu.events.EXIT)
        main_menu.mainloop(SCREEN)  
    else:
        main_menu.add.text_input(title = 'Jméno hráče:  ', textinput_id = 'players_name')
        main_menu.add.selector(title = 'Hra :  ', selector_id = 'game', items = games)
        main_menu.add.button('Připojit se', join_game)
        main_menu.add.button('Konec', pygame_menu.events.EXIT)
        main_menu.mainloop(SCREEN)  

def create_game():
    global SCREEN
    global main_menu
    main_menu = pygame_menu.Menu('pyDominion', 500, 400, theme=pygame_menu.themes.THEME_DARK)
    main_menu.add.text_input(title = 'Jméno hráče:  ', textinput_id = 'players_name')
    main_menu.add.text_input(title = 'Jméno hry:  ', textinput_id = 'game_name')
    main_menu.add.selector(title = 'Počet hráčů :  ', selector_id = 'players_count', items = [('2', 2), ('3', 3), ('4', 4)])
    main_menu.add.button('Vytvořit', start_game)
    main_menu.add.button('Konec', pygame_menu.events.EXIT)
    main_menu.mainloop(SCREEN)  

def setup():
    global SCREEN
    global main_menu
    main_menu = pygame_menu.Menu('pyDominion', 400, 300, theme=pygame_menu.themes.THEME_DARK)
    main_menu.add.button('Vytvořit hru', select_expansions)
    main_menu.add.button('Připojit se ke hře', list_games)
    main_menu.add.button('Konec', pygame_menu.events.EXIT)
    main_menu.mainloop(SCREEN) 

def setup_test():
    global SCREEN
    global game
    expansions = ['Dominion','Intrigue', 'Seaside']

#    cards_set = ['Artisan', 'Cellar', 'Market', 'Merchant', 'Mine', 'Moat', 'Moneylender', 'Poacher', 'Remodel', 'Witch']
    cards_set = ['Workshop', 'Woodcutter', 'Mine', 'Moat', 'Smithy', 'Militia', 'Remodel', 'Cellar', 'Market', 'Village']
    if debug.test_attack_cards == True:
        if debug.creator == True:
            players = []
            data = call_api({ 'function' : 'create_game', 'name' : 'test1', 'player' : 'waladir1', 'players_count' : 2, 'expansions' : json.dumps(expansions), 'cards_set' : json.dumps(cards_set) })
            player = Player('waladir1', 1)
        else:
            data = call_api({ 'function' : 'list_games' })
            for game in data:
                if game['name'] == 'test1':
                    game_id = game['id']
            data = call_api({ 'function' : 'join_game', 'id' : game_id, 'player' : 'waladir2' })    
            idx = 1
            players = []
            for player_name in data['players']:
                player = Player(player_name, idx)
                idx = idx + 1
                players.append(player)
            me = player_name
            game = Game(data['id'], int(data['players_count']), players, data['expansions'])
            game.join_game(SCREEN, data['cards_set'], int(data['round']), me)
            do_game()
    else:
        players = []
        data = call_api({ 'function' : 'create_game', 'name' : 'test1', 'player' : 'waladir', 'players_count' : 2, 'expansions' : json.dumps(expansions), 'cards_set' : json.dumps(cards_set) })
        player = Player('waladir', 1)
    players.append(player)
    game = Game(data['id'], 2, players, expansions)
    game.create(SCREEN, cards_set)
    do_game()

############################ MAIN ############################
if debug.test_cards == False and debug.test_attack_cards == False:
    setup()    
else:
    setup_test()

