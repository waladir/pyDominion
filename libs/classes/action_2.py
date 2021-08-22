class Action():
    def do_add_treasure(self, val):
        if self.player.active_card == None:
            self.player.treasure = self.player.treasure + val
            self.desk.changed.append('info')
            self.desk.draw()

    def do_add_actions(self, val):
        if self.player.active_card == None:
            self.player.actions = self.player.actions + val
            self.desk.changed.append('info')
            self.desk.draw()

    def do_add_buys(self, val):
        if self.player.active_card == None:
            self.player.buys = self.player.buys + val
            self.desk.changed.append('info')
            self.desk.draw()

    def do_add_cards(self, val):
        if self.player.active_card == None:
            self.player.move_cards_from_deck_to_hand(val)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
        
    def do_workshop(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1:
            piles = self.desk.basic_piles + self.desk.kingdom_piles
            for pile in piles:
                card = pile.top_card()
                if card.price <= 4:
                    self.player.selectable_cards.append(card)
            if len(self.player.selectable_cards) > 0:
                self.player.to_select = 1
        elif self.player.to_select == -2:
            for selected in self.player.selected_cards:
                pile = self.player.selected_cards[selected]
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)  
            self.cleanup()
            self.desk.changed.append('basic')
            self.desk.changed.append('kingdom')
            self.desk.changed.append('players_discard')
            self.desk.draw()

    def do_cellar(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1:
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.player.selectable_cards.append(card)
            if len(self.player.selectable_cards) > 0:
                self.player.to_select = 999
        elif self.player.to_select == -2:
            for selected in self.player.selected_cards:
                pile = self.player.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_discard(card)  
                self.player.move_cards_from_deck_to_hand(1)
            self.cleanup()
            self.player.coalesce_hand()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.desk.draw()

    def do_chapel(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1:
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.player.selectable_cards.append(card)
            if len(self.player.selectable_cards) > 0:
                self.player.to_select = 4
        elif self.player.to_select == -2:
            for selected in self.player.selected_cards:
                pile = self.player.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.desk.trash.add_card(card)                
            self.player.coalesce_hand()
            self.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('trash')
            self.desk.draw()

    # def do_harbinger(self, val):
    #     self.player.active_card = self.card
    #     if self.player.to_select == -1:
    #         for i in range(len(self.player.discard.cards)):
    #             card = self.player.discard.get_top_card()
    #             self.player.selectable_cards.append(card)
    #             self.desk.put_card_to_select_area(card)
    #         if len(self.player.selectable_cards) > 0:
    #             self.player.to_select = 1
    #             self.desk.select_area_type = 'select_card'
    #             self.desk.select_area = True
    #             self.desk.changed.append('select_area')
    #             self.desk.changed.append('players_discard')
    #             self.desk.draw()
    #     elif self.player.to_select == -2:
    #         for selected in self.player.selected_cards:
    #             pile = self.player.selected_cards[selected]
    #             card = pile.get_top_card()
    #             self.desk.coalesce_select_area()
    #             self.player.put_card_to_deck(card)               
    #         for card in self.player.selectable_cards:
    #             self.player.put_card_to_discard(card)               
    #         self.cleanup()
    #         self.desk.changed.append('players_deck')
    #         self.desk.changed.append('players_discard')
    #         self.desk.draw()


    # def do_vassal(self, val):
    #     self.player.active_card = self.card
    #     if self.player.to_select == -1:
    #         cards = self.player.get_cards_from_deck(1)
    #         for card in cards:
    #             if card.type == 'action':
    #                 self.player.selectable_cards.append(card)
    #                 self.desk.put_card_to_select_area(card)
    #                 self.player.to_select = 1
    #                 self.desk.select_area_type = 'play_action'
    #                 self.desk.select_area = True
    #                 self.desk.changed.append('select_area')
    #                 self.desk.draw()  
    #             else:
    #                 self.player.put_card_to_discard(card)
    #                 self.desk.changed.append('players_discard')
    #                 self.desk.draw()  
    #     elif self.player.to_select == -2:
    #         if len(self.player.selected_cards) == 0:
    #             for pile in self.desk.select_area_piles:
    #                 card = pile.get_top_card()
    #                 self.desk.coalesce_select_area()
    #                 self.player.put_card_to_discard(card)     
    #             self.cleanup()
    #             self.desk.changed.append('select_area')
    #             self.desk.changed.append('players_discard')
    #             self.desk.draw()
    #         else:
    #             for selected in self.player.selected_cards:
    #                 pile = self.player.selected_cards[selected]
    #                 card = pile.get_top_card()
    #                 self.desk.coalesce_select_area()
    #                 self.desk.put_card_to_play_area(card) 
    #                 self.player.active_card = None
    #                 self.player.selectable_cards = []
    #                 self.player.selected_cards = {}
    #                 self.desk.select_area = False
    #                 self.desk.select_area_piles = []
    #                 self.player.to_select = -1
    #                 self.player.action(self.desk, card)
    #                 self.desk.changed.append('play_area')
    #                 self.desk.draw()

    def do_moneylander(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1:
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                if card.name == 'Měďák':
                    self.player.selectable_cards.append(card)
            if len(self.player.selectable_cards) > 0:
                self.player.to_select = 1
        elif self.player.to_select == -2:
            for selected in self.player.selected_cards:
                pile = self.player.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.desk.trash.add_card(card)
                self.player.treasure = self.player.treasure + 3
            self.player.coalesce_hand()
            self.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.changed.append('trash')
            self.desk.draw()  

    def do_remodel(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1:
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.player.selectable_cards.append(card)
            if len(self.player.selectable_cards) > 0:
                self.player.to_select = 1
                self.desk.draw()
        elif self.player.to_select == -2:
            if len(self.player.selected_cards) == 0:
                self.cleanup()
            else:
                if self.desk.price is None:        
                    for selected in self.player.selected_cards:
                        pile = self.player.selected_cards[selected]
                        card = pile.get_top_card()
                        self.desk.price = card.price + 2 
                        self.desk.trash.add_card(card)
                    self.player.coalesce_hand()
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('trash')
                    self.desk.draw()                        

                    piles = self.desk.basic_piles + self.desk.kingdom_piles
                    self.player.selectable_cards = []
                    self.player.selected_cards = {}
                    for pile in piles:
                        card = pile.top_card()
                        if card.price <= self.desk.price:
                            self.player.selectable_cards.append(card)
                    if len(self.player.selectable_cards) > 0:
                        self.player.to_select = 1
                    self.player.coalesce_hand()
                    self.desk.redraw_borders()                        
                else:
                    for selected in self.player.selected_cards:
                        pile = self.player.selected_cards[selected]
                        card = pile.get_top_card()
                        self.player.put_card_to_discard(card) 
                    self.desk.price = None
                    self.cleanup()
                    self.desk.changed.append('players_discard')
                    self.desk.changed.append('trash')
                    self.desk.draw()                    

    def do_throne_room(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1:
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                if card.type == 'action':
                    self.player.selectable_cards.append(card)
            if len(self.player.selectable_cards) > 0:
                self.player.to_select = 1
        elif self.player.to_select == -2:
            if len(self.player.selected_cards) == 0:
                self.cleanup()
            else:
                for selected in self.player.selected_cards:
                    pile = self.player.selected_cards[selected]
                    card = pile.get_top_card()
                    self.player.coalesce_hand()
                    self.desk.put_card_to_play_area(card) 
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('play_area')
                    self.desk.draw()
                    for i in range(2):
                        self.player.active_card = None
                        self.player.selectable_cards = []
                        self.player.selected_cards = {}
                        self.desk.select_area = False
                        self.desk.select_area_piles = []
                        self.player.to_select = -1
                        self.player.action(self.desk, card)
                self.cleanup()

    def do_library(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1 or self.player.to_select > 0:
            hand_count = len(self.player.hand)
            skip = False
            while hand_count < 7 and len(self.player.deck.cards) + len(self.player.discard.cards) > 0 and skip == False:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    if card.type == 'action':
                        self.player.selectable_cards.append(card)
                        self.desk.put_card_to_select_area(card)
                        self.player.to_select = 1
                        self.desk.select_area_type = 'select_action'
                        self.desk.select_area = True
                        self.desk.changed.append('players_deck')
                        self.desk.changed.append('select_area')
                        self.desk.draw()
                        skip = True
                    else:
                        self.desk.select_area = False
                        self.player.put_card_to_hand(card)
                        self.player.coalesce_hand()
                        self.desk.changed.append('players_hand')
                        self.desk.changed.append('players_deck')
                        self.desk.draw()                        
            if  hand_count >= 7 or len(self.player.deck.cards) + len(self.player.discard.cards) <= 0:
                self.desk.select_area = False
                for card in self.player.skipped_cards:               
                    self.player.put_card_to_discard(card)
                self.cleanup()
                self.desk.changed.append('select_area')
                self.desk.changed.append('players_discard')                
                self.desk.draw()
        elif self.player.to_select == -2:
            if len(self.player.selected_cards) == 0:
                for card in self.player.selectable_cards:
                    self.player.put_card_to_hand(card)                 
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')                
                self.desk.draw()                    
            else:
                for selected in self.player.selected_cards:
                    pile = self.player.selected_cards[selected]
                    card = pile.get_top_card()
                    self.player.skipped_cards.append(card)
                self.desk.coalesce_select_area()                    
                self.desk.changed.append('select_area')
                self.desk.draw()                    

            hand_count = len(self.player.hand)
            if hand_count < 7 and len(self.player.deck.cards) + len(self.player.discard.cards) > 0:    
                self.player.selectable_cards = []
                self.player.selected_cards = {}
                self.desk.select_area = False
                self.desk.select_area_piles = []
                self.player.to_select = -1
                self.player.action(self.desk, card)
            else:
                self.desk.select_area = False
                for card in self.player.skipped_cards:               
                    self.player.put_card_to_discard(card)
                self.cleanup()
                self.desk.changed.append('players_discard')                
                self.desk.draw()

    def do_mine(self, val):
        self.player.active_card = self.card
        if self.player.to_select == -1:
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                if card.type == 'treasure':
                    self.player.selectable_cards.append(card)
            if len(self.player.selectable_cards) > 0:
                self.player.to_select = 1
        elif self.player.to_select == -2:
            if len(self.player.selected_cards) == 0:
                self.cleanup()
            else:
                if self.desk.price is None:        
                    for selected in self.player.selected_cards:
                        pile = self.player.selected_cards[selected]
                        card = pile.get_top_card()
                        self.desk.price = card.price + 3 
                        self.desk.trash.add_card(card)
                    self.player.coalesce_hand()
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('trash')
                    self.desk.draw()                        
                    piles = self.desk.basic_piles
                    self.player.selectable_cards = []
                    self.player.selected_cards = {}
                    for pile in piles:
                        card = pile.top_card()
                        if card.type == 'treasure' and card.price <= self.desk.price:
                            self.player.selectable_cards.append(card)
                    if len(self.player.selectable_cards) > 0:
                        self.player.to_select = 1
                    self.desk.redraw_borders()                        
                else:
                    for selected in self.player.selected_cards:
                        pile = self.player.selected_cards[selected]
                        card = pile.get_top_card()
                        self.player.put_card_to_discard(card) 
                    self.desk.price = None
                    self.cleanup()
                    self.player.coalesce_hand()
                    self.desk.changed.append('players_discard')
                    self.desk.draw()    

    # def do_sentry(self, val):
    #     self.player.active_card = self.card
    #     if self.player.to_select == -1:
    #         cards = self.player.get_cards_from_deck(2)
    #         for card in cards:
    #             self.player.selectable_cards.append(card)
    #             self.desk.put_card_to_select_area(card)
    #             self.player.to_select = 1
    #             self.desk.select_area_type = 'select_card'
    #             self.desk.select_area = True
    #         self.desk.changed.append('select_area')
    #         self.desk.draw()  
    #     elif self.player.to_select == -2:
    #         if len(self.player.selected_cards) == 1:
    #             self.player.selectable_piles = [self.player.deck, self.player.discard, self.desk.trash]
    #             self.desk.draw()

    def do_to_do(self, val):
        pass

    def cleanup(self):
        self.player.active_card = None
        self.player.selectable_cards = []
        self.player.selected_cards = {}
        self.desk.select_area = False
        self.desk.select_area_piles = []
        self.player.to_select = -1

    def do_action(self, action_name, val):
        eval('self.do_' +action_name + '(' + str(val) + ')')  
