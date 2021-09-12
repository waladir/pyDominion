import json
from libs.classes.card import Card

class Masquerade(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'masquerade'
        self.name = 'Maškary' 
        self.name_en = 'Masquerade'
        self.expansion = 'Intrigue'
        self.image = 'Masquerade.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'action':
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            self.phase = 'select_card'
            self.action.to_attack = self.player.game.get_other_players_names()
            self.action.do_attack()
        elif self.phase == 'select_card':
            if len(self.player.hand) > 0:
                selectable_piles = []
                for pile in self.player.hand:
                    selectable_piles.append(pile)
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'pass_cards'
                self.desk.add_message('Vyber kartu, kterou pošleš hráči vlevo')
                self.desk.draw()                
            else:
                self.phase = 'pass_cards'
                self.desk_draw()
        elif self.phase == 'pass_cards':
            idx = 0
            players_to_pass_cards = {}
            for player in self.player.game.players:
                if player.name == self.player.name:
                    if len(self.desk.selected_piles) > 0:
                        for pile in self.desk.selected_piles:
                            card = pile.get_top_card()
                            if card is not None:
                                players_to_pass_cards.update({ idx : {'player_name' : self.player.name, 'card_name' : card.name_en }})
                                idx = idx + 1
                                self.player.coalesce_hand()
                    self.desk.changed.append('players_hand')
                    self.desk.draw()
                else:
                    for data in self.action.data:
                        if data['player_name'] == player.name and data['card_name'] != '':
                            players_to_pass_cards.update({ idx : {'player_name' : data['player_name'], 'card_name' : data['card_name'] }})
                            idx = idx + 1
            idx = self.game.current_player
            skip = False
            while skip == False:
                from_player = players_to_pass_cards[idx]['player_name']
                if idx < len(players_to_pass_cards) - 1:
                    to_player =  players_to_pass_cards[idx + 1]['player_name']
                else:
                    to_player = players_to_pass_cards[0]['player_name']
                card_name = players_to_pass_cards[idx]['card_name']
                if to_player == self.player.name:
                    cardClass = self.player.deck.get_class(card_name)
                    card = cardClass() 
                    self.desk.add_message('Hráč ' + from_player + ' ti předal kartu ' + card.name)
                    self.player.put_card_to_hand(card)
                    self.desk.changed.append('players_hand')
                    self.desk.draw()
                else:
                    create_event(self, 'pass_card', { 'player' : from_player, 'card_name' : card_name }, [to_player])
                if idx < len(players_to_pass_cards) - 1:
                    idx = idx + 1
                else:
                    idx = 0
                if idx == self.game.current_player:
                    skip = True

            if len(self.player.hand) > 0:
                selectable_piles = []
                for pile in self.player.hand:
                    selectable_piles.append(pile)
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'trash_card'
                self.desk.add_message('Ukonči výběr, pokud žádnou zahodit nechceš.')
                self.desk.add_message('Vyber kartu, kterou zahodíš na smetiště.')
                self.desk.draw()                
            else:
                self.action.cleanup()    
        elif self.phase == 'trash_card':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.desk.trash.add_card(card)
                    create_event(self, 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.player.coalesce_hand()
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('trash')
            self.desk.draw() 

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            if len(self.player.hand) > 0:
                selectable_piles = []
                for pile in self.player.hand:
                    selectable_piles.append(pile)
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'pass_card'
                self.desk.add_message('Vyber kartu, kterou pošleš hráči vlevo')
                self.desk.draw()                
            else:
                create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps({ 'player_name' : self.player.name, 'card_name' : '' }) }, self.player.game.get_other_players_names())
                self.action.cleanup()
        elif self.phase == 'pass_card':
            card_name = ''
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    card_name = card.name_en
                    del card
            self.player.coalesce_hand()
            self.desk.changed.append('players_hand')
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps({ 'player_name' : self.player.name, 'card_name' : card_name }) }, self.player.game.get_other_players_names())
            self.action.cleanup()
