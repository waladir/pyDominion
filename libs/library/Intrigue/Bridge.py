from libs.classes.card import Card
from libs.classes.trigger import Trigger

class Bridge(Card):
    def __init__(self):
        self.id = 'bridge'
        self.name = 'Most' 
        self.name_en = 'Bridge'
        self.expansion = 'Intrigue'
        self.image = 'Bridge.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.trigger = None        

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.buys = self.player.buys + 1
            self.player.treasure = self.player.treasure + 1
            self.trigger = Trigger(self, self.player, 'set_price', 'end_of_round')
            self.trigger.duration_end = self.player.game.round            
            self.action.cleanup()
            self.do_trigger_start()
            self.desk.changed.append('info')
            self.desk.draw()

    def do_trigger_start(self):
        for pile in  self.desk.get_all_piles():        
            for card in pile.cards:
                if card.price > 0:
                    card.price = card.price - 1

    def do_trigger_end(self):
        for pile in  self.desk.get_all_piles():        
            for card in pile.cards:
                card = pile.top_card()
                if card.price > 0:
                    card.price = card.price + 1
    