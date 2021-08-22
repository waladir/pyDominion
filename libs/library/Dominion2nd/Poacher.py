from libs.classes.card import Card

class Poacher(Card):
    def __init__(self):
        self.id = 'poacher'
        self.name = 'Pytlák' 
        self.name_en = 'Poacher'
        self.expansion = 'Dominion2nd'
        self.image = 'Poacher.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.to_discard = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.player.treasure = self.player.treasure + 1
            self.desk.changed.append('info')
            self.desk.draw()

        if self.action.phase != 'select':
            piles = self.desk.basic_piles + self.desk.kingdom_piles
            for pile in piles:
                if len(pile.cards) == 0:
                    self.to_discard = self.to_discard + 1
            if self.to_discard > 0:
                piles = self.player.hand
                for pile in piles:
                    card = pile.top_card()
                    self.action.selectable_cards.append(card)
                if len(self.action.selectable_cards) > 0:
                    self.action.to_select = self.to_discard
                    self.action.phase = 'select'
                    self.desk.draw()
                else:
                    self.action.cleanup()
            else:
                self.action.cleanup()
        else:
            if len(self.action.selected_cards) == 0:
                self.action.cleanup()
            else:
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.desk.trash.add_card(card)
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')
                self.desk.changed.append('trash')
            self.action.cleanup()                    
            self.desk.draw()



            