from libs.classes.card import Card

class Festival(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'festival'
        self.name = 'Jarmark' 
        self.name_en = 'Festival'
        self.expansion = 'Dominion'
        self.image = 'Festival.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

    def do_action(self):
        self.player.actions = self.player.actions + 2
        self.player.buys = self.player.buys + 1
        self.player.treasure = self.player.treasure + 2
        self.desk.changed.append('info')
        self.desk.draw()
        self.action.cleanup()
