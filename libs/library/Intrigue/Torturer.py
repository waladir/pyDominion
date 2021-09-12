import json
from libs.classes.card import Card

class Torturer(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'torturer'
        self.name = 'Žalářník' 
        self.name_en = 'Torturer'
        self.expansion = 'Intrigue'
        self.image = 'Torturer.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 5
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'action':
            self.action.request_reactions()   
            self.phase = 'get_reactions'         
        elif self.phase == 'get_reactions':             
            self.player.move_cards_from_deck_to_hand(3)
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_deck')
            self.desk.draw()
            self.phase = 'cleanup'
            self.action.do_attack()
        elif self.phase == 'cleanup':
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_deck')
            self.desk.draw()        

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            selectable_piles = []
            self.desk.add_message('Vyber, jestli zahodíš dvě karty z ruky nebo si vezmeš kletbu')
            for pile in self.desk.basic_piles:
                if pile.card_name == 'Curse':
                    selectable_piles.append(pile)
            selectable_piles.append(self.player.discard)
            self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
            self.phase = 'choose_attack'
            self.subphase = 'select_choice'
            self.action.select_cards = 'mandatory'
            self.desk.draw()
        elif self.phase == 'choose_attack':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    if pile == self.player.discard:
                        self.desk.clear_select()
                        selectable_piles = []
                        for pile_to_discard in self.player.hand:
                            selectable_piles.append(pile_to_discard)
                        if len(selectable_piles) > 0:
                            if len(self.player.hand) < 2:
                                to_select = len(self.player.hand)
                            else:
                                to_select = 2
                            self.player.activity.action_card_select(to_select = to_select, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                            self.phase = 'discard_cards'
                            self.desk.add_message('Vyber karty, které zahodíš')
                            self.desk.draw()                
                        else:
                            self.attacked_cleanup()
                    else:
                        card = pile.get_top_card()
                        if card is not None and card.name == 'Kletba':
                            self.player.put_card_to_discard(card)
                            self.player.coalesce_hand()
                            self.desk.changed.append('basic')
                            self.desk.changed.append('players_discard')
                            create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                        self.attacked_cleanup()
            else:
                self.attacked_cleanup()
        elif self.phase == 'discard_cards':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)                        
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('players_discard')
                create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
            self.attacked_cleanup()

    def attacked_cleanup(self):
        from libs.events import create_event
        self.desk.draw()
        create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
        self.action.cleanup()
