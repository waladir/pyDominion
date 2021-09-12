from libs.classes.card import Card

class Ironworks(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'ironworks'
        self.name = 'Hutě' 
        self.name_en = 'Ironworks'
        self.expansion = 'Intrigue'
        self.image = 'Ironworks.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'cards_to_get'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'cards_to_get':
            selectable_piles = []
            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                card = pile.top_card()
                if card is not None and card.price <= 4:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'gain_card'
                self.desk.draw()                
            else:
                self.action.cleanup()
        else:
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)  
                create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                if 'action' in card.type:
                    self.player.actions = self.player.actions + 1
                if 'treasure' in card.type:
                    self.player.treasure = self.player.treasure + 1
                if 'victory' in card.type:
                    self.player.move_cards_from_deck_to_hand(1)
                    self.desk.changed.append('players_deck')
                    self.desk.changed.append('players_hand')                                       
            self.action.cleanup()
            self.desk.changed.append('basic')
            self.desk.changed.append('kingdom')
            self.desk.changed.append('players_discard')
            self.desk.changed.append('info')
            self.desk.draw()

