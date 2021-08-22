from libs.classes.card import Card

class Laboratory(Card):
    def __init__(self):
        self.id = 'laboratory'
        self.name = 'Laboratoř' 
        self.name_en = 'Laboratory'
        self.expansion = 'Dominion2nd'
        self.image = 'Laboratory.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False   
            self.player.move_cards_from_deck_to_hand(2)
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.draw()
        self.action.cleanup()
