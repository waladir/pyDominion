from libs.classes.pile import Pile
from libs.classes.desk import Desk
from libs.events import get_events, create_event

class Player():
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.treasure = 0
        self.actions = 1
        self.buys = 1
        self.phase = 'wait'

        self.action = None
        self.actions_to_play = []

        self.events = []
        self.results = []

    def attach_game(self, game):
        self.game = game

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
        for card in cards:
            self.put_card_to_hand(card)

    def move_cards_from_hand_to_discard(self, count):
        cards = self.get_cards_from_hand(count)
        for card in cards:
            self.put_card_to_discard(card)   
        self.coalesce_hand()

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
        create_event(self, 'start_turn', self.name, self.game.get_other_players_names())
        self.phase = 'action'

    def do_turn(self, desk):
        if self.phase == 'action':
            self.action_phase(desk)
        if self.phase == 'buy':
            self.buy_phase(desk)
        if self.phase == 'cleanup':
            self.cleanup_phase()
        if self.phase == 'attacked_reaction' or self.phase == 'attacked':
            desk.changed.append('info')
            desk.draw()
            
    def action_phase(self, desk):
        self.action = None
        create_event(self, 'action', self.name, self.game.get_other_players_names())
        self.desk.add_message('Začátek akční fáze')
        desk.changed.append('info')
        desk.draw()

    def buy_phase(self, desk):
        desk.changed.append('info')
        desk.draw()

    def cleanup_phase(self):
        for pile in self.game.desk.play_area_piles:
            for i in range(len(pile.cards)):
                card = pile.get_top_card()
                self.put_card_to_discard(card)
        self.move_cards_from_hand_to_discard(len(self.hand))
        self.move_cards_from_deck_to_hand(5)      
        self.treasure = 0
        self.actions = 1
        self.buys = 1
        self.phase = 'wait'
        self.action = None
        self.desk.clear_triggers(duration = 'end_of_round')
        self.desk.draw(False)
        create_event(self, 'next_player', self.name, self.game.get_other_players_names())
        self.game.next_player()

    def wait_phase(self, desk):
        self.phase = 'wait'

    def get_phase(self):
        if self.phase == 'wait':
            return 'čekám na ostatní hráče'
        if self.phase == 'action':
            return 'Akční'
        if self.phase == 'buy':
            return 'Nákup'
        if self.phase == 'attack':
            return 'Útok - čekání na reakci'
        if self.phase == 'attacked_reaction':
            return 'Útok - reakce'
        if self.phase == 'attacked':
            return 'Útok - akce'            
        if self.phase == 'buy':
            return 'Nákup'
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
                self.phase = 'buy'
                create_event(self, 'buy', self.name, self.game.get_other_players_names())
                self.desk.changed.append('info')
                self.desk.draw()
        if self.phase == 'buy':
            skip_phase = False
            if self.buys == 0:
                self.desk.add_message('Žádný další nákup, konec fáze nákupu')
                skip_phase = True
            if skip_phase == True:
                self.phase = 'cleanup'
                self.cleanup_phase()
                self.desk.changed.append('info')
                self.desk.draw()                
