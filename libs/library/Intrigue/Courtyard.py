from libs.classes.card import Card

class Courtyard(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'courtyard'
        self.name = 'Hradní nádvoří' 
        self.name_en = 'Courtyard'
        self.expansion = 'Intrigue'
        self.image = 'Courtyard.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.phase = 'select_card'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_card':
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            self.player.move_cards_from_deck_to_hand(3)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'move_to_deck'
                self.desk.add_message('Vyber kartu, kterou dáš na dobírací balíček')
                self.desk.draw()                
            else:
                self.action.cleanup()
        elif self.phase == 'move_to_deck':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_deck(card)
                create_event(self, 'move_card_from_hand_to_deck', { 'player' : self.player.name }, self.game.get_other_players_names())
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_deck')
            self.desk.changed.append('info')
            self.desk.draw() 