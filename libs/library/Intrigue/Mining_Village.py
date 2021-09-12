from libs.classes.card import Card

class Mining_Village(Card):
    def __init__(self):
        Card.__init__(self)        
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

        self.phase = 'select_to_trash'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_trash':
            self.player.move_cards_from_deck_to_hand(1)
            self.player.actions = self.player.actions + 2
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.draw()
            selectable_piles = []
            selectable_piles.append(self.pile)
            self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
            self.phase = 'trash_card'
            self.desk.add_message('nebo ukonči výběr jestli si ji chceš ponechat')
            self.desk.add_message('Vyber kartu, pokud ji chceš zahodit na smetiště,')
            self.desk.changed.append('play_area')
            self.desk.draw()                
        elif self.phase == 'trash_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.desk.trash.add_card(card)
                create_event(self, 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.desk.coalesce_play_area()
                self.player.treasure = self.player.treasure + 2
            self.action.cleanup()
            self.desk.changed.append('play_area')
            self.desk.changed.append('trash')
            self.desk.changed.append('info')
            self.desk.draw() 