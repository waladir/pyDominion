from libs.classes.card import Card

class Cellar(Card):
    def __init__(self):
        self.id = 'cellar'
        self.name = 'Sklepení' 
        self.name_en = 'Cellar'
        self.expansion = 'Dominion'
        self.image = 'Cellar.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 999
                self.action.phase = 'select'
                self.desk.draw()                
            else:
                self.action.cleanup()
        else:
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_discard(card)  
                self.player.move_cards_from_deck_to_hand(1)
            self.action.cleanup()
            self.player.coalesce_hand()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.desk.draw()

