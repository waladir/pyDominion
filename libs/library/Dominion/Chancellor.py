from libs.classes.card import Card

class Chancellor(Card):
    def __init__(self):
        self.id = 'chancellor'
        self.name = 'Kancléř' 
        self.name_en = 'Chancellor'
        self.expansion = 'Dominion'
        self.image = 'Chancellor.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.treasure = self.player.treasure + 2
            self.desk.changed.append('info')
            self.desk.draw()          

        if self.action.phase != 'select':
            if len(self.player.deck.cards) > 0:
                self.action.to_select = 1
                self.action.selectable_piles.append(self.player.deck)
                self.action.phase = 'select'
                self.desk.draw()
        else:
            if len(self.action.selected_piles) == 0:
                self.action.cleanup()
            else:
                cards = self.player.get_cards_from_deck(len(self.player.deck.cards))
                for card in cards:
                    self.player.put_card_to_discard(card)   
                self.action.cleanup()
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_discard')
                self.desk.draw()
            self.action.cleanup()