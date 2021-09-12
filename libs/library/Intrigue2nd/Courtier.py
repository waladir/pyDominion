from libs.classes.card import Card

class Courtier(Card):
    def __init__(self):
        Card.__init__(self)        
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

        self.phase = 'select_card_to_show'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_card_to_show':
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'show_card'             
                self.desk.add_message('Vyber kartu, kterou ukážeš')
                self.desk.draw()   
            else:
                self.action.cleanup()
        elif self.phase == 'show_card':
            for pile in self.desk.selected_piles:
                card = pile.top_card()
                create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())                    
                types = 0
                types = len(card.type)
                if card.subtype is not None:
                    types = types + 1
            if types > 0:
                self.desk.clear_select()
                selectable_piles = []
                selectable_info = ['treasure', 'actions','buys']
                for pile in self.desk.basic_piles:
                    card = pile.top_card()
                    if card is not None and card.name == 'Zlaťák':
                        selectable_piles.append(pile)
                self.player.activity.action_card_select(to_select = types, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = selectable_info)
                self.phase = 'get_choice'             
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'get_choice':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.put_card_to_discard(card) 
                    self.desk.changed.append('players_discard')
                    create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
            if len(self.desk.selected_info) > 0:
                for section in self.desk.selected_info:
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
