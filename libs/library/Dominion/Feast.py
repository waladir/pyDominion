from libs.classes.card import Card

class Feast(Card):
    def __init__(self):
        Card.__init__(self)        
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

        self.phase = 'select_to_gain'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_gain':
            selectable_piles = []
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                card = pile.top_card()
                if card is not None and card.price <= 5:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'gain_card'
                self.desk.add_message('Vyber kartu, kterou chceš získat. Hostina bude zahozena na smetiště.')
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'gain_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)  
                create_event(self.player.game.get_me(), 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            for pile in self.desk.play_area_piles:
                card = pile.top_card()
                if card == self.action.card:
                    card = pile.get_top_card()
                    self.desk.trash.add_card(card)
                    create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.desk.coalesce_play_area()
            self.action.cleanup()
            self.desk.changed.append('basic')
            self.desk.changed.append('kingdom')
            self.desk.changed.append('trash')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('play_area')            
            self.desk.draw()
