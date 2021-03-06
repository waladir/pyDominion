from libs.classes.card import Card

class Harem(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'harem'
        self.name = 'Harém' 
        self.name_en = 'Harem'
        self.expansion = 'Intrigue'
        self.image = 'Harem.png'
        self.kingdom_card = True
        self.type = ['treasure', 'victory']
        self.subtype = None
        self.price = 6
        self.value = 2

    def do_action(self):
        self.player.treasure = self.player.treasure + 2            
        self.desk.changed.append('info')
        self.desk.draw()
        self.action.cleanup()   
