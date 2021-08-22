from libs.classes.card import Card

class Secret_Passage(Card):
    def __init__(self):
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

        self.subphase = ''
        self.card_to_place = None

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')            
            self.player.actions = self.player.actions + 1           
            self.desk.changed.append('info')

        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.action.select_cards = 'mandatory'
                self.subphase = 'select_card'             
                self.desk.draw()   
            else:
                self.action.cleanup()
        else:
            if self.subphase == 'select_card':
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    self.card_to_place = pile.get_top_card()
                self.player.coalesce_hand()  
                self.desk.redraw_borders()                  
                if self.card_to_place is not None:
                    self.action.selectable_cards = []
                    self.action.selected_cards = {}
                    for card in self.player.deck.cards:
                        self.action.to_select = 1
                        self.desk.put_card_to_select_area(card)
                        self.action.selectable_cards.append(card)
                if len(self.action.selectable_cards) > 0:
                    self.action.select_cards = 'mandatory'
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_hide_cards = True
                    self.desk.select_area_label = 'Označ kartu z dobíracího balíčku, za kterou vybranou kartu vložíš. Pokud chceš kartu umístit navrch dobíracího balíčku, označ dobírací balíček'
                    self.subphase = 'self_resolution'
                    self.desk.changed.append('select_area')
                else:
                    self.desk.select_area = False
                self.action.selectable_piles.append(self.player.deck)
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_hand')
                self.action.to_select = 1
                self.action.select_cards = 'mandatory'
                self.subphase = 'place_card'             
                self.desk.draw()
            elif self.subphase == 'place_card':
                if len(self.action.selected_piles):
                    self.player.put_card_to_deck(self.card_to_place)
                else:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        self.player.deck.cards.insert(pile.position + 1, self.card_to_place)
                self.desk.select_area = False
                self.desk.changed.append('players_deck')
                self.desk.changed.append('play_area')
                self.desk.changed.append('info')
                self.action.cleanup()
                self.desk.draw()



