from libs.classes.card import Card

class Baron(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'baron'
        self.name = 'Baron' 
        self.name_en = 'Baron'
        self.expansion = 'Intrigue'
        self.image = 'Baron.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'select_to_discard'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_discard':
            self.player.buys = self.player.buys + 1
            self.desk.changed.append('info')
            self.desk.draw()        
            selectable_piles = []
            for pile in self.player.hand:
                card = pile.top_card()
                if card.name == 'Statek':
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'discard_card'
                self.desk.add_message('Vyber kartu statku, kterou dáš na odkládací balíček')
                self.desk.draw()
            else:
                self.gain_estate()
                self.action.cleanup()
        elif self.phase == 'discard_card':
            if len(self.desk.selected_piles) == 0:
                self.gain_estate()
                self.action.cleanup()
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.treasure = self.player.treasure + 4
                    self.player.put_card_to_discard(card)
                    create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('players_discard')
                self.desk.changed.append('info')
                self.desk.draw()
                self.action.cleanup()                    
    def gain_estate(self):
        from libs.events import create_event
        for pile in self.desk.basic_piles:
            card = pile.top_card()
            if card is not None and card.name == 'Statek':
                card = pile.get_top_card()
                if card is not None:
                    self.player.put_card_to_discard(card)
                    create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
        self.desk.changed.append('basic')
        self.desk.changed.append('players_discard') 
        self.desk.draw()                   

