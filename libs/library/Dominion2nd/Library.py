from libs.classes.card import Card

class Library(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'library'
        self.name = 'Sklepení' 
        self.name_en = 'Library'
        self.expansion = 'Dominion2nd'
        self.image = 'Library.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.phase = 'select_cards'
        self.skipped_cards = []

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_cards':
            hand_count = len(self.player.hand)
            skip = False
            while hand_count < 7 and len(self.player.deck.cards) + len(self.player.discard.cards) > 0 and skip == False:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    if card is not None:
                        create_event(self.player.game.get_me(), 'draw_card', { 'player' : self.player.name, 'count' : 1 }, self.player.game.get_other_players_names())
                        if 'action' in card.type:
                            self.desk.put_card_to_select_area(card)
                            self.desk.select_area_type = 'select_action'
                            self.desk.select_area = True
                            self.desk.select_area_label = 'Označ akční kartu, pokud ji chceš dát stranou nebo ukonči vyběr karet, pokud ji chceš dát do ruky'
                            selectable_piles = []
                            for pile in self.desk.select_area_piles:
                                selectable_piles.append(pile)
                            self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                            self.phase = 'choose_to_skip'
                            self.desk.changed.append('players_deck')
                            self.desk.changed.append('select_area')
                            self.desk.draw()
                            skip = True
                        else:
                            self.desk.select_area = False
                            self.player.put_card_to_hand(card)
                            self.desk.changed.append('players_hand')
                            self.desk.changed.append('players_deck')
                            self.desk.draw()                        
            hand_count = len(self.player.hand)
            if  hand_count >= 7 or len(self.player.deck.cards) + len(self.player.discard.cards) <= 0:
                self.desk.select_area = False
                for card in self.skipped_cards:               
                    self.player.put_card_to_discard(card)
                self.action.cleanup()
                self.desk.changed.append('select_area')
                self.desk.changed.append('players_discard')                
                self.desk.draw()
        elif self.phase == 'choose_to_skip':
            if len(self.desk.selected_piles) == 0:
                for pile in self.desk.selectable_piles:
                    card = pile.get_top_card()
                    self.player.put_card_to_hand(card)  

                    self.desk.coalesce_select_area()                                        
                self.desk.changed.append('players_hand')                
                self.desk.changed.append('select_area')
                self.desk.draw()                    
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.skipped_cards.append(card)
                self.desk.coalesce_select_area()                    
                self.desk.changed.append('select_area')
                self.desk.draw()                    
            hand_count = len(self.player.hand)
            if hand_count < 7 and len(self.player.deck.cards) + len(self.player.discard.cards) > 0:    
                self.desk.clear_select()
                self.desk.select_area = False
                self.phase = 'select_cards'
                self.do_action()
            else:
                self.desk.select_area = False
                for card in self.skipped_cards:               
                    self.player.put_card_to_discard(card)
                    create_event(self.player.game.get_me(), 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.action.cleanup()
                self.desk.changed.append('players_discard')                
                self.desk.draw()

