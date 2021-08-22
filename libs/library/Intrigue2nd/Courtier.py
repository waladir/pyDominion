from libs.classes.card import Card

class Courtier(Card):
    def __init__(self):
        self.id = 'courtier'
        self.name = 'Dvořan' 
        self.name_en = 'Courtier'
        self.expansion = 'Intrigue2nd'
        self.image = 'Courtier.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.subphase = ''

    def do_action(self):
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.action.select_cards = 'mandatory'
                self.desk.draw()   
                self.subphase = 'select_card'             
            else:
                self.action.cleanup()
        else:
            if self.subphase == 'select_card':
                from libs.events import create_event
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.top_card()
                    create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                    
                    types = 0
                    types = len(card.type)
                    if card.subtype is not None:
                        types = types + 1
                if types > 0:
                    self.action.selectable_cards = []
                    self.action.selected_cards = {}
                    self.action.to_select = types
                    self.action.selectable_info = ['treasure', 'actions','buys']
                    for pile in self.desk.basic_piles:
                        card = pile.top_card()
                        if card.name == 'Zlaťák':
                            self.action.selectable_cards.append(card)
                    self.subphase = 'get_choice'             
                    self.action.cleanup()
                    self.desk.draw()
            elif self.subphase == 'get_choice':
                if len(self.action.selected_cards) > 0:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.player.put_card_to_discard(card) 
                        self.desk.changed.append('players_discard')
                if len(self.action.selected_info) > 0:
                    for section in self.action.selected_info:
                        if section == 'treasure':
                            self.player.treasure = self.player.treasure + 3
                        if section == 'actions':
                            self.player.actions = self.player.actions + 1
                        if section == 'buys':
                            self.player.buys = self.player.buys + 1
                self.action.cleanup()
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_hand')
                self.desk.changed.append('info')
                self.desk.draw()
