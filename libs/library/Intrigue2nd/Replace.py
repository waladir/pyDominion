import sys
import time
import pygame
from pygame.locals import *
from libs.classes.card import Card

class Replace(Card):
    def __init__(self):
        self.id = 'replace'
        self.name = 'Záměna' 
        self.name_en = 'Replace'
        self.expansion = 'Intrigue2nd'
        self.image = 'Replace.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 5
        self.value = 0

        self.subphase = ''
        self.card_price = -1

    def do_action(self):
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.action.select_cards = 'mandatory'
                self.desk.draw()   
                self.subphase = 'trash_card'             
            else:
                self.action.cleanup()
        else:
            if self.subphase == 'trash_card':
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    card_price = card.price + 2 
                    self.player.coalesce_hand()
                    self.desk.trash.add_card(card)
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('trash')
                    self.desk.draw() 

                self.action.selectable_cards = []
                self.action.selected_cards = {}
                piles = self.desk.basic_piles + self.desk.kingdom_piles
                for pile in piles:
                    card = pile.top_card()
                    if card.price <= card_price:
                        self.action.selectable_cards.append(card)
                if len(self.action.selectable_cards) > 0:
                    self.action.select_cards = 'mandatory'
                    self.action.to_select = 1
                    self.desk.redraw_borders()    
                    self.subphase = 'gain_card'              
                else:
                    self.action.cleanup()
                    self.desk.draw()
            elif self.subphase == 'gain_card':
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    if 'action' in card.type or 'treasure' in card.type:
                        self.player.put_card_to_deck(card) 
                        self.desk.changed.append('players_deck')
                        self.desk.changed.append('basic')
                        self.desk.changed.append('kingdom')
                        self.desk.draw()
                    if 'victory' in card.type:
                        if 'action' not in card.type and 'treasure' not in card.type:
                            self.player.put_card_to_discard(card) 
                            self.desk.changed.append('players_discard')
                            self.desk.draw()
                        from libs.events import get_events, create_event
                        other_players = self.player.game.get_other_players_names()
                        create_event(self.player.game.get_me(), 'attack', { 'player' : self.player.name, 'card_name' : self.name_en }, other_players)
                        self.player.phase = 'attack'
                        self.desk.changed.append('info')
                        self.desk.draw()
                        last_ts = 0
                        end_wait = False
                        self.desk.changed.append('action_button')
                        self.desk.draw()

                        while end_wait == False:
                            ts = int(time.time())             
                            if ts-last_ts > 1:
                                last_ts = ts
                                get_events(self.player.game.get_me())
                                if len(self.player.events) > 0:
                                    for event in self.player.events:
                                        if event['event_type'] == 'attack_reaction' and event['card_name'] == self.name_en:
                                            other_players.remove(event['player'])
                                            self.player.events.remove(event)
                                if len(other_players) == 0:
                                    end_wait = True
                                for event in pygame.event.get():
                                    self.player.game.check_events(event)
                self.card_price = -1
                self.action.cleanup()   
                self.player.phase = 'action'                 
                self.desk.changed.append('info')
                self.desk.draw()

    def do_attack(self):
        from libs.events import get_events, create_event
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
                create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.name_en }, self.player.game.get_other_players_names())
