from libs.classes.card import Card
from libs.classes.trigger import Trigger

class Coppersmith(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'coppersmith'
        self.name = 'Měditepec' 
        self.name_en = 'Coppersmith'
        self.expansion = 'Intrigue'
        self.image = 'Coppersmith.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.trigger = None

    def do_action(self):
        self.trigger = Trigger(self, self.player, 'card_played', 'end_of_round')
        self.trigger.duration_end = self.player.game.round
        self.desk.draw()        
        self.action.cleanup()     

    def do_trigger_start(self):
        card = self.trigger.card_played
        if card.name == 'Měďák':
            card.value = card.value + 1

    def do_trigger_end(self):
        card = self.trigger.card_played
        if card.name == 'Měďák':
            card.value = card.value - 1
