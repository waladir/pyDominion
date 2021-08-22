# import traceback
import time
import pygame
from pygame.locals import *

class Action():
    def __init__(self, card, player):
        self.card = card
        self.player = player
        self.bonuses = True
        self.phase = None

        self.selectable_cards = []
        self.select_cards = 'optional'
        self.selected_cards = {}
        self.selectable_piles = []
        self.select_piles = 'optional'
        self.selected_piles = []
        self.selectable_info = []
        self.selected_info = []
        self.attack_card = None

        self.to_select = -1
        self.skipped_cards = []
        self.cards_to_play = []

        self.to_attack = []
        self.defended = []

    def do_action(self):
        self.card.action = self
        self.card.do_action()

    def check_reaction(self):
        from libs.events import get_events, create_event
        other_players = self.player.game.get_other_players_names()
        create_event(self.player.game.get_me(), 'check_reaction', { 'player' : self.player.name, 'card_name' : self.card.name_en }, other_players)
        self.player.phase = 'attack'
        last_ts = 0
        end_wait = False
        self.player.coalesce_hand()        
        self.player.desk.changed.append('action_button')
        self.player.desk.changed.append('play_area')
        self.player.desk.changed.append('players_hand')
        self.player.desk.changed.append('info')
        self.player.desk.draw()
        while end_wait == False:
            ts = int(time.time())             
            if ts-last_ts > 1:
                last_ts = ts
                get_events(self.player.game.get_me())
                if len(self.player.events) > 0:
                    for event in self.player.events:
                        if event['event_type'] == 'attack_reaction' and event['card_name'] == self.card.name_en:
                            if int(event['defend']) == 1 and event['player'] not in self.defended:
                                self.defended.append(event['player'])
                            if int(event['end']) == 1:
                                other_players.remove(event['player'])
                                if event['player'] not in self.defended:
                                    self.to_attack.append(event['player'])
                            self.player.events.remove(event)
                            if len(other_players) == 0:
                                end_wait = True
            for event in pygame.event.get():
                self.player.game.check_events(event)
        self.player.phase = 'action'

    def do_attack(self):
        from libs.events import get_events, create_event
        if len(self.to_attack) > 0:
            create_event(self.player.game.get_me(), 'attack', { 'player' : self.player.name, 'card_name' : self.card.name_en }, self.to_attack)
            self.player.phase = 'attack'
            last_ts = 0
            end_wait = False
            self.player.desk.changed.append('action_button')
            self.player.desk.changed.append('play_area')
            self.player.desk.changed.append('info')
            self.player.desk.draw()
            while end_wait == False:
                ts = int(time.time())             
                if ts-last_ts > 1:
                    last_ts = ts
                    get_events(self.player.game.get_me())
                    if len(self.player.events) > 0:
                        for event in self.player.events:
                            if event['event_type'] == 'attack_respond' and event['card_name'] == self.card.name_en:
                                self.to_attack.remove(event['player'])
                                self.player.events.remove(event)
                                if len(self.to_attack) == 0:
                                    end_wait = True
                for event in pygame.event.get():
                    self.player.game.check_events(event)
        self.player.phase = 'action'

    def do_check_reaction(self):
        from libs.events import create_event
        self.attack_card = self.card
        piles = self.player.hand
        for pile in piles:
            card = pile.top_card()
            if 'action' in card.type and card.subtype == 'reaction':
                self.selectable_cards.append(card)
            self.to_select = len(self.selectable_cards)
            self.phase = 'select'
        if len(self.selectable_cards) == 0:
            self.player.phase = 'wait'
            self.player.desk.changed.append('info')
            self.player.desk.draw()
            self.player.game.switch_player = True
            create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.attack_card.name_en, 'end' : 1, 'defend' : 0 }, self.player.game.get_other_players_names())
            self.cleanup()

    def do_reaction(self):
        self.card.action = self
        self.card.do_reaction()

    def do_attacked(self):
        self.card.action = self
        self.card.do_attacked()

    def select_card(self, card, pile):
        self.selectable_cards.remove(card)
        self.selected_cards.update({ card : pile })   
        if (len(self.selected_cards) + len(self.selected_piles) + len(self.selected_info)) == self.to_select:
            self.to_select = -1
            if self.player.phase == 'action' or self.player.phase == 'select':
                self.do_action()
            if self.player.phase == 'attacked':
                self.do_attacked()
            if self.player.phase == 'attacked_reaction':
                from libs.events import create_event
                action = self
                for card in self.selected_cards:
                    attack_card = self.attack_card
                    self.player.action = Action(card, self.player)
                    self.player.action.attack_card = attack_card
                    self.player.action.do_reaction()   
                self.player.action = action  
                create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.player.action.attack_card.name_en, 'end' : 1, 'defend' : 0 }, self.player.game.get_other_players_names())

    def cleanup(self):
        if len(self.player.actions_to_play) > 0:
            action = self.player.actions_to_play[0] 
            self.player.actions_to_play.remove(action)
            self.player.action = action
            action.do_action()
        else:            
            self.player.action = None
        del self