from libs.classes.card import Card
from libs.classes.trigger import Trigger

class Merchant(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'merchant'
        self.name = 'Obchodnice' 
        self.name_en = 'Merchant'
        self.expansion = 'Dominion2nd'
        self.image = 'Merchant.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

        self.trigger = None

    def do_action(self):
        self.player.move_cards_from_deck_to_hand(1)
        self.desk.changed.append('players_deck')
        self.desk.changed.append('players_hand')            
        self.player.actions = self.player.actions + 1
        self.desk.changed.append('info')
        self.trigger = Trigger(self, self.player, 'card_played', 'end_of_round')
        self.trigger.duration_end = self.player.game.round
        self.desk.draw()        
        self.action.cleanup()     

    def do_trigger_start(self):
        card = self.trigger.card_played
        if card.name == 'Stříbrňák':
            self.player.treasure = self.player.treasure + 1
        self.desk.triggers.remove(self.trigger)
        del self.trigger            

    def do_trigger_end(self):
        pass