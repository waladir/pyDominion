from libs.classes.card import Card

class Market(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'market'
        self.name = 'Trh' 
        self.name_en = 'Market'
        self.expansion = 'Dominion'
        self.image = 'Market.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

    def do_action(self):
        self.player.move_cards_from_deck_to_hand(1)
        self.desk.changed.append('players_deck')
        self.desk.changed.append('players_hand')
        self.player.actions = self.player.actions + 1
        self.player.buys = self.player.buys + 1
        self.player.treasure = self.player.treasure + 1
        self.desk.changed.append('info')
        self.desk.draw()
        self.action.cleanup()
