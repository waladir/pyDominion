from libs.classes.card import Card

class Woodcutter(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'woodcutter'
        self.name = 'Dřevorubec' 
        self.name_en = 'Woodcutter'
        self.expansion = 'Dominion'
        self.image = 'Woodcutter.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

    def do_action(self):
        self.player.buys = self.player.buys + 1
        self.player.treasure = self.player.treasure + 2
        self.desk.changed.append('info')
        self.desk.draw()        
        self.action.cleanup()