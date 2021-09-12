import json 
from libs.classes.card import Card

class Witch(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'witch'
        self.name = 'Čarodějnice' 
        self.name_en = 'Witch'
        self.expansion = 'Dominion2nd'
        self.image = 'Witch.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 5
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        if self.phase == 'action':
            self.action.request_reactions()   
            self.phase = 'get_reactions'         
        elif self.phase == 'get_reactions':
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            self.phase = 'cleanup'
            self.action.do_attack()
        elif self.phase == 'cleanup':
            self.action.cleanup()        
            self.desk.changed.append('info')
            self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        for pile in self.desk.basic_piles:
            card = pile.top_card()
            if card is not None and card.name == 'Kletba':
                card = pile.get_top_card()
                if card is not None:
                    self.player.put_card_to_discard(card)
                    self.desk.add_message('Při útoku kartou ' + self.name + ' jsi získal kartu ' + card.name)
                    create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
            self.desk.changed.append('basic')
        self.desk.changed.append('players_discard')
        self.action.cleanup()
        create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
