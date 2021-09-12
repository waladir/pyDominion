# import traceback
import time
import pygame
from pygame.locals import *

class Action():
    def __init__(self, card, player):
        self.card = card
        self.player = player
        self.card.action = self
        self.to_attack = []
        self.defended = []
        self.data = []

    def do_action(self):
        self.player.phase = 'action_play'
        self.card.do_action()

    def request_reactions(self):
        from libs.events import create_event
        self.other_players = self.player.game.get_other_players_names()
        create_event(self.player.game.get_me(), 'request_reaction', { 'player' : self.player.name, 'card_name' : self.card.name_en }, self.other_players)
        self.player.phase = 'attack_wait_for_reaction'
        self.player.desk.changed.append('info')
        self.player.desk.draw()

    def get_reaction(self, player_name, defend, end):
        if defend == 1 and player_name not in self.defended:
            self.player.desk.add_message('Hráč ' + player_name + ' se ubránil útoku')
            self.defended.append(player_name)
        if end == 1:
            self.other_players.remove(player_name)
            if player_name not in self.defended:
                self.to_attack.append(player_name)
        if len(self.other_players) == 0:
            self.player.phase = 'action_play'
            self.player.desk.changed.append('info')
            self.player.desk.draw()            
            self.do_action()

    def do_check_reaction(self):
        from libs.events import create_event
        for trigger in self.player.desk.get_triggers('attack'):
            trigger.run()
        selectable_piles = []
        for pile in self.player.hand:
            card = pile.top_card()
            if 'action' in card.type and card.subtype == 'reaction':
                selectable_piles.append(pile)
        if len(selectable_piles) > 0:
            self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
            self.player.desk.add_message('Můžeš použít karty reakce. Ukonči výběr, pokud chceš reakce ukončit.')
            self.player.desk.draw()
        else:
            self.player.phase = 'other_players_turn'
            self.player.desk.changed.append('info')
            self.player.desk.draw()
            create_event(self.player.game.get_me(), 'send_reaction', { 'player' : self.player.name, 'defend' : 0, 'end' : 1 }, self.player.game.get_other_players_names())

    def do_attack(self):
        from libs.events import create_event
        self.to_attack = list(dict.fromkeys(self.to_attack))
        if len(self.to_attack) > 0:
            create_event(self.player.game.get_me(), 'attack', { 'player' : self.player.name, 'card_name' : self.card.name_en }, self.to_attack)
            self.player.phase = 'attack_wait_for_respond'
            self.player.desk.changed.append('info')
            self.player.desk.draw()
        else:
            self.player.phase = 'action_play'
            self.player.desk.changed.append('info')
            self.player.desk.draw()            
            self.do_action()            
            
    def get_attack_respond(self, player_name, data):
        self.to_attack.remove(player_name)
        self.data.append(data)
        if len(self.to_attack) == 0:
            self.player.phase = 'action_play'
            self.player.desk.changed.append('info')
            self.player.desk.draw()            
            self.do_action()

    def do_reaction(self):
        self.card.do_reaction()

    def do_attacked(self):
        self.card.do_attacked()

    def cleanup(self):
        if len(self.player.actions_to_play) > 0:
            self.player.actions_to_play.remove(self)
            if len(self.player.actions_to_play) > 0:
                action = self.player.actions_to_play[0]
                if self.player.phase == 'action_play':
                    action.do_action()
                elif self.player.phase == 'attacked_reaction':
                    action.do_reaction()
            else:
                if self.player.phase == 'action_play':
                    self.player.phase = 'action'
                    self.player.activity.cards_to_play()
                    self.player.check_phase_end()    
                    self.player.desk.draw()        
                if self.player.phase == 'attacked' or self.player.phase == 'attacked_reaction':
                    if self.player.phase == 'attacked_reaction':
                        self.player.desk.clear_select()
                        del self.card
                        self.do_check_reaction()
                    if self.player.phase == 'attacked':
                        self.player.desk.clear_select()
                        self.player.phase = 'other_players_turn'
                        self.player.desk.changed.append('info')
                    self.player.desk.draw()
                
