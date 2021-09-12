from libs.classes.card import Card

class Pearl_Diver(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'pearl_diver'
        self.name = 'Lovec perel' 
        self.name_en = 'Pearl_Diver'
        self.expansion = 'Seaside'
        self.image = 'Pearl_Diver.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

    def do_action(self):
        self.player.move_cards_from_deck_to_hand(1)
        self.desk.changed.append('players_deck')
        self.desk.changed.append('players_hand')
        self.player.actions = self.player.actions + 1
        self.desk.changed.append('info')

        print(self.player.deck.cards)

        self.desk.draw()
        self.action.cleanup()
