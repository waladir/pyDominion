from libs.classes.card import Card

class Upgrade(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'upgrade'
        self.name = 'Pokrok' 
        self.name_en = 'Upgrade'
        self.expansion = 'Intrigue'
        self.image = 'Upgrade.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.phase = 'select_to_trash'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_trash':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')            
            self.desk.draw()
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.add_message('Vyber kartu, kterou zahodíš na smetiště')
                self.phase = 'trash_card'
                self.desk.draw()                
            else:
                self.action.cleanup()               
        elif self.phase == 'trash_card':
            if len(self.desk.selected_piles) > 0:
                card_price = 0
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    card_price = card.price + 1
                    self.player.coalesce_hand()
                    self.desk.trash.add_card(card)
                    create_event(self, 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                    self.desk.changed.append('players_hand')        
                    self.desk.changed.append('trash')        
                    self.desk.draw()                
                if card_price > 0:
                    self.desk.clear_select()
                    selectable_piles = []
                    for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                        card = pile.top_card()
                        if card is not None and card.price == card_price:
                            selectable_piles.append(pile)
                    if len(selectable_piles) > 0:
                        self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                        self.desk.add_message('Vyber kartu, kterou získáš')
                        self.phase = 'gain_card'
                        self.desk.draw()                
                    else:
                        self.action.cleanup()               
        elif self.phase == 'gain_card':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.put_card_to_discard(card)
                    create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.action.cleanup()
                self.desk.changed.append('players_discard')
                self.desk.draw() 