from libs.classes.card import Card

class Steward(Card):
    def __init__(self):
        Card.__init__(self)        
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

        self.phase = 'select_bonus'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_bonus':
            selectable_piles = []
            if len(self.player.deck.cards) + len(self.player.discard.cards) > 0:
                selectable_piles.append(self.player.deck)
            selectable_piles.append(self.desk.trash)
            selectable_info = ['treasure']
            self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = selectable_info)
            self.phase = 'get_bonus'
            self.desk.add_message('Pro +2 karty vyber dobírací balíček, pro zahození 2 karet smetiště')
            self.desk.draw()                
        elif self.phase == 'get_bonus':
                for pile in self.desk.selected_piles:
                    if pile == self.player.deck:
                        cards = self.player.get_cards_from_deck(2)
                        for card in cards:
                            self.player.put_card_to_hand(card)   
                    elif pile == self.desk.trash:
                        self.desk.clear_select()
                        selectable_piles = []
                        for pile in self.player.hand:
                            selectable_piles.append(pile)
                        if len(selectable_piles) > 0:
                            self.player.activity.action_card_select(to_select = 2, select_type = 'optional', select_action = 'select', piles = selectable_piles)
                            self.desk.add_message('Vyber karty, které zahodíš na smetiště')
                            self.phase = 'select_to_trash'
                            self.desk.draw()                
                if len(self.desk.selected_info) > 0:
                    for section in self.desk.selected_info:
                        if section == 'treasure':
                            self.player.treasure = self.player.treasure + 2
                if self.phase != 'select_to_trash':
                    self.action.cleanup()
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('info')
                    self.desk.changed.append('players_deck')
                    self.desk.draw()
        elif self.phase == 'select_to_trash':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.desk.trash.add_card(card)
                    create_event(self, 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                    self.player.coalesce_hand()
                self.action.cleanup()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('players_deck')
                self.desk.changed.append('info')
                self.desk.changed.append('trash')
                self.desk.draw()                      
