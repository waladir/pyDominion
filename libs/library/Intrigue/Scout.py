from libs.classes.card import Card

class Scout(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'scout'
        self.name = 'Zvěd' 
        self.name_en = 'Scout'
        self.expansion = 'Intrigue'
        self.image = 'Scout.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'select_to_return_to_deck'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_return_to_deck':
            self.player.actions = self.player.actions + 1           
            self.desk.changed.append('info')      
            cards = self.player.get_cards_from_deck(4)
            for card in cards:
                create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                if 'victory' in card.type:
                    self.player.put_card_to_hand(card)
                else:
                    self.desk.put_card_to_select_area(card)
            selectable_piles = []
            for pile in self.desk.select_area_piles:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Označuj postupně karty, které se v určeném pořadí vrátí do dobíracího balíčku'
                self.phase = 'return_to_deck'
                self.desk.changed.append('select_area')
            else:
                self.action.cleanup()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
        elif self.phase == 'return_to_deck':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_deck(card)
                self.desk.coalesce_select_area()
                self.desk.changed.append('players_deck')
                self.desk.changed.append('select_area')
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
