from libs.classes.card import Card

class Nobles(Card):
    def __init__(self):
        self.id = 'nobles'
        self.name = 'Šlechtici' 
        self.name_en = 'Nobles'
        self.expansion = 'Intrigue'
        self.image = 'Nobles.png'
        self.kingdom_card = True
        self.type = ['action', 'victory']
        self.subtype = None
        self.price = 6
        self.value = 2

    def do_action(self):
        if self.action.phase != 'select':
            if len(self.player.deck.cards) + len(self.player.discard.cards) > 0:
                self.action.selectable_piles.append(self.player.deck)
            self.action.to_select = 1
            self.action.selectable_info = ['actions']
            self.action.phase = 'select'
            self.desk.draw()                
        else:
            if len(self.action.selected_piles) > 0:
                cards = self.player.get_cards_from_deck(3)
                for card in cards:
                    self.player.put_card_to_hand(card)   

            if len(self.action.selected_info) > 0:
                for section in self.action.selected_info:
                    if section == 'actions':
                        self.player.actions = self.player.actions + 2
            self.action.cleanup()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.draw()
