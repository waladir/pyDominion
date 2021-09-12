from libs.classes.card import Card

class Chapel(Card):
    def __init__(self):
        Card.__init__(self) 
        self.id = 'chapel'
        self.name = 'Kaple' 
        self.name_en = 'Chapel'
        self.expansion = 'Dominion2nd'
        self.image = 'Chapel.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.phase = 'select_to_trash'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_trash':
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 4, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'trash_cards'
                self.desk.add_message('Vyber karty, které zahodíš na smetiště')
                self.desk.draw()                
            else:
                self.action.cleanup()
        elif self.phase == 'trash_cards':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.desk.trash.add_card(card)                
                create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('trash')
            self.desk.draw()

