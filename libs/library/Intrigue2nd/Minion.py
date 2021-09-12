import json
from libs.classes.card import Card

class Minion(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'minion'
        self.name = 'Služebník' 
        self.name_en = 'Minion'
        self.expansion = 'Intrigue2nd'
        self.image = 'Minion.png'
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
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()        
            selectable_piles = []
            selectable_piles.append(self.player.discard)
            selectable_info = ['treasure']
            self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = selectable_info)
            self.phase = 'choose_bonus'
            self.desk.draw()                
        elif self.phase == 'choose_bonus':
            if len(self.desk.selected_piles) > 0 and self.player.discard in self.desk.selected_piles:
                for pile in self.player.hand:
                    card = pile.get_top_card()
                    self.player.put_card_to_discard(card) 
                    create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.player.coalesce_hand()
                self.player.move_cards_from_deck_to_hand(4)                  
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('players_discard')
                self.desk.changed.append('players_deck')
                self.phase = 'cleanup'
                self.action.do_attack()
            if len(self.desk.selected_info) > 0:
                for section in self.desk.selected_info:
                    if section == 'treasure':
                        self.player.treasure = self.player.treasure + 2
                self.action.cleanup()
                self.desk.changed.append('info')
                self.desk.draw()
        elif self.phase == 'cleanup':
            self.action.cleanup()        
            self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':        
            if len(self.player.hand) >= 5:
                for pile in self.player.hand:
                    card = pile.get_top_card()
                    self.player.put_card_to_discard(card) 
                    create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.desk.add_message('Při útoku karty Služebník jsi zahodil karty z ruky')
                self.player.coalesce_hand()
                self.player.move_cards_from_deck_to_hand(4)                  
                self.desk.changed.append('players_hand')
                self.desk.changed.append('players_discard')
                self.desk.changed.append('players_deck')
                self.desk.draw()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
        self.action.cleanup()
