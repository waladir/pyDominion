import sys
import time
import pygame
from pygame.locals import *

from libs.classes.card import Card

class Militia(Card):
    def __init__(self):
        self.id = 'militia'
        self.name = 'Milice' 
        self.name_en = 'Militia'
        self.expansion = 'Dominion'
        self.image = 'Militia.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
        self.value = 0

    def do_action(self):
        self.action.check_reaction()

        if self.action.bonuses == True:
            self.action.bonuses = False   
            self.player.treasure = self.player.treasure + 2
            self.desk.changed.append('info')
            self.desk.draw()

        self.action.do_attack()
        self.action.cleanup()        
        self.desk.changed.append('info')
        self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        if self.action.phase != 'select':
            self.action.selectable_cards = []
            piles = self.player.hand
            self.player.phase = 'attacked'
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = len(self.action.selectable_cards) - 3
                self.action.select_cards = 'mandatory'
                self.action.phase = 'select'
                self.desk.draw()
            else:
                self.action.cleanup()
        else:
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_discard(card)                
            self.player.coalesce_hand()
            self.action.cleanup()
            self.player.phase = 'wait'
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('info')
            self.desk.draw()
            self.player.game.switch_player = True
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'card_name' : self.name_en }, self.player.game.get_other_players_names())
