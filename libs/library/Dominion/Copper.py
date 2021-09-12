from libs.classes.card import Card

class Copper(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'copper'
        self.name = 'Měďák' 
        self.name_en = 'Copper'
        self.expansion = 'Dominion'
        self.image = 'Copper.png'
        self.kingdom_card = False
        self.type = ['treasure']
        self.subtype = None
        self.price = 0
        self.value = 1
