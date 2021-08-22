from libs.classes.card import Card

class Upgrade(Card):
    def __init__(self):
        self.id = 'upgrade'
        self.name = 'Pokrok' 
        self.name_en = 'Upgrade'
        self.expansion = 'Intrigue2nd'
        self.image = 'Upgrade.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.card_price = -1
        self.subphase = ''

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')            
            self.desk.draw()
     
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.subphase = 'to_trash'
                self.desk.draw()                
            else:
                self.action.cleanup()               
        else:
            if self.action.phase == 'select' and self.subphase == 'to_trash':
                if len(self.action.selected_cards) > 0:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.card_price = card.price + 1
                        self.player.coalesce_hand()
                        self.desk.trash.add_card(card)
                        self.desk.changed.append('players_hand')        
                        self.desk.changed.append('trash')        
                        self.desk.draw()                
                    if self.card_price > 0:
                        self.action.selectable_cards = []
                        self.action.selected_cards = {}
                        piles = self.desk.basic_piles + self.desk.kingdom_piles
                        for pile in piles:
                            card = pile.top_card()
                            if card is not None and card.price == self.card_price:
                                self.action.selectable_cards.append(card)
                        if len(self.action.selectable_cards) > 0:
                            self.action.to_select = 1
                            self.action.phase = 'select'
                            self.subphase = 'to_gain'
                            self.desk.changed.append('basic')        
                            self.desk.changed.append('kingdom')        
                            self.desk.draw()                
                        else:
                            self.action.cleanup()               
            elif self.action.phase == 'select' and self.subphase == 'to_gain':
                if len(self.action.selected_cards) > 0:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.player.put_card_to_discard(card)
                    self.action.cleanup()
                    self.desk.changed.append('players_discard')
                    self.desk.draw() 