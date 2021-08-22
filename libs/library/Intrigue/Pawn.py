from libs.classes.card import Card

class Pawn(Card):
    def __init__(self):
        self.id = 'pawn'
        self.name = 'Pěšák' 
        self.name_en = 'Pawn'
        self.expansion = 'Intrigue'
        self.image = 'Pawn.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

    def do_action(self):
        if self.action.phase != 'select':
            if len(self.player.deck.cards) + len(self.player.discard.cards) > 0:
                self.action.selectable_piles.append(self.player.deck)
            self.action.to_select = 2
            self.action.selectable_info = ['treasure', 'actions','buys']
            self.action.phase = 'select'
            self.desk.draw()                
        else:
            if len(self.action.selected_piles) > 0:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    self.player.put_card_to_hand(card)   

            if len(self.action.selected_info) > 0:
                for section in self.action.selected_info:
                    if section == 'treasure':
                        self.player.treasure = self.player.treasure + 1
                    if section == 'actions':
                        self.player.actions = self.player.actions + 1
                    if section == 'buys':
                        self.player.buys = self.player.buys + 1
            self.action.cleanup()
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.draw()
