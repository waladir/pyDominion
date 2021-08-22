from libs.classes.card import Card

class Chapel(Card):
    def __init__(self):
        self.id = 'chapel'
        self.name = 'Kaple' 
        self.name_en = 'Chapel'
        self.expansion = 'Dominion'
        self.image = 'Chapel.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0


    def do_action(self):
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 4
                self.action.phase = 'select'
                self.desk.draw()
            else:
                self.action.cleanup()
        else:
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.desk.trash.add_card(card)                
            self.player.coalesce_hand()
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('trash')
            self.desk.draw()

