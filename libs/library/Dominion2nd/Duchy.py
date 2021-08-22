from libs.classes.card import Card

class Duchy(Card):
    def __init__(self):
        self.id = 'duchy'
        self.name = 'Vévodství' 
        self.name_en = 'Duchy'
        self.expansion = 'Dominion2nd'
        self.image = 'Duchy.png'
        self.kingdom_card = False
        self.type = ['victory']
        self.subtype = None
        self.price = 5
        self.value = 3
