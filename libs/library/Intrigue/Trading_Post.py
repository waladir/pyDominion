from libs.classes.card import Card

class Trading_Post(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'trading_post'
        self.name = 'Obchodní misto' 
        self.name_en = 'Trading_Post'
        self.expansion = 'Intrigue'
        self.image = 'Trading_Post.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.phase = 'select_to_trash'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_trash':
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 2, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'trash_cards'
                self.desk.add_message('Vyber karty, které zahodíš na smetiště')
                self.desk.draw()                
            else:
                self.action.cleanup()               
        elif self.phase == 'trash_cards':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.desk.trash.add_card(card)
                    create_event(self, 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.player.coalesce_hand()
                if len(self.desk.selected_piles) == 2:
                    for pile in self.desk.basic_piles:
                        card = pile.top_card()
                        if card is not None and card.name == 'Stříbrňák':
                            card = pile.get_top_card()
                            self.player.put_card_to_discard(card)                
                            create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())                            
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('trash')
            self.desk.draw() 