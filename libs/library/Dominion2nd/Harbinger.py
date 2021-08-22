from libs.classes.card import Card
from libs.classes.action import Action

class Harbinger(Card):
    def __init__(self):
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

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False    
            self.player.move_cards_from_deck_to_hand(1)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')                
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')
            self.desk.draw()

        if self.action.phase != 'select':
            cards = self.player.get_cards_from_discard(len(self.player.discard.cards))
            for card in cards:
                if card is not None:
                    self.desk.put_card_to_select_area(card)
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Můžeš vybrat kartu, která bude umístěna na tvůj dobírací balíček'
                self.action.phase = 'select'
                self.subphase = 'select_card'
                self.desk.changed.append('select_area')
                self.desk.changed.append('players_deck')
                self.desk.draw()
            else:
                self.action.cleanup()
                self.desk.changed.append('players_deck')
                self.desk.draw()
        else:
            for selected in self.action.selected_cards:
                pile = self.action.selected_cards[selected]
                card = pile.get_top_card()
                self.player.put_card_to_deck(card)
                self.desk.coalesce_select_area()
            self.desk.changed.append('players_deck')
            for card in self.action.selectable_cards:
                self.player.put_card_to_discard(card)
            self.desk.changed.append('players_discard')
            self.desk.select_area = False
            self.action.selectable_piles = []
            self.action.selected_piles = []
            self.action.selected_cards = {}
            self.desk.changed.append('play_area')
            self.action.cleanup()
            self.desk.draw()