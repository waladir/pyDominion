from libs.classes.card import Card

class Workshop(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'workshop'
        self.name = 'Dílna' 
        self.name_en = 'Workshop'
        self.expansion = 'Dominion'
        self.image = 'Workshop.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

        self.phase = 'select_to_gain'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_gain':
            selectable_piles = []
            piles = self.desk.basic_piles + self.desk.kingdom_piles
            for pile in piles:
                card = pile.top_card()
                if card is not None and card.price <= 4:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'gain_card'
                self.desk.add_message('Vyber kartu, kterou získáš')
                self.desk.draw()                
            else:
                self.action.cleanup()
        elif self.phase == 'gain_card':
            if len(self.desk.selected_piles) == 0:
                self.action.cleanup()
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.put_card_to_discard(card)  
                    create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.action.cleanup()
                self.desk.changed.append('basic')
                self.desk.changed.append('kingdom')
                self.desk.changed.append('players_discard')
                self.desk.draw()

