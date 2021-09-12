import json 
from libs.classes.card import Card

class Bandit(Card):
    def __init__(self):
        self.id = 'bandit'
        Card.__init__(self)
        self.name = 'Bandita' 
        self.name_en = 'Bandit'
        self.expansion = 'Dominion2nd'
        self.image = 'Bandit.png'
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
            for pile in self.desk.basic_piles:
                card = pile.top_card()
                if card is not None and card.name == 'Zlaťák':
                    card = pile.get_top_card()
                    if card is not None:
                        self.player.put_card_to_discard(card)
                        self.desk.add_message('Získal jsi kartu ' + card.name + ' a umístil ji svůj odkládací balíček')
                        create_event(self.player.game.get_me(), 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                                    
            self.desk.changed.append('basic')                    
            self.desk.changed.append('players_discard') 
            self.desk.draw()                   
            self.phase = 'cleanup'
            self.action.do_attack()
        elif self.phase == 'cleanup':
            self.action.cleanup()        
            self.desk.draw()


    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            cards = self.player.get_cards_from_deck(2)
            for card in cards:
                if card is not None:
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                    if 'treasure' in card.type and card.name != 'Měďák':
                        create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                        self.desk.add_message('Odložil jsi kartu ' + card.name + ' na smetiště')
                        self.desk.trash.add_card(card)
                    else:                            
                        create_event(self.player.game.get_me(), 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                        self.desk.add_message('Odložil jsi kartu ' + card.name + ' a svůj odkládací balíček')
                        self.player.put_card_to_discard(card) 
            self.desk.changed.append('trash')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('players_deck')
            self.action.cleanup()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())


