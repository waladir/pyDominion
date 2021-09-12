from libs.classes.card import Card

class Curse(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'curse'
        self.name = 'Kletba' 
        self.name_en = 'Curse'
        self.expansion = 'Dominion2nd'
        self.image = 'Curse.png'
        self.kingdom_card = False
        self.type = ['curse']
        self.subtype = None
        self.price = 0
        self.value = -1
