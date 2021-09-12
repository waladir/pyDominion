import json
from libs.classes.card import Card

class Spy(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'spy'
        self.name = 'Špion' 
        self.name_en = 'Spy'
        self.expansion = 'Dominion'
        self.image = 'Spy.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
        self.value = 0

        self.phase = 'action'
        self.cards_data = {}

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'action':
            self.action.request_reactions()   
            self.phase = 'get_reactions'         
        elif self.phase == 'get_reactions':    
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()
            self.phase = 'select_to_choose'
            self.action.do_attack()
        elif self.phase == 'select_to_choose':
            for player in self.action.data:
                if player['card_name'] != '':
                    self.cards_data.update({ player['player_name'] : player['card_name']})
            self.action.data = {}
            if len(self.cards_data) > 0:
                player_name = next(iter(self.cards_data))
                card_name = self.cards_data[player_name]
                del self.cards_data[player_name]
                self.desk.clear_select()
                cardClass = self.player.deck.get_class(card_name)
                card = cardClass() 
                self.selected_card = card
                self.player_name = player_name
                self.desk.put_card_to_select_area(card)
                selectable_piles = []
                selectable_piles.append(self.player.deck)
                selectable_piles.append(self.player.discard)
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Označ jestli má hráč ' + player_name + ' odložit kartu na svůj odkládací balíček nebo vrátit na dobírací balíček'
                self.phase = 'move_card'
                self.desk.changed.append('select_area')
                self.desk.draw()
            else:
                self.desk.add_message('Nelze zaútočit na žádného hráče')
                self.action.cleanup()
        elif self.phase == 'move_card':
            self.desk.select_area = False
            for pile in self.desk.select_area_piles:
                card = pile.get_top_card()            
                del card
            for pile in self.desk.selected_piles:
                if pile == self.player.deck:
                    create_event(self.player.game.get_me(), 'return_card_to_deck', { 'attacking_player' : self.player.name, 'player' : self.player_name, 'card_name' : self.selected_card.name_en }, self.player.game.get_other_players_names())                        
                else:
                    create_event(self.player.game.get_me(), 'discard_card_from_deck', { 'attacking_player' : self.player.name, 'player' : self.player_name, 'card_name' : self.selected_card.name_en }, self.player.game.get_other_players_names())                        
            if len(self.cards_data) == 0:
                self.desk.changed.append('play_area')
                self.phase = 'select_to_choose_self'
                self.desk.draw()                
                self.do_action()
            else:
                self.phase = 'select_to_choose'
                self.do_action()
        elif self.phase == 'select_to_choose_self':
            self.desk.clear_select()
            cards = self.player.get_cards_from_deck(1)
            for card in cards:
                self.desk.put_card_to_select_area(card)
                self.desk.add_message('Ukázal jsi kartu ' + card.name + 'z dobíracího balíčku') 
                create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            selectable_piles = []
            selectable_piles.append(self.player.deck)
            selectable_piles.append(self.player.discard)
            self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
            self.desk.select_area_type = 'select_action'
            self.desk.select_area = True
            self.desk.select_area_label = 'Označ jestli odložíš svou kartu na odkládací balíček nebo ji vrátíš na dobírací balíček'
            self.phase = 'move_card_self'
            self.desk.changed.append('select_area')
            self.desk.changed.append('players_deck')
            self.desk.draw()
        elif self.phase == 'move_card_self':
            self.desk.select_area = False
            for pile in self.desk.select_area_piles:
                card = pile.get_top_card()
            for pile in self.desk.selected_piles:
                if pile == self.player.deck:
                    create_event(self.player.game.get_me(), 'return_card_to_deck', { 'attacking_player' : self.player.name, 'player' : self.player.name, 'card_name' : card.name_en }, self.player.game.get_other_players_names())                        
                    self.player.put_card_to_deck(card)
                else:
                    create_event(self.player.game.get_me(), 'discard_card_from_deck', { 'attacking_player' : self.player.name, 'player' : self.player.name, 'card_name' : card.name_en }, self.player.game.get_other_players_names())                        
                    self.player.put_card_to_discard(card)
            self.action.cleanup()                    
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('play_area')
            self.desk.draw()                

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            card_name = ''
            cards = self.player.get_cards_from_deck(1)
            for card in cards:
                card_name = card.name_en
                self.desk.add_message('Ukázal jsi kartu ' + card.name + 'z dobíracího balíčku') 
                create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            if card_name == '':
                create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + ' nemá žádnou kartu k odhalení'}, self.player.game.get_other_players_names())                
            self.desk.changed.append('players_deck')
            self.desk.draw()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps({ 'player_name' : self.player.name, 'card_name' : card_name }) }, self.player.game.get_other_players_names())
        self.action.cleanup()