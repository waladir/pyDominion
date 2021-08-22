from libs.classes.card import Card

class Conspirator(Card):
    def __init__(self):
        self.id = 'conspirator'
        self.name = 'Spiklenec' 
        self.name_en = 'Conspirator'
        self.expansion = 'Intrigue2nd'
        self.image = 'Conspirator.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

    def do_action(self):
        actions_played = 0
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.treasure = self.player.treasure + 2            
            self.desk.changed.append('info')            
            for pile in self.desk.play_area_piles:
                card = pile.top_card()
                if 'action' in card.type:
                    actions_played = actions_played + len(pile.cards)
            if actions_played >= 3:
                self.player.actions = self.player.actions + 1
                self.player.move_cards_from_deck_to_hand(1)
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_hand')            
                self.desk.changed.append('info') 
            self.desk.draw()        
        self.action.cleanup()     
