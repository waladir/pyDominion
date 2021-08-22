from libs.classes.card import Card

class Mill(Card):
    def __init__(self):
        self.id = 'mill'
        self.name = 'Mlýn' 
        self.name_en = 'Mill'
        self.expansion = 'Intrigue2nd'
        self.image = 'Mill.png'
        self.kingdom_card = True
        self.type = ['action', 'victory']
        self.subtype = None
        self.price = 4
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

        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 2
                self.action.phase = 'select'
                self.desk.draw()                
            else:
                self.action.cleanup()  
        else:
            if len(self.action.selected_cards) > 0:
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.player.coalesce_hand()
                    self.player.put_card_to_discard(card)
                if len(self.action.selected_cards) == 2:
                    self.player.treasure = self.player.treasure + 2
                self.desk.draw()                

            self.action.cleanup()
            self.desk.changed.append('players_discard')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.draw()
