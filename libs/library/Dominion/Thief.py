import sys
import time
import pygame
from pygame.locals import *

from libs.classes.card import Card

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd

import traceback

class Thief(Card):
    def __init__(self):
        self.id = 'thief'
        self.name = 'Zloděj' 
        self.name_en = 'Thief'
        self.expansion = 'Dominion'
        self.image = 'Thief.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
        self.value = 0

        self.subphase = ''
        self.select_to_trash = []
        self.to_trash = []
        self.cards_data = {}

    def do_action(self):
        if self.action.phase != 'select':
            from libs.events import get_events, create_event
            other_players = self.player.game.get_other_players_names()
            create_event(self.player.game.get_me(), 'attack', { 'player' : self.player.name, 'card_name' : self.name_en }, other_players)
            self.player.phase = 'attack'
            self.player.coalesce_hand()        
            self.desk.changed.append('players_hand')
            self.desk.changed.append('play_area')
            self.desk.changed.append('info')
            self.desk.draw()
            last_ts = 0
            end_wait = False
            self.desk.changed.append('action_button')
            self.desk.draw()
            while end_wait == False:
                if self.desk.select_area == False:
                    ts = int(time.time())             
                    if ts-last_ts > 1:
                        last_ts = ts
                        get_events(self.player.game.get_me())
                        if len(self.player.events) > 0:
                            for event in self.player.events:
                                if event['event_type'] == 'attack_reaction' and event['card_name'] == self.name_en:
                                    self.select_to_trash.append({ event['player'] : event['cards'] })
                                    other_players.remove(event['player'])
                                    self.player.events.remove(event)
                                    if len(other_players) == 0:
                                        self.action.phase = 'select'
                                        self.subphase = 'select_to_trash'
                                        end_wait = True
                for event in pygame.event.get():
                    self.player.game.check_events(event)
            self.do_action()
        else:
            if self.subphase == 'to_trash':
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.to_trash.append(card)
                if len(self.select_to_trash) == 0:
                    self.subphase = 'select_to_gain'
                else:
                    self.subphase = 'select_to_trash'

            if self.subphase == 'select_to_trash' and len(self.select_to_trash) > 0:
                event = self.select_to_trash[0]
                self.select_to_trash.remove(event)
                player = list(event.keys())[0]
                cards = event[player]
                for card_name in cards:
                    cardClass = Dominion.get_class(card_name)
                    card = cardClass() 
                    if 'treasure' in card.type:
                        self.action.to_select = 1
                        self.action.selectable_cards.append(card)
                        self.desk.put_card_to_select_area(card)
                    self.action.phase = 'select'
                    self.cards_data.update({ card : player })
                if len(self.action.selectable_cards) > 0:
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Označ karty peněz hráče ' + player + ', které zahodí na smetiště'
                    self.player.phase = 'action'
                    self.subphase = 'to_trash'
                    self.desk.changed.append('select_area')
                    self.desk.draw()

            if self.subphase == 'select_to_gain':
                self.action.selectable_cards = []
                self.action.selected_cards = {}
                self.desk.select_area_piles = []
                for card in self.to_trash:
                    self.action.selectable_cards.append(card)
                    self.desk.put_card_to_select_area(card)
                if len(self.action.selectable_cards) > 0:
                    self.action.to_select = len(self.action.selectable_cards)
                    print('aaaaaa')
                    self.action.to_select = 1
                    self.action.phase = 'select'
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Ze zahozených karet si vyber libovolný počet karet, které získáš'
                    self.desk.changed.append('select_area')
                    self.subphase = 'cleanup'
                    self.desk.draw()
                self.subphase = 'cleanup'

            if self.subphase == 'cleanup':
                print(self.action.selected_cards)
                self.desk.select_area = False
                for card in self.cards_data:
                    print(card)
                    print(card.name)
                    print(self.action.selected_cards)
                    if card in self.action.selected_cards:
                        print('x')
                    elif card in self.to_trash:
                        print('y')
                    else:
                        print('z')


                self.action.cleanup()                    
                self.desk.changed.append('play_area')
                self.desk.changed.append('trash')
                self.desk.draw()                



    def do_attack(self):
        from libs.events import create_event
        self.player.attack_card = self
        if self.action.phase != 'select':
            self.action.selectable_cards = []
            if self.player.phase == 'attacked_reaction':
                piles = self.player.hand
                for pile in piles:
                    card = pile.top_card()
                    if 'action' in card.type and card.subtype == 'reaction':
                        self.action.selectable_cards.append(card)
                        self.action.to_select = 1
                        self.action.phase = 'select'
            if len(self.action.selectable_cards) == 0 or self.player.phase == 'attacked':
                card_names = []
                cards = self.player.get_cards_from_deck(2)
                for card in cards:
                    card_names.append(card.name_en)
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.player.phase = 'wait'
                self.desk.changed.append('players_deck')
                self.desk.changed.append('info')
                self.desk.draw()
                self.player.game.switch_player = True
                create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.name_en, 'cards' : card_names }, self.player.game.get_other_players_names())
