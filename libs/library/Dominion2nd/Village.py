from libs.classes.card import Card

class Village(Card):
    def __init__(self):
        self.id = 'village'
        self.name = 'Vesnice' 
        self.name_en = 'Village'
        self.expansion = 'Dominion2nd'
        self.image = 'Village.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 2            
            self.desk.changed.append('info')
            self.desk.draw()  
        self.action.cleanup()      
