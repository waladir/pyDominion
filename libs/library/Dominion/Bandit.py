import sys
import time
import pygame
from pygame.locals import *

from libs.classes.card import Card

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd

from libs.events import get_events, create_event

class Bandit(Card):
    def __init__(self):
        self.id = 'bandit'
        self.name = 'Bandita' 
        self.name_en = 'Bandit'
        self.expansion = 'Dominion'
        self.image = 'Bandit.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 5
        self.value = 0

        self.subphase = ''
        self.select_to_choose = []
        self.card_to_choose = None
        self.cards_data = {}

    def get_class(self, card_name):
        for expansion in self.game.expansions:
            cards = globals()[expansion].get_cards()
            if card_name in cards:
                return globals()[expansion].get_class(card_name)
        return None        

    def do_action(self):
        self.action.check_reaction()
        if self.action.bonuses == True:
            self.action.bonuses = False        
            piles = self.desk.basic_piles
            for pile in piles:
                card = pile.top_card()
                if card.name == 'Zlaťák':
                    card = pile.get_top_card()
                    if card is not None:
                        self.player.put_card_to_discard(card)
            self.desk.changed.append('basic')                    
            self.desk.changed.append('players_discard') 
            self.desk.draw()                   
        self.action.do_attack()
        self.action.cleanup()        
        self.desk.changed.append('info')
        self.desk.draw()

    def do_attacked(self):
        if self.action.phase != 'select':
            cards = self.player.get_cards_from_deck(2)
            for card in cards:
                if card is not None:
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                    if 'treasure' in card.type and card.name != 'Měďák':
                        create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                        self.desk.trash.add_card(card)
                    else:                            
                        create_event(self.player.game.get_me(), 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                        self.player.put_card_to_discard(card) 
            self.desk.changed.append('trash')
            self.desk.changed.append('players_discard')
            self.desk.draw()
            self.player.phase = 'wait'
            self.player.game.switch_player = True
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'card_name' : self.name_en }, self.player.game.get_other_players_names())


