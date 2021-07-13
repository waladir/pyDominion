from libs.classes.desk import Desk

class Game():
    def __init__(self, players_count, players, expansions):
        self.players_count = players_count
        self.players = players
        self.expansions = expansions
        self.round = 0
        self.state = 'created'

    def start(self, SCREEN, cards_set):
        self.round = 0
        self.SCREEN = SCREEN
        self.cards_set = cards_set
        for player in self.players:
            player.attach_game(self)
            player.create_deck_pile()
            player.create_hand()
            player.create_discard_pile()
            player.move_cards_from_deck_to_hand(5)
        self.current_player = 0
        self.state = 'running'
        self.round = self.round + 1
        self.current_player = 0        

    def next_player(self):
        if self.current_player+1 > len(self.players)-1:
            self.current_player = 0
            self.round = self.round + 1
        else:
            self.current_player = self.current_player + 1
        self.switch_player = True

    def do_round(self):
        player = self.players[self.current_player]
        self.desk = Desk(self.SCREEN, self.cards_set, self.players_count, self, self.players[self.current_player])
        player.start_turn()
        player.do_turn(self.desk)
  





