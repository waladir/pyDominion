from libs.classes.activity import Activity
from libs.classes.pile import Pile
from libs.classes.desk import Desk

from libs.events import create_event

class Player():
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.treasure = 0
        self.actions = 1
        self.buys = 1
        self.round = 0
        self.phase = 'wait_for_start'

        self.action = None
        self.activity = Activity(self)
        self.actions_to_play = []

        self.events = []
        self.results = []

        self.play_area_cards = []

    def attach_game(self, game):
        self.game = game
        self.activity.game = self.game
        self.activity.desk = self.game.desk

    def create_deck_pile(self):
        pile = Pile('players_deck', 0, self.game)
        pile.create_players_pile()
        self.deck = pile

    def create_hand(self):
        self.hand = []

    def create_discard_pile(self):
        pile = Pile('players_discard', 0, self.game)
        self.discard = pile

    def get_cards_from_deck(self, count):
        cards = []
        if len(self.deck.cards) < count:
            to_draw = count - len(self.deck.cards)
            for i in range(len(self.deck.cards)):
                card = self.deck.get_top_card()
                cards.append(card)
            self.discard.shuffle()
            self.move_cards_from_discard_to_deck(len(self.discard.cards))
            if to_draw > len(self.deck.cards):
                to_draw = len(self.deck.cards)
            if to_draw > 0:
                for i in range(to_draw):
                    card = self.deck.get_top_card()
                    cards.append(card)
        else:
            for i in range(count):
                card = self.deck.get_top_card()
                cards.append(card)
        return cards

    def get_cards_from_hand(self, count):
        cards = []
        i = 0
        for i in range(count):
            card = self.hand[i].get_top_card()
            cards.append(card)
        self.coalesce_hand()
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
        pile = Pile('players_hand', len(self.hand), self.game)
        pile.add_card(card, True)
        self.hand.append(pile)

    def put_card_to_discard(self, card):
        self.discard.add_card(card)      

    def move_cards_from_discard_to_deck(self, count):
        cards = self.get_cards_from_discard(count)
        for card in cards:
            self.put_card_to_deck(card)          

    def move_cards_from_deck_to_hand(self, count):
        cards = self.get_cards_from_deck(count)
        if self.phase != 'wait_for_start':
            create_event(self, 'draw_card', { 'player' : self.name, 'count' : len(cards) }, self.game.get_other_players_names())
        for card in cards:
            self.put_card_to_hand(card)

    def move_cards_from_hand_to_discard(self):
        for pile in self.hand:
            card = pile.get_top_card()
            self.put_card_to_discard(card)   
            create_event(self, 'discard_card', { 'player' : self.name, 'card_name' : card.name }, self.game.get_other_players_names())
            del pile
        self.hand = []

    def coalesce_hand(self):
        for pile in self.hand:
            if len(pile.cards) == 0:
               self.hand.remove(pile)
               del pile
        i = 0
        for pile in self.hand:
            pile.position = i
            i = i + 1

    def start_turn(self):
        self.activity.start_action_phase()

    def get_phase(self):
        if self.phase == 'wait_for_start':
            return 'Čekám na ostatní hráče'
        if self.phase == 'action' or self.phase == 'action_play':
            return 'Akční'
        if self.phase == 'buy':
            return 'Nákup'
        if self.phase == 'other_players_turn':
            return 'Hraje ' + self.game.get_current_player()
        if self.phase == 'attack_wait_for_reaction' or self.phase == 'attack_wait_for_respond':
            if self.actions_to_play[0].card.subtype == 'attack':
                return 'Útok - čekání na reakci'
            else:
                return 'Akce - čekání na reakci'                
        if self.phase == 'attacked_reaction':
            return 'Útok - reakce'
        if self.phase == 'attacked':
            if len(self.actions_to_play) > 0 and self.actions_to_play[0].card.subtype == 'attack':
                return 'Útok - akce'   
            else:
                return 'Akce - reakce'
        if self.phase == 'end_game':
            return 'Konec hry'            

    def get_points(self):
        points = 0
        cards = self.get_cards_from_deck(len(self.deck.cards)) + self.get_cards_from_hand(len(self.hand)) + self.get_cards_from_discard(len(self.discard.cards))
        for card in cards:
            if card is not None and ('victory' in card.type or 'curse' in card.type):
                if card.value != 999:
                    points = points + card.value
                else:
                    points = points + card.do_victory_points(cards)
        return points

    def check_phase_end(self):
        if self.phase == 'action':
            skip_phase = False
            action_cards = 0
            self.coalesce_hand()
            for pile in self.hand:
                card = pile.top_card()
                if 'action' in card.type:
                    action_cards = action_cards + 1
            if action_cards == 0 and self.action is None:
                self.desk.add_message('Žádné akční karty v ruce, konec akční fáze')
                skip_phase = True
            elif self.actions == 0 and self.action is None:
                self.desk.add_message('Žádné další akce, konec akční fáze')
                skip_phase = True
            if skip_phase == True:
                self.activity.start_buy_phase()
        if self.phase == 'buy':
            skip_phase = False
            if self.buys == 0:
                self.desk.add_message('Žádný další nákup, konec fáze nákupu')
                skip_phase = True
            if skip_phase == True:
                self.activity.start_cleanup()
