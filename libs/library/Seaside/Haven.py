from libs.classes.card import Card
from libs.classes.trigger import Trigger

class Haven(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'haven'
        self.name = 'Přístav' 
        self.name_en = 'Haven'
        self.expansion = 'Seaside'
        self.image = 'Haven.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'duration'
        self.price = 2
        self.value = 0

        self.phase = 'action'
        self.trigger = None   
        self.selected_card = None

    def do_action(self):
        if self.phase =='action':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            selectable_piles = []
            for pile in self.player.hand:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])                
                self.desk.redraw_borders()
                self.phase = 'select_card'              
                self.desk.add_message('Vyber kartu, která bude vrácená do ruky v příštím kole')
                self.desk.draw()
            else:
                self.action.cleanup()
                self.desk.draw()                
        elif self.phase == 'select_card':
            self.phase = 'cleanup'
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()    
                    if card is not None:
                        card.hidden = -1
                        self.desk.put_card_to_play_area(card, hidden = card.hidden)   
                        card.skip_cleanup = True  
                        self.desk.changed.append('play_area')
                        self.player.coalesce_hand()
                        self.selected_card = card
                        self.skip_cleanup = True
                        self.trigger = Trigger(self, self.player, 'next_round_start', 'next_round')
            self.action.cleanup()
            self.desk.draw()
        elif self.phase == 'cleanup':
            self.action.cleanup()
            self.desk.draw()

    def do_trigger_start(self):
        from libs.events import create_event     
        for pile in self.desk.play_area_piles:
            card = pile.top_card()
            if card is not None and card == self.selected_card :
                card = pile.get_top_card()
                if card is not None:
                    card.skip_cleanup = False
                    card.hidden = 0
                    self.skip_cleanup = False
                    self.selected_card = None
                    self.player.put_card_to_hand(card)
                    self.desk.add_message('Kartu ' + card.name + ' jsi vrátil do ruky')
                    create_event(self, 'return_hidden_card_to_hand', { 'player' : self.player.name }, self.game.get_other_players_names())
        self.desk.coalesce_play_area()
        self.desk.changed.append('play_area')
        self.desk.changed.append('players_hand')
        self.desk.triggers.remove(self.trigger)
        del self.trigger            
        self.desk.draw()

    def do_trigger_end(self):
        pass