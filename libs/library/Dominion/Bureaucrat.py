import sys
import time
import pygame
from pygame.locals import *

from libs.classes.card import Card

class Bureaucrat(Card):
    def __init__(self):
        self.id = 'bureaucrat'
        self.name = 'Úředník' 
        self.name_en = 'Bureaucrat'
        self.expansion = 'Dominion'
        self.image = 'Bureaucrat.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
        self.value = 0

    def do_action(self):
        self.action.check_reaction()
        for pile in self.desk.basic_piles:
            card = pile.top_card()
            if card.id == 'silver':
                card = pile.get_top_card()
                self.player.put_card_to_deck(card)
        self.action.do_attack()
        self.action.cleanup()        
        self.player.phase = 'action'
        self.desk.changed.append('info')
        self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        self.player.attack_card = self
        if self.action.phase != 'select':
            piles = self.player.hand
            self.player.phase = 'attacked'
            for pile in piles:
                card = pile.top_card()
                if 'victory' in card.type:
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.action.select_cards = 'mandatory'
                self.desk.draw()
            else:
                piles = self.player.hand
                self.player.phase = 'attacked'
                for pile in piles:
                    card = pile.top_card()
                    create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                                    
                self.action.cleanup()
                self.player.phase = 'wait'
                self.desk.changed.append('players_hand')
                self.desk.changed.append('players_deck')
                self.desk.changed.append('info')
                self.desk.draw()
                self.player.game.switch_player = True
                create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'card_name' : self.name_en }, self.player.game.get_other_players_names())
        else:
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_deck(card)
                create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + 'vložil kartu ' + card.name + ' z ruky do dobíracího balíčku'}, self.player.game.get_other_players_names())
            self.player.coalesce_hand()
            self.action.cleanup()
            self.player.phase = 'wait'
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_deck')
            self.desk.changed.append('info')
            self.desk.draw()
            self.player.game.switch_player = True
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'card_name' : self.name_en }, self.player.game.get_other_players_names())
