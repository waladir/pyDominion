from libs.classes.card import Card

class Province(Card):
    def __init__(self):
        self.id = 'province'
        self.name = 'Provincie' 
        self.name_en = 'Province'
        self.expansion = 'Dominion'
        self.image = 'Province.png'
        self.kingdom_card = False
        self.type = ['victory']
        self.subtype = None
        self.price = 8
        self.value = 6
