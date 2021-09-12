import json 
from libs.classes.card import Card

class Militia(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'militia'
        self.name = 'Milice' 
        self.name_en = 'Militia'
        self.expansion = 'Dominion2nd'
        self.image = 'Militia.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        if self.phase == 'action':
            self.action.request_reactions()   
            self.phase = 'get_reactions'         
        elif self.phase == 'get_reactions':
            self.player.treasure = self.player.treasure + 2
            self.desk.changed.append('info')
            self.desk.draw()
            self.phase = 'cleanup'
            self.action.do_attack()
        elif self.phase == 'cleanup':
            self.action.cleanup()        
            self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0 and len(selectable_piles) - 3 > 0:
                self.player.activity.action_card_select(to_select = len(selectable_piles) - 3, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'discard_cards'
                self.desk.add_message('Vyber karty, které odložíš')
                self.desk.draw()
            else:
                self.action.cleanup()

        elif self.phase == 'discard_cards':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_discard(card)   
                create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
            self.player.coalesce_hand()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.action.cleanup()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
