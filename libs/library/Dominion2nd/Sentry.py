from libs.classes.card import Card
from libs.classes.action import Action

class Sentry(Card):
    def __init__(self):
        self.id = 'sentry'
        self.name = 'Stráž' 
        self.name_en = 'Sentry'
        self.expansion = 'Dominion2nd'
        self.image = 'Sentry.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0
        self.cards_to_deal_with = []
        self.subphase = ''

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
            cards = self.player.get_cards_from_deck(2)
            for card in cards:
                if card is not None:
                    self.cards_to_deal_with.append(card)
                    self.desk.put_card_to_select_area(card)
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.select_cards = 'mandatory'
                self.desk.select_area_type = 'select_action'
                self.desk.select_area = True
                self.desk.select_area_label = 'Vyber kartu'
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
            if self.subphase == 'move_card':
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    cards_to_deal_with = self.cards_to_deal_with
                    self.cards_to_deal_with = []
                    for card_to_deal_with in cards_to_deal_with:
                        if card_to_deal_with != card:
                            self.cards_to_deal_with.append(card_to_deal_with)
                for pile in self.action.selected_piles:
                    if pile == self.player.deck:
                        self.player.put_card_to_deck(card)
                    if pile == self.player.discard:
                        self.player.put_card_to_discard(card)
                    if pile == self.desk.trash:
                        self.desk.trash.add_card(card)
                self.desk.changed.append('players_deck') 
                self.desk.changed.append('players_discard') 
                self.desk.changed.append('trash')  
                if len(self.cards_to_deal_with) > 0:
                    self.action.selectable_cards = self.cards_to_deal_with
                    self.action.selectable_piles = []
                    self.action.selected_piles = []
                    self.action.selected_cards = {}
                    self.action.to_select = 1
                    self.action.select_cards = 'mandatory'
                    self.desk.select_area_type = 'select_action'
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Vyber kartu'
                    self.subphase = 'select_card'
                    self.action.phase = 'select'
                    self.desk.changed.append('select_area')
                    self.desk.draw()
                else:
                    self.action.cleanup()
                    self.desk.select_area = False
                    self.desk.changed.append('play_area')
                    self.desk.draw()
            elif self.subphase == 'select_card':
                if len(self.action.selected_cards) > 0:
                    self.desk.select_area_label = 'Označ jestli má být vrácená na dobírací balíček, odložená na odkládací balíček nebo zahozená na smetiště'
                    self.desk.changed.append('select_area') 
                    self.subphase = 'move_card'
                    self.action.selectable_cards = []
                    self.action.selectable_piles.append(self.player.deck)
                    self.action.selectable_piles.append(self.player.discard)
                    self.action.selectable_piles.append(self.desk.trash)
                    self.desk.changed.append('players_deck') 
                    self.desk.changed.append('players_discard') 
                    self.desk.changed.append('trash') 
                    self.action.to_select = 2
                    self.action.select_cards = 'mandatory'
                    self.desk.draw()                   
                else:
                    self.desk.changed.append('play_area')                    
                    self.action.cleanup()
                    self.desk.draw()



