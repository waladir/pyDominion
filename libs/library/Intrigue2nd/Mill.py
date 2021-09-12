from libs.classes.card import Card

class Mill(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'mill'
        self.name = 'Mlýn' 
        self.name_en = 'Mill'
        self.expansion = 'Intrigue2nd'
        self.image = 'Mill.png'
        self.kingdom_card = True
        self.type = ['action', 'victory']
        self.subtype = None
        self.price = 4
        self.value = 1

        self.phase = 'select_to_discard'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_discard':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')            
            self.desk.draw()
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 2, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'discard_cards'
                self.desk.add_message('Vyber až dvě karty, které dáš na odkládací balíček')
                self.desk.draw()                
            else:
                self.action.cleanup()  
        else:
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.coalesce_hand()
                    self.player.put_card_to_discard(card)
                    create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                if len(self.desk.selected_piles) == 2:
                    self.player.treasure = self.player.treasure + 2
            self.action.cleanup()
            self.desk.changed.append('players_discard')
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.draw()
