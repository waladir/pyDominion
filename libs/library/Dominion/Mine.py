from libs.classes.card import Card

class Mine(Card):
    def __init__(self):
        self.id = 'mine'
        self.name = 'Důl' 
        self.name_en = 'Mine'
        self.expansion = 'Dominion'
        self.image = 'Mine.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.card_price = -1

    def do_action(self):
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                if 'treasure' in card.type:
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.desk.draw()
            else:
                self.action.cleanup()
        else:
            if len(self.action.selected_cards) == 0:
                self.action.cleanup()
            else:
                if self.card_price == -1:        
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.card_price = card.price + 3 
                        self.desk.trash.add_card(card)
                    self.player.coalesce_hand()
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('trash')
                    self.desk.draw()                        
                    piles = self.desk.basic_piles
                    self.action.selectable_cards = []
                    self.action.selected_cards = {}
                    for pile in piles:
                        card = pile.top_card()
                        if 'treasure' in card.type and card.price <= self.card_price:
                            self.action.selectable_cards.append(card)
                    if len(self.action.selectable_cards) > 0:
                        self.action.to_select = 1
                    self.desk.redraw_borders()                        
                else:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.player.put_card_to_discard(card) 
                    self.desk.price = -1
                    self.action.cleanup()
                    self.player.coalesce_hand()
                    self.desk.changed.append('players_discard')
                    self.desk.draw()    

