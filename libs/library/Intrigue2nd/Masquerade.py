from libs.classes.card import Card

class Masquerade(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'masquerade'
        self.name = 'Maškary' 
        self.name_en = 'Masquerade'
        self.expansion = 'Intrigue2nd'
        self.image = 'Masquerade.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        from libs.events import create_event
        to_discard = []
        if self.phase == 'action':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            self.action.cleanup()
