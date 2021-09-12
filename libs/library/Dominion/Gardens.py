import math
from libs.classes.card import Card

class Gardens(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'gardens'
        self.name = 'Zahrady' 
        self.name_en = 'Gardens'
        self.expansion = 'Dominion'
        self.image = 'Gardens.png'
        self.kingdom_card = True
        self.type = ['victory']
        self.subtype = None
        self.price = 4
        self.value = 999

    def do_victory_points(self, cards):
        return math.floor(len(cards)/10)
