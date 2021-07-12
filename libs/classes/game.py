from libs.classes.desk import Desk

class Game():
    def __init__(self, players_count, players, expansions):
        self.players_count = players_count
        self.players = players
        self.expansions = expansions
        self.state = 'created'

    def start(self, SCREEN, cards_set):
        self.round = 0
        for player in self.players:
            player.create_deck_pile()
            player.create_hand()
            player.create_discard_pile()
            player.move_cards_from_deck_to_hand(5)
        self.current_player = 0
        self.desk = Desk(SCREEN, cards_set, self.players_count, self.players[self.current_player])
        self.state = 'running'
        self.next_round()

    def next_round(self):
        self.round = self.round + 1
        player = self.players[self.current_player]
        player.start_turn()
        player.do_turn(self.desk)
        # test jestli hra neskoncila            





