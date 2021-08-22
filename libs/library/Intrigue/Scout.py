from libs.classes.card import Card

class Scout(Card):
    def __init__(self):
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

    def do_action(self):
        cards_to_hand = []
        from libs.events import create_event
        if self.action.bonuses == True:
            self.action.bonuses = False
            self.player.actions = self.player.actions + 1           
            cards = self.player.get_cards_from_deck(4)
            for card in cards:
                create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                if 'victory' in card.type:
                    self.player.put_card_to_hand(card)
                else:
                    self.desk.put_card_to_select_area(card)
                    self.action.selectable_cards.append(card)
                    self.action.to_select = 1
                    self.action.phase = 'select'
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Označuj postupně karty, které se v určeném pořadí vrátí do dobíracího balíčku'
                    self.desk.changed.append('select_area')
            if len(self.action.selectable_cards) == 0:
                self.action.cleanup()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
        elif self.action.phase == 'select':
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.put_card_to_deck(card)
                self.desk.changed.append('players_deck')
            if len(self.action.selectable_cards) > 0:
                self.action.selected_cards = {}
                self.action.to_select = 1
                self.desk.changed.append('select_area')
            else:
                self.desk.select_area = False
                self.desk.changed.append('play_area')
                self.action.cleanup()
            self.desk.draw()
