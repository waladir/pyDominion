import random

from libs.classes.card import Card

class Pile():
    def __init__(self, place, position):
        self.place = place
        self.position = position
        self.cards = []

    def create_pile(self, card, count):
        for i in range(count):
            self.add_card(card)

    def create_players_pile(self):
        self.create_pile('Měďák', 7)
        self.create_pile('Statek', 3)
        self.shuffle()        

    def add_card(self, card_id):
        card = Card(card_id)
        self.cards.append(card)

    def top_card(self):
        if len(self.cards) > 0:
            return self.cards[0]
        return None

    def get_top_card(self):
        if len(self.cards) > 0:
            card = self.cards[0]
            self.cards.remove(card)
            return card

    def shuffle(self):
        random.shuffle(self.cards)


