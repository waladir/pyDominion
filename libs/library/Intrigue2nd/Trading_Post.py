from libs.classes.card import Card

class Trading_Post(Card):
    def __init__(self):
        self.id = 'trading_post'
        self.name = 'Obchodní misto' 
        self.name_en = 'Trading_Post'
        self.expansion = 'Intrigue2nd'
        self.image = 'Trading_Post.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

    def do_action(self):
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 2
                self.action.phase = 'select'
                self.desk.draw()                
            else:
                self.action.cleanup()               
        else:
            if len(self.action.selected_cards) > 0:
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.desk.trash.add_card(card)
                if len(self.action.selected_cards) == 2:
                    self.player.coalesce_hand()
                    piles = self.desk.basic_piles
                    for pile in piles:
                        card = pile.top_card()
                        if card.name == 'Stříbrňák':
                            card = pile.get_top_card()
                            if card is not None:
                                self.player.put_card_to_discard(card)                
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('trash')
            self.desk.draw() 