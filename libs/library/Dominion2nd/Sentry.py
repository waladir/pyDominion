from libs.classes.card import Card

class Sentry(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'sentry'
        self.name = 'Stráž' 
        self.name_en = 'Sentry'
        self.expansion = 'Dominion2nd'
        self.image = 'Sentry.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0
        
        self.cards_to_deal_with = []
        self.phase = 'select_top_cards'

    def do_action(self):
        from libs.events import create_event        
        if self.phase == 'select_top_cards':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')                
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()
            cards = self.player.get_cards_from_deck(2)
            selectable_piles = []
            for card in cards:
                if card is not None:
                    self.cards_to_deal_with.append(card)
                    self.desk.put_card_to_select_area(card)
                    create_event(self.player.game.get_me(), 'draw_card', { 'player' : self.player.name, 'count' : 1 }, self.player.game.get_other_players_names())          
            for pile in self.desk.select_area_piles:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Vyber kartu'
                self.phase = 'choose_action'
                self.desk.changed.append('select_area')
                self.desk.changed.append('players_deck')
                self.desk.draw()
            else:
                self.action.cleanup()
                self.desk.changed.append('players_deck')
        elif self.phase == 'choose_action':
            if len(self.desk.selected_piles) > 0:
                selected_piles = self.desk.selected_piles
                self.desk.select_area_label = 'Označ jestli má být vrácená na dobírací balíček, odložená na odkládací balíček nebo zahozená na smetiště'
                self.desk.changed.append('select_area') 
                self.desk.clear_select()
                selectable_piles = []
                selectable_piles.append(self.player.deck)
                selectable_piles.append(self.player.discard)
                selectable_piles.append(self.desk.trash)
                for pile in selected_piles:
                    selectable_piles.append(pile)
                self.player.activity.action_card_select(to_select = 2, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.selected_piles = selected_piles
                self.phase = 'move_card'
                self.desk.changed.append('trash')
                self.desk.draw()                   
            else:
                self.desk.changed.append('play_area')                    
                self.action.cleanup()
                self.desk.draw()
        elif self.phase == 'move_card':
            for pile in self.desk.selected_piles:
                if pile.place == 'select_area':
                    card = pile.get_top_card()
                    cards_to_deal_with = self.cards_to_deal_with
                    self.cards_to_deal_with = []
                    for card_to_deal_with in cards_to_deal_with:
                        if card_to_deal_with != card:
                            self.cards_to_deal_with.append(card_to_deal_with)
            for pile in self.desk.selected_piles:
                if pile == self.player.deck:
                    self.player.put_card_to_deck(card)
                    self.desk.changed.append('players_deck') 
                    create_event(self.player.game.get_me(), 'move_card_from_hand_to_deck', { 'player' : self.player.name }, self.player.game.get_other_players_names())
                if pile == self.player.discard:
                    self.player.put_card_to_discard(card)
                    self.desk.changed.append('players_discard') 
                    create_event(self.player.game.get_me(), 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                if pile == self.desk.trash:
                    self.desk.trash.add_card(card)
                    self.desk.changed.append('trash')  
                    create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            if len(self.cards_to_deal_with) > 0:
                selectable_piles = []
                for pile in self.desk.select_area_piles:
                    selectable_piles.append(pile)
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Vyber kartu'
                self.phase = 'choose_action'
                self.desk.changed.append('select_area')
                self.desk.changed.append('players_deck')
                self.desk.draw()
            else:
                self.action.cleanup()
                self.desk.select_area = False
                self.desk.changed.append('play_area')
                self.desk.draw()



