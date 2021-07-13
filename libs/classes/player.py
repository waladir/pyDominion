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
        self.activated_cards = {}

    def attach_game(self, game):
        self.game = game

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

    def get_cards_from_deck(self, count):
        cards = []
        for i in range(count):
            card = self.deck.get_top_card()
            cards.append(card)
        return cards

    def get_cards_from_hand(self, count):
        cards = []
        for i in range(count):
            card = self.hand.get_top_card()
            cards.append(card)
        return cards

    def get_cards_from_discard(self, count):
        cards = []
        for i in range(count):
            card = self.discard.get_top_card()
            cards.append(card)
        return cards        

    def put_card_to_deck(self, card):
        self.deck.add_card(card)  

    def put_card_to_hand(self, card):
        self.hand.add_card(card)

    def put_card_to_discard(self, card):
        self.discard.add_card(card)      

    def move_cards_from_discard_to_deck(self, count):
        cards = self.get_cards_from_discard(count)
        for card in cards:
            self.put_card_to_deck(card)          

    def move_cards_from_deck_to_hand(self, count):
        if len(self.deck.cards) < count:
            to_draw = count - len(self.deck.cards)
            cards = self.get_cards_from_deck(len(self.deck.cards))
            for card in cards:
                self.put_card_to_hand(card)     
            self.discard.shuffle()
            self.move_cards_from_discard_to_deck(len(self.discard.cards))
            cards = self.get_cards_from_deck(to_draw)
            for card in cards:
                self.put_card_to_hand(card)  
        else:
            cards = self.get_cards_from_deck(count)
            for card in cards:
                self.put_card_to_hand(card)

    def move_cards_from_hand_to_discard(self, count):
        cards = self.get_cards_from_hand(count)
        for card in cards:
            self.put_card_to_discard(card)            

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
        desk.draw()
        self.phase = 'buy'

    def buy_phase(self, desk):
        desk.draw()

    def cleanup_phase(self, desk):
        self.move_cards_from_hand_to_discard(len(self.hand.cards))
        self.treasure = 0
        self.actions = 1
        self.buys = 1
        self.move_cards_from_deck_to_hand(5)      
        self.phase = 'wait'
        desk.draw()
        self.game.next_player()

    def wait_phase(self, desk):
        self.phase = 'wait'
        pass
