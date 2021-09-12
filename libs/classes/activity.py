import debug
from libs.classes.action import Action
from libs.classes.pile import Pile
from libs.events import create_event

class Activity():
    def __init__(self, player):
        self.player = player
        self.game = None
        self.desk = None
    
    def start_action_phase(self):
        self.desk.clear_select()
        create_event(self, 'start_turn', self.player.name, self.game.get_other_players_names())
        create_event(self, 'action', self.player.name, self.game.get_other_players_names())
        if len(self.player.play_area_cards) > 0:
            for card in self.player.play_area_cards:
                self.desk.put_card_to_play_area(card, hidden = card.hidden)
            self.desk.changed.append('play_area')
            self.desk.draw()
            self.player.play_area_cards = []
        for trigger in self.player.desk.get_triggers('next_round_start'):
            trigger.run()
        self.desk.add_message('Začal tvůj tah')
        self.desk.add_message('Začátek akční fáze')
        self.player.phase = 'action'
        self.desk.changed.append('info')
        self.desk.changed.append('play_area')
        self.cards_to_play()
        self.player.check_phase_end()
        self.desk.draw()

    def start_buy_phase(self):
        self.desk.clear_select()
        create_event(self, 'buy', self.player.name, self.game.get_other_players_names())
        self.player.phase = 'buy'
        self.desk.add_message('Začátek fáze nákupu')
        self.desk.changed.append('info')
        self.cards_to_buy()
        self.desk.draw()

    def start_cleanup(self):
        self.desk.clear_select()
        for pile in self.game.desk.play_area_piles:
            for i in range(len(pile.cards)):
                card = pile.get_top_card()
                if card is not None:
                    if card.skip_cleanup == False:
                        self.player.put_card_to_discard(card)
                        card.__init__()
                    else: 
                        self.player.play_area_cards.append(card)
        self.desk.coalesce_play_area()
        self.player.move_cards_from_hand_to_discard()
        self.player.move_cards_from_deck_to_hand(5)      
        self.player.treasure = 0
        self.player.actions = 1
        self.player.buys = 1
        self.desk.clear_triggers(duration = 'end_of_round')
        self.game.next_player()
        if debug.test_cards == False or debug.test_attack_cards == True:
            create_event(self, 'next_player', self.player.name, self.game.get_other_players_names())
            self.player.phase = 'other_players_turn'
        self.desk.draw(False)

    def click_on_pile(self, pile):
        if pile in self.desk.selectable_piles:
            if self.player.phase == 'action':
                card = pile.get_top_card()
                if card is not None:
                    self.player.coalesce_hand()
                    self.player.actions = self.player.actions - 1
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('info')
                    self.play_card(card)
            elif self.player.phase == 'buy':
                if pile.place == 'basic' or pile.place == 'kingdom':
                    card = pile.get_top_card()
                    if card is not None:
                        self.player.buys = self.player.buys - 1
                        self.player.treasure = self.player.treasure - card.price
                        self.player.put_card_to_discard(card)
                        create_event(self, 'bought_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                        triggers = self.desk.get_pile_triggers(pile)
                        if len(triggers) > 0:
                            for trigger in triggers:
                                if trigger.type == 'buy_token':
                                    trigger.run()
                        self.desk.changed.append('basic')
                        self.desk.changed.append('kingdom')
                        self.desk.changed.append('players_discard')
                        self.desk.changed.append('info')
                        self.cards_to_buy()
                        self.desk.draw()
                        self.player.check_phase_end()
                if pile.place == 'players_hand':
                    card = pile.get_top_card()
                    if card is not None and 'treasure' in card.type:
                        self.player.coalesce_hand()
                        self.play_treasure_card(card)
                        self.player.treasure = self.player.treasure + card.value
                        self.desk.changed.append('info')
                        self.desk.changed.append('players_hand')
                        self.cards_to_buy()
                        self.desk.draw()
            elif self.player.phase == 'action_play' or self.player.phase == 'attacked' or (self.player.phase == 'attacked_reaction' and len(self.player.actions_to_play) > 0):
                self.desk.selected_piles.append(pile)
                self.desk.selectable_piles.remove(pile)
                if len(self.desk.selected_piles) + len(self.desk.selected_info) == self.desk.to_select:
                    action = self.player.actions_to_play[0]
                    if self.player.phase == 'action_play':
                        action.do_action()
                    elif self.player.phase == 'attacked':
                        action.do_attacked()
                    elif self.player.phase == 'attacked_reaction':
                        action.do_reaction()
                else:
                    self.desk.draw()
            elif self.player.phase == 'attacked_reaction' and len(self.player.actions_to_play) == 0:
                card = pile.top_card()
                if card is not None:
                    action = Action(card, self.player)
                    self.player.actions_to_play.append(action)
                    if len(self.player.actions_to_play) == 1:
                        action.do_reaction()
                    self.desk.draw()

    def click_on_action_button(self):
        if self.player.phase == 'action':
            self.start_buy_phase()
        elif self.player.phase == 'buy':
            self.start_cleanup()
        elif self.player.phase == 'action_play':
            action = self.player.actions_to_play[0]
            action.do_action()
        elif self.player.phase == 'attacked_reaction':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.top_card()
                    if card is not None:
                        action = Action(card, self.player)
                        self.player.actions_to_play.append(action)
                        if len(self.player.actions_to_play) == 1:
                            action.do_reaction()
            else:
                self.desk.clear_select()
                self.player.phase = 'other_players_turn'
                self.player.desk.changed.append('info')
                self.player.desk.draw()
                create_event(self.player.game.get_me(), 'send_reaction', { 'player' : self.player.name, 'defend' : 0, 'end' : 1 }, self.player.game.get_other_players_names())

    def click_on_info(self, section):
        if self.player.phase == 'action_play':
            if section in self.desk.selectable_info:
                self.desk.selected_info.append(section)   
                self.desk.selectable_info.remove(section)
                if len(self.desk.selected_piles) + len(self.desk.selected_info) == self.desk.to_select:
                    action = self.player.actions_to_play[0]
                    action.do_action()
            self.desk.draw()

    def play_card(self, card,):
        for trigger in self.player.desk.get_triggers('card_played'):
            trigger.card_played = card
            trigger.run()
        self.desk.put_card_to_play_area(card)
        self.desk.changed.append('play_area')
        create_event(self, 'played_action_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
        self.desk.draw()
        self.desk.clear_select()
        action = Action(card, self.player)
        self.player.actions_to_play.append(action)
        if len(self.player.actions_to_play) == 1:
            action.do_action()

    def play_treasure_card(self, card):
        for trigger in self.player.desk.get_triggers('card_played'):
            trigger.card_played = card
            trigger.run()
        self.desk.put_card_to_play_area(card)
        self.desk.changed.append('play_area') 
        create_event(self, 'played_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())        
        self.desk.draw()
        self.desk.clear_select()

    def cards_to_play(self):
        if self.player.actions > 0:
            selectable_piles = []
            for pile in self.player.hand:
                card = pile.top_card()
                if 'action' in card.type:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.desk.action_button_label = 'Ukončit akční fázi'
                self.desk.changed.append('action_button')
                self.desk.create_select(to_select = 1, select_type = 'optional', select_action = 'play', piles = selectable_piles, info = [])

    def action_card_select(self, to_select, select_type, select_action = 'select', piles = [], info = []):
        if select_type == 'optional' and to_select > 0:
            self.desk.action_button_label = 'Ukončit výběr'
            self.desk.changed.append('action_button') 
        else:
            self.desk.action_button_label = ''
        self.desk.create_select(to_select = to_select, select_type = select_type, select_action = select_action, piles = piles, info = info)

    def cards_to_buy(self):
        if self.player.buys > 0:
            selectable_piles = []
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                card = pile.top_card()
                if card is not None and card.price <= self.player.treasure:
                    selectable_piles.append(pile)
            for pile in self.player.hand:
                card = pile.top_card()
                if 'treasure' in card.type:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.desk.action_button_label = 'Ukončit fázi nákupu'
                self.desk.changed.append('action_button')
                self.desk.create_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
 