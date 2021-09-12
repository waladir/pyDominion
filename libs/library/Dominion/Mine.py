from libs.classes.card import Card

class Mine(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'mine'
        self.name = 'Důl' 
        self.name_en = 'Mine'
        self.expansion = 'Dominion'
        self.image = 'Mine.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.phase = 'select_to_trash'
        self.card_price = -1

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_trash':
            selectable_piles = []
            for pile in self.player.hand:
                card = pile.top_card()
                if 'treasure' in card.type:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'trash_card'
                self.desk.add_message('Vyber kartu, kterou zahodíš na smetiště')                
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'trash_card':
            if len(self.desk.selected_piles) == 0:
                self.action.cleanup()
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    card_price = card.price + 3 
                    self.desk.trash.add_card(card)
                    create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('trash')
                self.desk.draw()  
                self.desk.clear_select()             
                selectable_piles = []         
                for pile in self.desk.basic_piles:
                    card = pile.top_card()
                    if card is not None and 'treasure' in card.type and card.price <= card_price:
                        selectable_piles.append(pile)
                if len(selectable_piles) > 0:
                    self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                    self.phase = 'gain_card'
                    self.desk.add_message('Vyber kartu, kterou získáš')                
                else:
                    self.action.cleanup()
                self.desk.redraw_borders()     
        elif self.phase == 'gain_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_discard(card) 
                create_event(self.player.game.get_me(), 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.action.cleanup()
            self.desk.changed.append('players_discard')
            self.desk.draw()    

