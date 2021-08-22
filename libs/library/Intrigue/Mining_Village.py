from libs.classes.card import Card

class Mining_Village(Card):
    def __init__(self):
        self.id = 'mining_village'
        self.name = 'Důlní osada' 
        self.name_en = 'Mining_Village'
        self.expansion = 'Intrigue'
        self.image = 'Mining_Village.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.move_cards_from_deck_to_hand(1)
            self.player.actions = self.player.actions + 2
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.draw()

        if self.action.phase != 'select':
            self.action.selectable_cards.append(self)
            self.action.to_select = 1
            self.action.phase = 'select'
            self.desk.changed.append('play_area')
            self.desk.draw()                
        else:
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.desk.trash.add_card(card)
                self.desk.coalesce_play_area()
                self.player.treasure = self.player.treasure + 2
            self.action.cleanup()
            self.desk.changed.append('play_area')
            self.desk.changed.append('trash')
            self.desk.changed.append('info')
            self.desk.draw() 