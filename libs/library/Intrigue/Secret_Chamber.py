from libs.classes.card import Card

class Secret_Chamber(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'secret_chamber'
        self.name = 'Tajemná komnata' 
        self.name_en = 'Secret_Chamber'
        self.expansion = 'Intrigue'
        self.image = 'Secret_Chamber.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'reaction'
        self.price = 2
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        if self.phase == 'action':
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = len(selectable_piles), select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'get_treasure'
                self.desk.add_message('Vyber karty, které zahodíš na odkládací balíček')
                self.desk.draw()                
            else:
                self.action.cleanup()
        elif self.phase == 'get_treasure':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)  
                self.player.treasure = self.player.treasure + 1
                self.player.coalesce_hand()
            self.action.cleanup()
            self.desk.changed.append('info')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.desk.draw()

    def do_reaction(self):
        from libs.events import create_event
        if self.phase == 'action':
            create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : self.name }, self.player.game.get_other_players_names())
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            if len(selectable_piles) > 0:
                if len(selectable_piles) > 2:
                    to_select = 2
                else:
                    to_select = len(selectable_piles)
                self.player.activity.action_card_select(to_select = to_select, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'return_to_deck'
                self.desk.add_message('Vyber karty, které vrátíš na dobírací balíček')
                self.desk.draw()                
        elif self.phase == 'return_to_deck':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.coalesce_hand()
                    self.player.put_card_to_deck(card)
                    self.desk.add_message('Odložil jsi kartu ' + card.name + ' a svůj dobírací balíček')
                    create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + ' odložil kartu ' + card.name + ' z ruky na dobírací balíček'}, self.player.game.get_other_players_names())
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            self.phase = 'action'
            create_event(self.player.game.get_me(), 'send_reaction', { 'player' : self.player.name, 'defend' : 0, 'end' : 0 }, self.player.game.get_other_players_names())
            self.action.cleanup()
