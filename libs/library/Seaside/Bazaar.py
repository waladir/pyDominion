from libs.classes.card import Card

class Bazaar(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'bazaar'
        self.name = 'Bazar' 
        self.name_en = 'Bazaar'
        self.expansion = 'Seaside'
        self.image = 'Bazaar.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

    def do_action(self):
        self.player.move_cards_from_deck_to_hand(1)
        self.desk.changed.append('players_deck')
        self.desk.changed.append('players_hand')
        self.player.actions = self.player.actions + 2
        self.player.treasure = self.player.treasure + 1
        self.desk.changed.append('info')
        self.desk.draw()
        self.action.cleanup()
