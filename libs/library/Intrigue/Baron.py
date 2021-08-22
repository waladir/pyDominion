from libs.classes.card import Card

class Baron(Card):
    def __init__(self):
        self.id = 'minion'
        self.name = 'Baron' 
        self.name_en = 'Baron'
        self.expansion = 'Intrigue'
        self.image = 'Baron.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.buys = self.player.buys + 1
            self.desk.changed.append('info')
            self.desk.draw()        

        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                if card.name == 'Statek':
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.desk.draw()
            else:
                self.gain_estate()
                self.action.cleanup()
        else:
            if len(self.action.selected_cards) == 0:
                self.gain_estate()
                self.action.cleanup()
            else:
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.player.treasure = self.player.treasure + 4
                    self.player.put_card_to_discard(card)
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('players_discard')
                self.desk.changed.append('info')
                self.desk.draw()
                self.action.cleanup()                    

    def gain_estate(self):
        piles = self.desk.basic_piles
        for pile in piles:
            card = pile.top_card()
            if card.name == 'Statek':
                card = pile.get_top_card()
                if card is not None:
                    self.player.put_card_to_discard(card)
        self.desk.changed.append('basic')                    
        self.desk.changed.append('players_discard') 
        self.desk.draw()                   

