from libs.classes.card import Card

class Great_Hall(Card):
    def __init__(self):
        self.id = 'great_hall'
        self.name = 'Velký sál' 
        self.name_en = 'Great_Hall'
        self.expansion = 'Intrigue'
        self.image = 'Great_Hall.png'
        self.kingdom_card = True
        self.type = ['action', 'victory']
        self.subtype = None
        self.price = 3
        self.value = 1

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1            
            self.desk.changed.append('info')
            self.desk.draw()
        self.action.cleanup()     
