import sys
import time
import pygame
from pygame.locals import *

from libs.classes.desk import Desk
from libs.classes.player import Player
from libs.api import call_api
from libs.events import get_events, create_event

class Game():
    def __init__(self, id, players_count, players, expansions):
        self.id = id
        self.players_count = players_count
        self.players = players
        self.expansions = expansions
        self.round = 0
        self.state = 'created'

    def create(self, SCREEN, cards_set):
        self.me = self.players[0].name
        self.round = 0
        self.SCREEN = SCREEN
        self.cards_set = cards_set
        self.round = self.round + 1
        self.current_player = 0 
        self.desk = Desk(self.SCREEN, self.cards_set, self.players_count, self, self.players[self.current_player])
        for player in self.players:
            player.attach_game(self)
            player.create_deck_pile()
            player.create_hand()
            player.create_discard_pile()
            player.move_cards_from_deck_to_hand(5)
        self.desk.draw(False)
        data = call_api({ 'function' : 'update_game', 'id' : self.id, 'status' : self.state, 'desk' : {}, 'round' : self.round, 'current_player' : 0 })
        self.desk.add_message('Čekám na ostatní hráče')
        self.wait_for_start()
        self.state = 'running'
        players_names = []
        idx = 0
        for player in self.players:
            players_names.append(player.name)
            idx = player.index
        data = call_api({ 'function' : 'get_game', 'id' : self.id })
        for player_name in data['players']:
            if player_name not in players_names:
                idx = idx + 1
                player = Player(player_name, idx)
                self.players.append(player)

    def join_game(self, SCREEN, cards_set, round, me):
        self.me = me
        self.SCREEN = SCREEN
        self.current_player = 0
        self.cards_set = cards_set
        self.round = round
        self.desk = Desk(self.SCREEN, self.cards_set, self.players_count, self, self.get_me())
        for player in self.players:
            player.attach_game(self)
            player.create_deck_pile()
            player.create_hand()
            player.create_discard_pile()
            player.move_cards_from_deck_to_hand(5)
        self.desk.draw(False)
        self.desk.add_message('Čekám na ostatní hráče')
        players_names = []
        idx = 0
        for player in self.players:
            players_names.append(player.name)
            idx = player.index
        data = call_api({ 'function' : 'get_game', 'id' : self.id })
        for player_name in data['players']:
            if player_name not in players_names:
                idx = idx + 1
                player = Player(player_name, idx)
                self.players.append(player)
        create_event(self.get_me(), 'joined', self.get_me().name, self.get_other_players_names())
        self.wait_for_start()
        self.state = 'running'

    def next_player(self):
        if self.current_player+1 > len(self.players)-1:
            self.current_player = 0
            self.round = self.round + 1
        else:
            self.current_player = self.current_player + 1
        self.switch_player = True

    def do_round(self):
        player = self.players[self.current_player]
        if player.name == self.me:
            player.start_turn()
            player.do_turn(self.desk)
        else:
            player = self.get_me()
            if player.phase == 'attacked_reaction' or player.phase == 'attacked' :
                player.do_turn(self.desk)
            

    def get_other_players_names(self):
        names = []
        for player in self.players:
            if player.name != self.me:
                names.append(player.name)
        return names

    def get_other_players(self):
        players = []
        for player in self.players:
            if player.name != self.me:
                players.append(player)
        return players

    def get_me(self):
        for player in self.players:
            if player.name == self.me:
                return player
        return None

    def wait_for_start(self):
        data = call_api({ 'function' : 'get_game', 'id' : self.id })
        last_ts = 0
        while data['status'] == 'created':
            ts = int(time.time())             
            if ts-last_ts > 3:
                last_ts = ts
                get_events(self.get_me())
                data = call_api({ 'function' : 'get_game', 'id' : self.id })
            for event in pygame.event.get():
                self.check_events(event)
  

    def check_end(self, card):
        piles = self.desk.basic_piles + self.desk.kingdom_piles
        empty = 0
        end = False
        for pile in piles:
            if pile.card_id == 'province' and len(pile.cards) == 0:
                end = True
            if len(pile.cards) == 0:
                empty = empty + 1
        if empty >= 3:
            end = True
        if end == True:
            player = self.players[self.current_player]
            player.phase = 'end_game'
            self.state = 'end'
            player.put_card_to_discard(card)
            for pile in self.desk.play_area_piles:
                for i in range(len(pile.cards)):
                    card = pile.top_card()
                    player.put_card_to_discard(card)
            self.desk.coalesce_play_area()
            player.coalesce_hand()
            points = player.get_points()
            player.results.append({ 'player' : player.name, 'points' : points })
            create_event(player, 'end_game', None, self.get_other_players_names())
            create_event(player, 'results', { 'player_name' : player.name, 'points' : points }, player.game.get_other_players_names())
        return end

    def check_events(self, event):
        if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()    
        if event.type == pygame.KEYDOWN and event.key != K_RIGHT and event.key != K_LEFT and event.key != K_ESCAPE:
            if event.key == K_RETURN:
                self.desk.add_message(self.desk.player.name + ': ' + self.desk.chat)
                player = self.get_me()
                create_event(player, 'message', { 'player' : player.name, 'message' : self.desk.chat }, player.game.get_other_players_names())
                self.desk.chat = ''
            elif event.key == K_BACKSPACE:
                self.desk.chat = self.desk.chat[:-1]
            else:
                self.desk.chat += event.unicode
            self.desk.draw_chat()

