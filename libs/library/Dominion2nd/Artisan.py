from libs.classes.card import Card

class Artisan(Card):
    def __init__(self):
        self.id = 'artisan'
        self.name = 'Řemeslník' 
        self.name_en = 'Artisan'
        self.expansion = 'Dominion2nd'
        self.image = 'Artisan.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 6
        self.value = 0

        self.subphase = ''

    def do_action(self):
        if self.action.phase != 'select':
            piles = self.desk.basic_piles + self.desk.kingdom_piles
            for pile in piles:
                card = pile.top_card()
                if card.price <= 5:
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.desk.draw()
            else:
                self.action.cleanup()
        else:
            if self.subphase != 'select_to_deck':
                if len(self.action.selected_cards) > 0:
                    for selected in self.action.selected_cards:
                        pile = self.action.selected_cards[selected]
                        card = pile.get_top_card()
                        self.player.put_card_to_hand(card)
                        self.desk.changed.append('players_hand')
                self.action.selectable_cards = []
                self.action.selected_cards = {}
                self.desk.draw()
                piles = self.player.hand
                for pile in piles:
                    card = pile.top_card()
                    self.action.selectable_cards.append(card)
                if len(self.action.selectable_cards) > 0:
                    self.action.to_select = 1
                    self.subphase = 'select_to_deck'
                    self.desk.draw()
                else:
                    self.action.cleanup()
            else:
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.player.put_card_to_deck(card) 
                    self.player.coalesce_hand()
                    self.action.cleanup()                    
                    self.desk.changed.append('players_deck')
                    self.desk.changed.append('players_hand')
                    self.desk.draw()


