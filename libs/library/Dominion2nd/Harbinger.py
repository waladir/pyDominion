from libs.classes.card import Card

class Harbinger(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'harbinger'
        self.name = 'Průzkumník' 
        self.name_en = 'Harbinger'
        self.expansion = 'Dominion2nd'
        self.image = 'Harbinger.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

        self.phase = 'select_from_discard'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_from_discard':
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')                
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()
            for card in self.player.get_cards_from_discard(len(self.player.discard.cards)):
                if card is not None:
                    self.desk.put_card_to_select_area(card)
            selectable_piles = []
            for pile in self.desk.select_area_piles:
                selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Můžeš vybrat kartu, která bude umístěna na tvůj dobírací balíček'
                self.phase = 'move_card_to_deck'
                self.desk.changed.append('select_area')
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'move_card_to_deck':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.put_card_to_deck(card)
                self.desk.coalesce_select_area()
                create_event(self.player.game.get_me(), 'move_card_from_discard_to_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.desk.changed.append('players_deck')
            for pile in self.desk.select_area_piles:
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)
            self.desk.coalesce_select_area()
            self.desk.changed.append('players_discard')
            self.desk.select_area = False
            self.desk.changed.append('play_area')
            self.action.cleanup()
            self.desk.draw()