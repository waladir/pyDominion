from libs.classes.card import Card

class Silver(Card):
    def __init__(self):
        self.id = 'silver'
        self.name = 'Stříbrňák' 
        self.name_en = 'Silver'
        self.expansion = 'Dominion'
        self.image = 'Silver.png'
        self.kingdom_card = False
        self.type = ['treasure']
        self.subtype = None
        self.price = 3
        self.value = 2
