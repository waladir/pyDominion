from libs.classes.card import Card
class Feast(Card):
    def __init__(self):
        self.id = 'feast'
        self.name = 'Hostina' 
        self.name_en = 'Feast'
        self.expansion = 'Dominion'
        self.image = 'Feast.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

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
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)  
            for pile in self.desk.play_area_piles:
                card = pile.top_card()
                if card == self.action.card:
                    card = pile.get_top_card()
                    self.desk.trash.add_card(self.action.card)
            self.desk.coalesce_play_area()
            self.action.cleanup()
            self.desk.changed.append('basic')
            self.desk.changed.append('kingdom')
            self.desk.changed.append('trash')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('play_area')            
            self.desk.draw()
