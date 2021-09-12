from libs.classes.card import Card

class Diplomat(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'diplomat'
        self.name = 'Diplomat' 
        self.name_en = 'Diplomat'
        self.expansion = 'Intrigue2nd'
        self.image = 'Diplomat.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'reaction'
        self.price = 4
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        self.player.move_cards_from_deck_to_hand(2)
        self.desk.changed.append('players_deck')
        self.desk.changed.append('players_hand')
        if len(self.player.hand) <= 5:
            self.player.actions = self.player.actions + 2
            self.desk.changed.append('info')
        self.desk.draw()
        self.action.cleanup()

    def do_reaction(self):
        from libs.events import create_event
        if self.phase == 'action':        
            create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : self.name }, self.player.game.get_other_players_names())            
            if len(self.player.hand) >= 5:
                self.player.move_cards_from_deck_to_hand(2)
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_hand')
                self.desk.draw()
                selectable_piles = []
                for pile in self.player.hand:
                    selectable_piles.append(pile)
                if len(selectable_piles) > 0:
                    if len(selectable_piles) > 3:
                        to_select = 3
                    else:
                        to_select = len(selectable_piles)
                    self.player.activity.action_card_select(to_select = to_select, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                    self.phase = 'return_to_deck'
                    self.desk.add_message('Vyber karty, které zahodíš na odkládací balíček')
                    self.desk.draw()                
            else:
                self.phase = 'action'
                self.desk.add_message('Máš v ruce méně než 5 karet')
                create_event(self.player.game.get_me(), 'send_reaction', { 'player' : self.player.name, 'defend' : 0, 'end' : 0 }, self.player.game.get_other_players_names())
                self.action.cleanup()
        elif self.phase == 'return_to_deck':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.coalesce_hand()
                    self.player.put_card_to_discard(card)
                    self.desk.add_message('Odložil jsi kartu ' + card.name + ' a svůj odkládací balíček')
                    create_event(self.player.game.get_me(), 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.desk.changed.append('players_discard')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            self.phase = 'action'
            create_event(self.player.game.get_me(), 'send_reaction', { 'player' : self.player.name, 'defend' : 0, 'end' : 0 }, self.player.game.get_other_players_names())
            self.action.cleanup()
