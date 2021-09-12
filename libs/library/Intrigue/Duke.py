import math

from libs.classes.card import Card

class Duke(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'duke'
        self.name = 'Vévoda' 
        self.name_en = 'Duke'
        self.expansion = 'Intrigue'
        self.image = 'Duke.png'
        self.kingdom_card = True
        self.type = ['victory']
        self.subtype = None
        self.price = 5
        self.value = 999

    def do_victory_points(self, cards):
        points = 0
        for card in cards:
            if card.name_en == 'Duchy':
                points = points + 1
        return points