from libs.classes.card import Card

class Wishing_Well(Card):
    def __init__(self):
        Card.__init__(self)        
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

        self.phase = 'select_to_choose'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_choose':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')            
            self.player.actions = self.player.actions + 2            
            self.desk.changed.append('info')
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                cardClass = pile.get_class(pile.card_name)
                card = cardClass()
                self.desk.put_card_to_select_area(card)
            selectable_piles = []
            for pile in self.desk.select_area_piles:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.phase = 'choose_card'
                self.desk.select_area_label = 'Označ kartu, která by měla být navrchu tvého dobíracího balíčku'
                self.desk.changed.append('select_area')
            else:
                self.action.cleanup()
            self.desk.draw()
        elif self.phase == 'choose_card':
            if len(self.desk.selected_piles) == 1:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    self.desk.add_message('Ukázal jsi kartu ' + card.name)  
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                    for pile in self.desk.selected_piles:
                        card_tip = pile.top_card()
                    if card_tip.name == card.name:
                        self.player.put_card_to_hand(card)
                        self.desk.add_message('Správný tip, karta si vezmeš do ruky')
                        self.desk.changed.append('players_deck')
                        self.desk.changed.append('players_hand')
                    else:
                        self.player.put_card_to_deck(card)
                        self.desk.add_message('Nesprávný tip, karta se vrátí do balíčku')
                self.desk.select_area = False
                for pile in self.desk.select_area_piles:
                    for card in pile.cards:
                        del card
                    self.desk.select_area_piles.remove(pile)
                self.desk.select_area_piles = []
            self.action.cleanup()
            self.desk.changed.append('play_area')
            self.desk.draw()
