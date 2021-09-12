from libs.classes.card import Card

class Artisan(Card):
    def __init__(self):
        Card.__init__(self)
        self.id = 'artisan'
        self.name = 'Řemeslník' 
        self.name_en = 'Artisan'
        self.expansion = 'Dominion2nd'
        self.image = 'Artisan.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 6
        self.value = 0

        self.phase = 'select_to_gain'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_gain':
            selectable_piles = []
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                card = pile.top_card()
                if card.price <= 5:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'gain_card'
                self.desk.add_message('Vyber kartu, kterou získáš')                
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'gain_card':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.put_card_to_hand(card)
                    create_event(self.player.game.get_me(), 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                    self.desk.changed.append('players_hand')
            self.desk.draw()
            self.desk.clear_select()
            selectable_piles = []
            for pile in self.player.hand:
                card = pile.top_card()
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'move_from_hand_to_deck'
                self.desk.add_message('Vyber kartu, kterou odložíš na dobírací balíček')                
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'move_from_hand_to_deck':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_deck(card) 
                self.player.coalesce_hand()
                create_event(self.player.game.get_me(), 'move_card_from_hand_to_deck', { 'player' : self.player.name }, self.player.game.get_other_players_names())
            self.action.cleanup()                    
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()


