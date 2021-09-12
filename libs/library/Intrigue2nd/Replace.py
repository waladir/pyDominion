import json
from libs.classes.card import Card

class Replace(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'replace'
        self.name = 'Záměna' 
        self.name_en = 'Replace'
        self.expansion = 'Intrigue2nd'
        self.image = 'Replace.png'
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
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])                
                self.phase = 'trash_card'
                self.desk.add_message('Vyber kartu, kterou zahodíš na smetiště')
                self.desk.draw()   
            else:
                self.action.cleanup()
        elif self.phase == 'trash_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                card_price = card.price + 2 
                self.player.coalesce_hand()
                self.desk.trash.add_card(card)
                create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.desk.changed.append('players_hand')
                self.desk.changed.append('trash')
                self.desk.draw() 
            self.desk.clear_select()
            selectable_piles = []
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                card = pile.top_card()
                if card is not None and card.price <= card_price:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])                
                self.desk.redraw_borders()    
                self.phase = 'gain_card'              
                self.desk.add_message('Vyber kartu, kterou získáš')
            else:
                self.action.cleanup()
                self.desk.draw()
        elif self.phase == 'gain_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                create_event(self.player.game.get_me(), 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                if 'action' in card.type or 'treasure' in card.type:
                    self.player.put_card_to_deck(card) 
                    self.desk.changed.append('players_deck')
                    self.desk.changed.append('basic')
                    self.desk.changed.append('kingdom')
                    self.desk.draw()
                if 'victory' in card.type:
                    if 'action' not in card.type and 'treasure' not in card.type:
                        self.player.put_card_to_discard(card) 
                        self.desk.changed.append('players_discard')
                        self.desk.draw()
                    self.phase = 'cleanup'
                    self.action.do_attack()
                else:
                    self.action.cleanup()   
        elif self.phase == 'cleanup':
            self.action.cleanup()        
            self.desk.draw()            

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            for pile in self.desk.basic_piles:
                card = pile.top_card()
                if card is not None and card.name == 'Kletba':
                    card = pile.get_top_card()
                    if card is not None:
                        self.player.put_card_to_discard(card)
                        self.desk.add_message('Při útoku kartou Záměna si získal kartu Kletba')
                        create_event(self.player.game.get_me(), 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.action.cleanup()
            self.desk.changed.append('players_discard')
            self.desk.draw()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
        self.action.cleanup()
