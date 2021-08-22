from libs.classes.card import Card

class Smithy(Card):
    def __init__(self):
        self.id = 'smithy'
        self.name = 'Kovárna' 
        self.name_en = 'Smithy'
        self.expansion = 'Dominion2nd'
        self.image = 'Smithy.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(3)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
        self.action.cleanup()             