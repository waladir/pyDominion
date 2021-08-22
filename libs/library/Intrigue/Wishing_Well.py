from libs.classes.card import Card

class Wishing_Well(Card):
    def __init__(self):
        self.id = 'wishing_well'
        self.name = 'Studna přání' 
        self.name_en = 'Wishing_Well'
        self.expansion = 'Intrigue'
        self.image = 'Wishing_Well.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')            
            self.player.actions = self.player.actions + 2            
            self.desk.changed.append('info')

        if self.action.phase != 'select':
            piles = self.desk.basic_piles + self.desk.kingdom_piles
            for pile in piles:
                cardClass = pile.get_class(pile.card_name)
                card = cardClass()
                self.desk.put_card_to_select_area(card)
                self.action.selectable_cards.append(card)
                self.action.to_select = 1
                self.action.phase = 'select'
                self.desk.select_area_type = 'select_action'
                self.action.select_cards = 'mandatory'
                self.desk.select_area = True
                self.desk.select_area_label = 'Označ karty, které by měla být navrchu tvého dobíracího balíčku'
                self.desk.changed.append('select_area')
            self.desk.draw()
        else:
            from libs.events import create_event
            if len(self.action.selected_cards) == 1:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    self.desk.add_message('Ukázal jsi kartu ' + card.name)  
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card_tip = pile.top_card()
                    if card_tip.name == card.name:
                        self.player.put_card_to_hand(card)
                        self.desk.changed.append('players_deck')
                        self.desk.changed.append('players_hand')
                    else:
                        self.player.put_card_to_deck(card)
                self.desk.select_area = False
                for pile in self.desk.select_area_piles:
                    for card in pile.cards:
                        del card
                    self.desk.select_area_piles.remove(pile)
                self.desk.select_area_piles = []
            self.action.cleanup()
            self.desk.draw()
