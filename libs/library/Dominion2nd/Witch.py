import sys
import time
import pygame
from pygame.locals import *
from libs.classes.card import Card

class Witch(Card):
    def __init__(self):
        self.id = 'witch'
        self.name = 'Čarodějnice' 
        self.name_en = 'Witch'
        self.expansion = 'Dominion2nd'
        self.image = 'Witch.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 5
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False 
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
        self.action.check_reaction()
        self.action.do_attack()
        self.action.cleanup()        
        self.desk.changed.append('info')
        self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        piles = self.desk.basic_piles
        for pile in piles:
            card = pile.top_card()
            if card.name == 'Kletba':
                card = pile.get_top_card()
                if card is not None:
                    self.player.put_card_to_discard(card)
        self.player.coalesce_hand()
        self.action.cleanup()
        self.player.phase = 'wait'
        self.desk.changed.append('players_discard')
        self.desk.changed.append('info')
        self.desk.draw()
        self.player.game.switch_player = True
        create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'card_name' : self.name_en }, self.player.game.get_other_players_names())

