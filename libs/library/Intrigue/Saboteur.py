import json
from libs.classes.card import Card

class Saboteur(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'saboteur'
        self.name = 'Sabotér' 
        self.name_en = 'Saboteur'
        self.expansion = 'Intrigue'
        self.image = 'Saboteur.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'attack'
        self.price = 5
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        if self.phase == 'action':
            self.action.request_reactions()   
            self.phase = 'get_reactions'         
        elif self.phase == 'get_reactions':             
            self.phase = 'cleanup'
            self.action.do_attack()
        elif self.phase == 'cleanup':
            self.action.cleanup()        
            self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':   
            self.to_discard = []     
            skip = False
            while skip == False:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    if card is not None:
                        self.desk.add_message('Ukázal jsi kartu ' + card.name + ' z dobíracího balíčku')
                        create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                        if card.price >= 3:
                            card_price = card.price - 2
                            self.desk.trash.add_card(card) 
                            self.desk.changed.append('trash')
                            self.desk.add_message('Při útoku kartou Sabotér jsi zahodil kartu ' + card.name + ' na smetiště')
                            create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                            selectable_piles = []
                            for pile in self.desk.basic_piles + self.desk.kingdom_piles:
                                card = pile.top_card()
                                if card is not None and card.price <= card_price:
                                    selectable_piles.append(pile)
                            if len(selectable_piles) > 0:
                                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                                self.desk.add_message('Vyber kartu, kterou si můžeš vzít místo zahozené')
                                self.phase = 'gain_card'
                            skip = True
                        else:
                            self.to_discard.append(card)
                    else:
                        skip = True
                        self.attack_cleanup()
                self.desk.changed.append('players_deck')
                self.desk.draw()

        elif self.phase == 'gain_card':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    card = pile.top_card()
                    if card is not None:
                        card = pile.get_top_card()
                        self.player.put_card_to_discard(card) 
                        create_event(self, 'gain_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                self.desk.changed.append('players_discard')
                self.desk.draw()
            self.attack_cleanup()

    def attack_cleanup(self):
        from libs.events import create_event
        if len(self.to_discard) > 0:
            for card in self.to_discard:
                self.player.put_card_to_discard(card)
                self.desk.add_message('Zahodil jsi kartu ' + card.name + ' z dobíracího na odkládací balíček')
                create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
            self.desk.changed.append('players_discard')
            self.desk.draw()
        create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps(None) }, self.player.game.get_other_players_names())
        self.action.cleanup()
