from libs.classes.card import Card

class Poacher(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'poacher'
        self.name = 'Pytlák' 
        self.name_en = 'Poacher'
        self.expansion = 'Dominion2nd'
        self.image = 'Poacher.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'select_to_discard'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_discard':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.player.treasure = self.player.treasure + 1
            self.desk.changed.append('info')
            self.desk.draw()
            to_discard = 0
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                if len(pile.cards) == 0:
                    to_discard = to_discard + 1
            if to_discard > 0:
                selectable_piles = []
                for pile in self.player.hand:
                    selectable_piles.append(pile)
                if len(selectable_piles) > 0:
                    self.player.activity.action_card_select(to_select = to_discard, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                    self.phase = 'discard_cards'
                    self.desk.add_message('Vyber karty, které zahodíš na smetiště')
                    self.desk.draw()
                else:
                    self.action.cleanup()
            else:
                self.action.cleanup()
        elif self.phase == 'discard_cards':
            if len(self.desk.selected_piles) == 0:
                self.action.cleanup()
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.desk.trash.add_card(card)
                    create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('trash')
            self.action.cleanup()                    
            self.desk.draw()



            