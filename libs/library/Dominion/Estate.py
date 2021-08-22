from libs.classes.card import Card

class Estate(Card):
    def __init__(self):
        self.id = 'estate'
        self.name = 'Statek' 
        self.name_en = 'Estate'
        self.expansion = 'Dominion'
        self.image = 'Estate.png'
        self.kingdom_card = False
        self.type = ['victory']
        self.subtype = None
        self.price = 2
        self.value = 1

