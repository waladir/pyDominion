from libs.classes.card import Card

class Steward(Card):
    def __init__(self):
        self.id = 'steward'
        self.name = 'Správce' 
        self.name_en = 'Steward'
        self.expansion = 'Intrigue'
        self.image = 'Steward.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.select_to_trash = False

    def do_action(self):
        if self.action.phase != 'select':
            if len(self.player.deck.cards) + len(self.player.discard.cards) > 0:
                self.action.selectable_piles.append(self.player.deck)
            self.action.selectable_piles.append(self.desk.trash)
            self.action.to_select = 1
            self.action.selectable_info = ['treasure']
            self.action.phase = 'select'
            self.desk.draw()                
        else:
            if self.select_to_trash == False:
                if len(self.action.selected_piles) > 0:
                    for pile in self.action.selected_piles:
                        if pile == self.player.deck:
                            cards = self.player.get_cards_from_deck(2)
                            for card in cards:
                                self.player.put_card_to_hand(card)   
                        else:
                            self.action.selectable_piles = []
                            self.action.selectable_info = []
                            self.action.selected_piles = []
                            self.action.selected_info = []
                            piles = self.player.hand
                            for pile in piles:
                                card = pile.top_card()
                                self.action.selectable_cards.append(card)
                            if len(self.action.selectable_cards) > 0:
                                self.action.to_select = 2
                                self.action.phase = 'select'
                                self.select_to_trash = True
                                self.desk.draw()                
                if len(self.action.selected_info) > 0:
                    for section in self.action.selected_info:
                        if section == 'treasure':
                            self.player.treasure = self.player.treasure + 2
            if self.select_to_trash == False:
                self.action.cleanup()
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_hand')
                self.desk.changed.append('info')
                self.desk.draw()
            else:
                if self.action.to_select == -1:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.player.coalesce_hand()
                        self.desk.trash.add_card(card)
                    self.action.cleanup()
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('info')
                    self.desk.changed.append('trash')
                    self.desk.draw()                      
