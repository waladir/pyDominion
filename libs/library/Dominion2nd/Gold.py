from libs.classes.card import Card

class Gold(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'gold'
        self.name = 'Zlaťák' 
        self.name_en = 'Gold'
        self.expansion = 'Dominion2nd'
        self.image = 'Gold.png'
        self.kingdom_card = False
        self.type = ['treasure']
        self.subtype = None
        self.price = 6
        self.value = 3
