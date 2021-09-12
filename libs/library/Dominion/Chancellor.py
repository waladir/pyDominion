from libs.classes.card import Card

class Chancellor(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'chancellor'
        self.name = 'Kancléř' 
        self.name_en = 'Chancellor'
        self.expansion = 'Dominion'
        self.image = 'Chancellor.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'action':
            self.player.treasure = self.player.treasure + 2
            self.desk.changed.append('info')
            self.desk.draw()          
            selectable_piles = []
            if len(self.player.deck.cards) > 0:
                selectable_piles.append(self.player.deck)
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'choose_action'
                self.desk.add_message('karty přesunout, ukonči výběr.')
                self.desk.add_message('Výběrem dobíracího balíčku ho přesuneš na odkládací. Pokud nechceš')
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'choose_action':
            if len(self.desk.selected_piles) == 0:
                self.action.cleanup()
            else:
                cards = self.player.get_cards_from_deck(len(self.player.deck.cards))
                for card in cards:
                    self.player.put_card_to_discard(card)   
                create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + ' přesunul dobírací balíček na odkládací'}, self.player.game.get_other_players_names())
                self.action.cleanup()
                self.desk.changed.append('players_deck')
                self.desk.changed.append('players_discard')
                self.desk.draw()
            self.action.cleanup()