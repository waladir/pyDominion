import json
from libs.classes.card import Card
import traceback

class Thief(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'thief'
        self.name = 'Zloděj' 
        self.name_en = 'Thief'
        self.expansion = 'Dominion'
        self.image = 'Thief.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 4
        self.value = 0

        self.phase = 'action'
        self.cards_to_trash = []
        self.cards_to_discard = []
        self.trashed_cards = []
        self.trashed_cards_data = {}
        self.cards_data = {}

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'action':
            self.action.request_reactions()   
            self.phase = 'get_reactions'         
        elif self.phase == 'get_reactions':    
            self.phase = 'select_to_trash'
            self.action.do_attack()
        elif self.phase == 'select_to_trash':
            for player in self.action.data:
                if player['card_names'] != '':
                    self.cards_data.update({ player['player_name'] : player['card_names']})
            self.action.data = {}
            if len(self.cards_data) > 0:
                player_name = next(iter(self.cards_data))
                self.player_name = player_name
                card_names = self.cards_data[player_name]
                del self.cards_data[player_name]
                self.desk.clear_select()
                self.cards_to_trash = []
                self.cards_to_discard = []
                for card_name in card_names:
                    cardClass = self.player.deck.get_class(card_name)
                    card = cardClass() 
                    if 'treasure' in card.type:
                        self.cards_to_trash.append(card)
                    else:
                        self.cards_to_discard.append(card)
                if len(self.cards_to_trash) == 0:
                    self.desk.add_message('Hráč ' + player_name + ' nemá žádnou kartu peněz')
                    self.action.cleanup()
                # elif len(self.cards_to_trash) == 1:
                #     for card in self.cards_to_trash:
                #         for card in self.cards_to_trash:
                #             self.desk.put_card_to_select_area(card)
                #         for pile in self.desk.select_area_piles:
                #             self.desk.selected_piles.append(pile)
                #         self.desk.add_message('Hráč' + player_name + ' zahodí kartu ' + card.name + ' na smetiště')
                #     self.phase = 'to_trash'
                #     self.do_action()
                else:
                    selectable_piles = []
                    for card in self.cards_to_trash:
                        self.desk.put_card_to_select_area(card)
                    for pile in self.desk.select_area_piles:
                        selectable_piles.append(pile)
                    self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Označ kartu peněz hráče ' + player_name + ', kterou zahodí na smetiště'
                self.desk.changed.append('select_area')
                self.desk.draw()
                self.phase = 'to_trash'
            else:
                self.desk.add_message('Nelze zaútočit na žádného hráče')
                self.action.cleanup()
        elif self.phase == 'to_trash':
            self.desk.select_area = False
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.cards_to_trash.remove(card)
                    self.trashed_cards.append(card)
                    self.trashed_cards_data.update({ card : self.player_name })
                self.desk.coalesce_select_area()

            for pile in self.desk.select_area_piles:
                card = pile.get_top_card()
                if card is not None:
                    create_event(self.player.game.get_me(), 'discard_card_from_deck', { 'attacking_player' : self.player.name, 'player' : self.player_name, 'card_name' : card.name_en }, self.player.game.get_other_players_names())
                    self.cards_to_trash.remove(card)
                    del card
            for card in self.cards_to_discard:
                create_event(self.player.game.get_me(), 'discard_card_from_deck', { 'attacking_player' : self.player.name, 'player' : self.player_name, 'card_name' : card.name_en }, self.player.game.get_other_players_names())
                del card
            if len(self.cards_data) == 0:
                if len(self.trashed_cards) > 0:
                    self.phase = 'select_from_trash'
                    self.do_action()
                else:
                    self.desk.add_message('Na smetiště nebyla zahozená žádná karta peněz')
                    self.action.cleanup()                    
                    self.desk.changed.append('play_area')
                    self.desk.draw()                
            else:
                self.phase = 'select_to_trash'
                self.do_action()
        elif self.phase == 'select_from_trash':
            self.desk.clear_select()
            for card in self.trashed_cards:
                self.desk.put_card_to_select_area(card)
            selectable_piles = []
            for pile in self.desk.select_area_piles:
                selectable_piles.append(pile)
            self.player.activity.action_card_select(to_select = len(selectable_piles), select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
            self.desk.select_area_type = 'select_action'
            self.desk.select_area = True
            self.desk.select_area_label = 'Označ karty, které získáš. Pokud nechceš žádnou, ukonči výběr.'
            self.desk.changed.append('select_area')
            self.phase = 'gain_cards'
            self.desk.draw()
        elif self.phase == 'gain_cards':
            self.desk.select_area = False
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.put_card_to_discard(card)
                    self.trashed_cards.remove(card)
                    create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
            for card in self.trashed_cards:
                self.desk.trash.add_card(card)
                create_event(self.player.game.get_me(), 'trash_card_from_deck', { 'attacking_player' : self.player.name, 'player' : self.trashed_cards_data[card], 'card_name' : card.name_en }, self.player.game.get_other_players_names())
            self.action.cleanup()                    
            self.desk.changed.append('trash')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('play_area')
            self.desk.draw()   

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            card_names = []
            cards = self.player.get_cards_from_deck(2)
            for card in cards:
                card_names.append(card.name_en)
                self.desk.add_message('Ukázal jsi kartu ' + card.name + 'z dobíracího balíčku') 
                create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            if len(card_names) == 0:
                create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + ' nemá žádnou kartu k odhalení'}, self.player.game.get_other_players_names())                
            self.desk.changed.append('players_deck')
            self.desk.draw()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps({ 'player_name' : self.player.name, 'card_names' : card_names }) }, self.player.game.get_other_players_names())
        self.action.cleanup()