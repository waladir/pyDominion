from libs.classes.card import Card

class Cellar(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'cellar'
        self.name = 'Sklepení' 
        self.name_en = 'Cellar'
        self.expansion = 'Dominion'
        self.image = 'Cellar.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.phase = 'select_to_discard'

    def do_action(self):
        if self.phase == 'select_to_discard':
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = len(selectable_piles), select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'gain_card'
                self.desk.add_message('Vyber karty, které zahodíš na odkládací balíček')
                self.desk.draw()                
            else:
                self.action.cleanup()
        elif self.phase == 'gain_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_discard(card)  
                self.player.move_cards_from_deck_to_hand(1)
            self.action.cleanup()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.desk.draw()

