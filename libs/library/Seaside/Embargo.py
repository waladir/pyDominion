from libs.classes.card import Card
from libs.classes.trigger import Trigger

class Embargo(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'embargo'
        self.name = 'Embargo' 
        self.name_en = 'Embargo'
        self.expansion = 'Seaside'
        self.image = 'Embargo.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.phase = 'trash_card'
        self.trigger = None        

    def do_action(self):
        from libs.events import create_event  
        if self.phase == 'trash_card':
            self.player.treasure = self.player.treasure + 2
            selectable_piles = []
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])                
                self.desk.redraw_borders()    
                self.phase = 'place_token'              
                self.desk.add_message('Vyber balíček, na který vložíš token embarga')
            else:
                self.action.cleanup()
                self.desk.draw()                
        elif self.phase == 'place_token':
            if len(self.desk.selected_piles) == 1:
                for pile in self.desk.selected_piles:
                    self.trigger = Trigger(self, self.player, 'buy_token', 'forever', pile = pile)
                    self.trigger.description = 'E'
                    create_event(self, 'put_trigger_on_pile', { 'player' : self.player.name, 'pile_place' : pile.place, 'pile_position' : pile.position, 'card_name' : self.name_en, 'type' : 'buy_token', 'duration' : 'forever', 'description' : 'E' }, self.game.get_other_players_names())
                    card = self.pile.get_top_card()
                    self.desk.trash.add_card(card)
                    self.desk.coalesce_play_area()                    
            self.desk.changed.append('basic')
            self.desk.changed.append('kingdom')
            self.desk.changed.append('trash')
            self.desk.changed.append('play_area')
            self.desk.draw()
            self.action.cleanup()

    def do_trigger_start(self):
        from libs.events import create_event        
        for pile in self.desk.basic_piles:
            card = pile.top_card()
            if card is not None and card.name == 'Kletba':
                card = pile.get_top_card()
                if card is not None:
                    self.player.put_card_to_discard(card)
                    self.desk.add_message('Kvůli embargu jsi získal kartu ' + card.name)
                    create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
        self.desk.changed.append('basic')

    def do_trigger_end(self):
        pass
    