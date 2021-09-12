from libs.classes.card import Card

class Patrol(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'patrol'
        self.name = 'Hlídka' 
        self.name_en = 'Patrol'
        self.expansion = 'Intrigue2nd'
        self.image = 'Patrol.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.phase = 'get_cards'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'get_cards':
            action_cards = 0
            self.player.move_cards_from_deck_to_hand(3)          
            self.desk.changed.append('player_deck')
            self.desk.changed.append('player_hand')
            cards = self.player.get_cards_from_deck(4)
            for card in cards:
                create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                if 'victory' in card.type or 'curse' in card.type: 
                    self.player.put_card_to_hand(card)
                else:
                    self.desk.put_card_to_select_area(card)
            selectable_piles = []
            for pile in self.desk.select_area_piles:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'return_card_to_deck'
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Označuj postupně karty, které se v určeném pořadí vrátí do dobíracího balíčku'
                self.desk.changed.append('select_area')
            else:
                self.action.cleanup()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
        elif self.phase == 'return_card_to_deck':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_deck(card)
                self.desk.coalesce_select_area()
                create_event(self, 'move_card_from_hand_to_deck', { 'player' : self.player.name }, self.game.get_other_players_names())
                self.desk.changed.append('players_deck')
            if len(self.desk.selectable_piles) > 0:
                self.desk.clear_select()
                selectable_piles = []
                for pile in self.desk.select_area_piles:
                    selectable_piles.append(pile)
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.changed.append('select_area')
            else:
                self.desk.select_area = False
                self.desk.changed.append('play_area')
                self.action.cleanup()
            self.desk.draw()
