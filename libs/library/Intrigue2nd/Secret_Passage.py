from libs.classes.card import Card

class Secret_Passage(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'secret_passage'
        self.name = 'Tajný průchod' 
        self.name_en = 'Secret_Passage'
        self.expansion = 'Intrigue2nd'
        self.image = 'Secret_Passage.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'select_card_to_return_to_deck'
        self.card_to_place = None

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_card_to_return_to_deck':
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')            
            self.player.actions = self.player.actions + 1           
            self.desk.changed.append('info')
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.add_message('Vyber kartu, kterou dáš zpět do dobíracího balíčku')
                self.phase = 'choose_card'
                self.desk.draw()   
            else:
                self.action.cleanup()
        elif self.phase == 'choose_card':
            for pile in self.desk.selected_piles:
                self.card_to_place = pile.get_top_card()
            self.player.coalesce_hand()  
            self.desk.redraw_borders()                  
            if self.card_to_place is not None:
                selectable_piles = []
                self.desk.clear_select()
                for card in self.player.deck.cards:
                    self.action.to_select = 1
                    self.desk.put_card_to_select_area(card)
                for pile in self.desk.select_area_piles:
                    selectable_piles.append(pile)
                if len(selectable_piles) > 0:
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_hide_cards = True
                    self.desk.select_area_label = 'Označ kartu z dobíracího balíčku, za kterou vybranou kartu vložíš. Pokud chceš kartu umístit navrch dobíracího balíčku, označ dobírací balíček'
                    self.desk.changed.append('select_area')
                else:
                    self.desk.select_area = False
                selectable_piles.append(self.player.deck)
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_hand')
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'place_card'             
                self.desk.draw()
        elif self.phase == 'place_card':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    if pile == self.player.deck:
                        self.player.put_card_to_deck(self.card_to_place)
                    else:
                        self.player.deck.cards.insert(pile.position + 1, self.card_to_place)
                    create_event(self, 'move_card_from_hand_to_deck', { 'player' : self.player.name }, self.game.get_other_players_names())
            self.desk.select_area = False
            self.desk.changed.append('players_deck')
            self.desk.changed.append('play_area')
            self.desk.changed.append('info')
            self.action.cleanup()
            self.desk.draw()
