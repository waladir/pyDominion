from libs.classes.card import Card

class Moneylender(Card):
    def __init__(self):
        self.id = 'moneylender'
        self.name = 'Lichvář' 
        self.name_en = 'Moneylender'
        self.expansion = 'Dominion2nd'
        self.image = 'Moneylender.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

    def do_action(self):
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                if card.name == 'Měďák':
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.desk.draw()                
            else:
                self.action.cleanup()
        else:
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.desk.trash.add_card(card)
                self.player.treasure = self.player.treasure + 3
            self.player.coalesce_hand()
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.changed.append('trash')
            self.desk.draw()  

