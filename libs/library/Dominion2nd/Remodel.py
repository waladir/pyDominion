from libs.classes.card import Card

class Remodel(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'remodel'
        self.name = 'Přestavba' 
        self.name_en = 'Remodel'
        self.expansion = 'Dominion2nd'
        self.image = 'Remodel.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'select_to_trash'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_trash':
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'trash_card'
                self.desk.add_message('Vyber kartu, kterou zahodíš na smetiště')
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'trash_card':
            if len(self.desk.selectable_piles) == 0:
                self.action.cleanup()
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    card_price = card.price + 2 
                    self.desk.trash.add_card(card)
                    create_event(self, 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('trash')
                self.desk.draw()                        
                self.desk.clear_select()
                selectable_piles = []
                piles = self.desk.basic_piles + self.desk.kingdom_piles
                for pile in piles:
                    card = pile.top_card()
                    if card is not None and card.price <= card_price:
                        selectable_piles.append(pile)
                if len(selectable_piles) > 0:
                    self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                    self.phase = 'gain_card'
                    self.desk.add_message('Vyber kartu, kterou získáš')
                self.desk.draw()        
        elif self.phase == 'gain_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_discard(card) 
                create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
            self.action.cleanup()                    
            self.desk.changed.append('basic')
            self.desk.changed.append('kingdom')
            self.desk.changed.append('players_discard')
            self.desk.draw()


