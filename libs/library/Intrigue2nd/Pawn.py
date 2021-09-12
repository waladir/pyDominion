from libs.classes.card import Card

class Pawn(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'pawn'
        self.name = 'Pěšák' 
        self.name_en = 'Pawn'
        self.expansion = 'Intrigue2nd'
        self.image = 'Pawn.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.phase = 'select_bonus'

    def do_action(self):
        if self.phase == 'select_bonus':
            selectable_piles = []
            if len(self.player.deck.cards) + len(self.player.discard.cards) > 0:
                selectable_piles.append(self.player.deck)
            selectable_info = ['treasure', 'actions','buys']
            self.player.activity.action_card_select(to_select = 2, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = selectable_info)
            self.phase = 'get_bonus'
            self.desk.draw()                
        elif self.phase == 'get_bonus':
            if len(self.desk.selected_piles) > 0:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    self.player.put_card_to_hand(card)   
            if len(self.desk.selected_info) > 0:
                for section in self.desk.selected_info:
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
