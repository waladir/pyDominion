from libs.classes.pile import Pile
from libs.classes.desk import Desk

class Player():
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.treasure = 0
        self.actions = 1
        self.buys = 1
        self.phase = 'wait'
        self.activated_cards = []

    def create_deck_pile(self):
        pile = Pile('players_deck', 0)
        pile.create_players_pile()
        self.deck = pile

    def create_hand(self):
        pile = Pile('players_hand', 0)
        self.hand = pile

    def create_discard_pile(self):
        pile = Pile('players_hand', 0)
        self.discard = pile

    def get_card_from_deck(self, count):
        cards = []
        for i in range(count):
            card = self.deck.get_top_card()
            cards.append(card)
        return cards
    
    def put_card_to_hand(self, cards):
        self.hand.add_card(cards)

    def move_cards_from_deck_to_hand(self, count):
        cards = self.get_card_from_deck(count)
        for card in cards:
            self.put_card_to_hand(card.name)

    def start_turn(self):
        self.phase = 'action'

    def do_turn(self, desk):
        if self.phase == 'action':
            self.action_phase(desk)
        if self.phase == 'buy':
            self.buy_phase(desk)
        if self.phase == 'cleanup':
            self.cleanup_phase(desk)

    def action_phase(self, desk):
        self.phase = 'buy'

    def buy_phase(self, desk):
        desk.draw()

    def cleanup_phase(self, desk):
        self.treasure = 0
        self.actions = 1
        self.buys = 1
        pass

    def wait_phase(self, desk):
        self.phase = 'wait'
        pass
