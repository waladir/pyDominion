from libs.classes.card import Card

class Lurker(Card):
    def __init__(self):
        self.id = 'lurker'
        self.name = 'Zákeřník' 
        self.name_en = 'Lurker'
        self.expansion = 'Intrigue2nd'
        self.image = 'Lurker.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.subphase = ''

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')            
            self.desk.draw()        

        if self.action.phase != 'select':
            if len(self.desk.trash.cards)  > 0:
                self.action.selectable_piles.append(self.desk.trash)
            piles = self.desk.basic_piles + self.desk.kingdom_piles
            for pile in piles:
                card = pile.top_card()
                if 'action' in card.type:
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.action.select_cards = 'mandatory'
                self.subphase = 'choose_action'
                self.desk.draw()                
            else:
                self.action.cleanup()
                self.desk.draw()                
        else:

            if self.subphase == 'choose_action':
                if len(self.action.selected_piles) > 0:
                    self.action.selectable_piles = []
                    self.action.selectable_cards = []
                    self.action.selected_piles = []
                    self.action.selected_cards = {}
                    for card in self.desk.trash.cards:
                        if card is not None and 'action' in card.type:
                            self.desk.put_card_to_select_area(card)
                            self.action.selectable_cards.append(card)
                    if len(self.action.selectable_cards) > 0:
                        self.action.to_select = 1
                        self.action.select_cards = 'mandatory'
                        self.desk.select_area_type = 'select_action'
                        self.desk.select_area = True
                        self.desk.select_area_label = 'Vyber akční kartu ze smetiště, kterou získáš'
                        self.action.phase = 'select'
                        self.subphase = 'gain_card'
                        self.desk.changed.append('select_area')
                        self.desk.draw()
                    else:
                        self.action.cleanup()
                        self.desk.draw()
                if len(self.action.selected_cards) > 0:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.desk.trash.add_card(card) 
                        self.desk.changed.append('kingdom')
                        self.desk.changed.append('basic')
                        self.desk.changed.append('trash')
                    self.action.cleanup()
                    self.desk.changed.append('info')
                    self.desk.draw()
            elif self.subphase == 'gain_card':
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.player.put_card_to_discard(card)
                    self.desk.coalesce_select_area()
                self.desk.changed.append('players_discard')
                for card in self.action.selectable_cards:
                    self.desk.trash.add_card(card) 
                self.desk.changed.append('trash')
                self.desk.select_area = False
                self.player.phase = 'action'
                self.desk.changed.append('info')                
                self.desk.changed.append('play_area')
                self.action.cleanup()
                self.desk.draw()                