import json 
from libs.classes.card import Card

class Bureaucrat(Card):
    def __init__(self):
        Card.__init__(self)
        self.id = 'bureaucrat'
        self.name = 'Úředník' 
        self.name_en = 'Bureaucrat'
        self.expansion = 'Dominion2nd'
        self.image = 'Bureaucrat.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
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
                if card is not None and card.name == 'Stříbrňák':
                    card = pile.get_top_card()
                    self.player.put_card_to_deck(card)
                    self.desk.add_message('Získal jsi kartu ' + card.name + ' a umístil ji svůj dobírací balíček')
                    create_event(self.player.game.get_me(), 'gain_card_to_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                                    
            self.desk.changed.append('basic')
            self.desk.changed.append('players_deck')
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
                card = pile.top_card()
                if 'victory' in card.type:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'place_victory_card_on_deck'
                self.desk.add_message('Vyber kartu s vítěznými body, které odložíš na dobírací balíček')
                self.desk.draw()
            else:
                for pile in self.player.hand:
                    card = pile.top_card()
                    create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                                    
                self.desk.add_message('Ukázal jsi karty v ruce')
                self.action.cleanup()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
        elif self.phase == 'place_victory_card_on_deck':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.player.put_card_to_deck(card)
                self.desk.add_message('Odložil jsi kartu ' + card.name + ' a svůj dobírací balíček')
                create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + ' odložil kartu ' + card.name + ' z ruky na dobírací balíček'}, self.player.game.get_other_players_names())
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_deck')
            self.action.cleanup()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
