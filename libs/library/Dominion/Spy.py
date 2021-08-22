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

class Spy(Card):
    def __init__(self):
        self.id = 'spy'
        self.name = 'Špion' 
        self.name_en = 'Spy'
        self.expansion = 'Dominion'
        self.image = 'Spy.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
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
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()

        if self.action.phase != 'select':
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
                                    if 'cards' in event:
                                        self.select_to_choose.append({ event['player'] : event['cards'] })
                                    other_players.remove(event['player'])
                                    self.player.events.remove(event)
                                    if len(other_players) == 0:
                                        self.action.phase = 'select'
                                        self.subphase = 'select_to_choose'
                                        end_wait = True
                for event in pygame.event.get():
                    self.player.game.check_events(event)
            if len(self.select_to_choose) == 0:
                self.action.phase = 'select'               
                self.subphase = 'select_to_choose_self'
            self.player.phase = 'action'
            self.do_action()
        else:
            if self.subphase == 'attack_resolution':
                self.desk.select_area = False
                for pile in self.action.selected_piles:
                    if pile == self.player.deck:
                        create_event(self.player.game.get_me(), 'return_card_to_deck', { 'attacking_player' : self.player.name, 'player' : self.cards_data[self.card_to_choose], 'card_name' : self.card_to_choose.name }, self.player.game.get_other_players_names())                        
                    else:
                        create_event(self.player.game.get_me(), 'discard_card_from_deck', { 'attacking_player' : self.player.name, 'player' : self.cards_data[self.card_to_choose], 'card_name' : self.card_to_choose.name }, self.player.game.get_other_players_names())                        
                if len(self.select_to_choose) == 0:
                    self.desk.changed.append('play_area')
                    self.subphase = 'select_to_choose_self'
                    self.desk.draw()                
                else:
                    self.subphase = 'select_to_choose'

            if self.subphase == 'self_resolution':
                self.player.phase = 'action'
                self.desk.select_area = False
                for pile in self.desk.select_area_piles:
                    card = pile.get_top_card()
                for pile in self.action.selected_piles:
                    if pile == self.player.deck:
                        create_event(self.player.game.get_me(), 'return_card_to_deck', { 'attacking_player' : self.player.name, 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                        
                        self.player.put_card_to_deck(card)
                    else:
                        create_event(self.player.game.get_me(), 'discard_card_from_deck', { 'attacking_player' : self.player.name, 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                        
                        self.player.put_card_to_discard(card)
                self.action.selectable_piles = []
                self.action.selected_piles = []
                self.desk.select_area_piles = []
                self.action.cleanup()                    
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_discard')
                self.desk.changed.append('play_area')
                self.desk.draw()                

            if self.subphase == 'select_to_choose' and len(self.select_to_choose) > 0:
                event = self.select_to_choose[0]
                self.select_to_choose.remove(event)
                player = list(event.keys())[0]
                cards = event[player]
                self.action.selectable_piles = []
                self.action.selected_piles = []
                self.desk.select_area_piles = []
                for card_name in cards:
                    cardClass = self.get_class(card_name)
                    card = cardClass() 
                    self.action.to_select = 1
                    self.card_to_choose = card
                    self.desk.put_card_to_select_area(card)
                    self.cards_data.update({ card : player })
                self.action.selectable_piles.append(self.player.deck)
                self.action.selectable_piles.append(self.player.discard)
                self.action.select_cards = 'mandatory'
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Označ jestli má hráč ' + player + ' odložit kartu na svůj odkládací balíček nebo vrátit do dobíracího balíčku'
                self.subphase = 'attack_resolution'
                self.desk.changed.append('select_area')
                self.desk.draw()

            if self.subphase == 'select_to_choose_self':
                self.action.selectable_piles = []
                self.action.selected_piles = []
                self.desk.select_area_piles = [] 
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    self.action.to_select = 1
                    self.desk.put_card_to_select_area(card)
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.action.selectable_piles.append(self.player.deck)
                self.action.selectable_piles.append(self.player.discard)
                self.action.select_cards = 'mandatory'
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Označ jestli odložíš svou kartu na odkládací balíček nebo ji vrátíš do dobíracího balíčku'
                self.subphase = 'self_resolution'
                self.desk.changed.append('select_area')
                self.desk.changed.append('players_deck')
                self.desk.draw()

    def do_attack(self):
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
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    card_names.append(card.name_en)
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.player.phase = 'wait'
                self.desk.changed.append('players_deck')
                self.desk.changed.append('info')
                self.desk.draw()
                self.player.game.switch_player = True
                create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.name_en, 'cards' : card_names }, self.player.game.get_other_players_names())
