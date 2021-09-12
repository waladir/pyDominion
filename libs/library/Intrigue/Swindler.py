import json
from libs.classes.card import Card

class Swindler(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'swindler'
        self.name = 'Podvodník' 
        self.name_en = 'Swindler'
        self.expansion = 'Intrigue'
        self.image = 'Swindler.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 3
        self.value = 0

        self.phase = 'action'
        self.cards_data = {}
        self.player_name = ''

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'action':
            self.action.request_reactions()   
            self.phase = 'get_reactions'         
        elif self.phase == 'get_reactions':             
            self.player.treasure = self.player.treasure + 2
            self.desk.changed.append('info')
            self.desk.draw()
            self.phase = 'select_to_gain'
            self.action.do_attack()
        elif self.phase == 'select_to_gain':
            for player in self.action.data:
                if player['card_name'] != '':
                    self.cards_data.update({ player['player_name'] : player['card_name']})
            self.action.data = {}
            if len(self.cards_data) > 0:
                self.player_name = next(iter(self.cards_data))
                card_name = self.cards_data[self.player_name]
                del self.cards_data[self.player_name]
                self.desk.clear_select()
                cardClass = self.player.deck.get_class(card_name)
                trashed_card = cardClass() 
                selectable_piles = []
                for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                    card = pile.top_card()
                    if card is not None and card.price == trashed_card.price:
                        selectable_piles.append(pile)
                if len(selectable_piles) > 0:
                    self.desk.put_card_to_select_area(trashed_card)                    
                    self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Vyber, kterou kartu získá hráč ' + self.player_name + ' místo zahozené karty ' + trashed_card.name
                    self.phase = 'give_card_to_player'
                    self.desk.changed.append('select_area')
                    self.desk.changed.append('players_deck')
                    self.desk.draw()
                else:
                    if len(self.cards_data) == 0:
                        self.desk.changed.append('play_area')
                        self.action.cleanup()
                        self.desk.draw()        
                    else:
                        self.phase = 'select_to_gain'
                        self.do_action()
            else:
                if len(self.cards_data) == 0:
                    self.desk.changed.append('play_area')
                    self.action.cleanup()
                    self.desk.draw()        
                else:
                    self.phase = 'select_to_gain'
                    self.do_action()
        elif self.phase == 'give_card_to_player':
            self.desk.select_area = False
            for pile in self.desk.select_area_piles:
                card = pile.get_top_card()            
                del card
            for pile in self.desk.selected_piles:
                card = pile.top_card()
                if card is not None:
                    create_event(self.player.game.get_me(), 'get_card_from_supply', { 'attacking_player' : self.player.name, 'player' : self.player_name, 'card_name' : card.name }, self.player.game.get_other_players_names())                        
            if len(self.cards_data) == 0:
                self.desk.changed.append('play_area')
                self.action.cleanup()
                self.desk.draw()        
            else:
                self.phase = 'select_to_gain'
                self.do_action()


    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            card_name = ''
            cards = self.player.get_cards_from_deck(1)
            if len(cards) > 0:
                for card in cards:
                    self.desk.trash.add_card(card)      
                    self.desk.changed.append('trash')          
                    self.desk.changed.append('players_deck')
                    card_name = card.name_en
                    self.desk.add_message('Při útoku kartou Podvodník si zahodil kartu ' + card.name + ' z balíčku na smetiště')
                    create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.desk.draw()
            create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps({ 'player_name' : self.player.name, 'card_name' : card_name }) }, self.player.game.get_other_players_names())
        self.action.cleanup()


        
