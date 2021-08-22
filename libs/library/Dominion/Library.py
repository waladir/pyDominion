from libs.classes.card import Card
from libs.classes.action import Action

class Library(Card):
    def __init__(self):
        self.id = 'library'
        self.name = 'Sklepení' 
        self.name_en = 'Library'
        self.expansion = 'Dominion'
        self.image = 'Library.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

    def do_action(self):
        if self.action.phase != 'select' or self.action.to_select > 0:
            hand_count = len(self.player.hand)
            skip = False
            while hand_count < 7 and len(self.player.deck.cards) + len(self.player.discard.cards) > 0 and skip == False:
                cards = self.player.get_cards_from_deck(1)
                for card in cards:
                    if 'action' in card.type:
                        self.action.selectable_cards.append(card)
                        self.desk.put_card_to_select_area(card)
                        self.action.to_select = 1
                        self.action.phase = 'select'
                        self.desk.select_area_type = 'select_action'
                        self.desk.select_area = True
                        self.desk.select_area_label = 'Označ akční karty, které chceš dát stranou'
                        self.desk.changed.append('players_deck')
                        self.desk.changed.append('select_area')
                        self.desk.draw()
                        skip = True
                    else:
                        self.desk.select_area = False
                        self.player.put_card_to_hand(card)
                        self.player.coalesce_hand()
                        self.desk.changed.append('players_hand')
                        self.desk.changed.append('players_deck')
                        self.desk.draw()                        
            hand_count = len(self.player.hand)
            if  hand_count >= 7 or len(self.player.deck.cards) + len(self.player.discard.cards) <= 0:
                self.desk.select_area = False
                for card in self.action.skipped_cards:               
                    self.player.put_card_to_discard(card)
                self.action.cleanup()
                self.desk.changed.append('select_area')
                self.desk.changed.append('players_discard')                
                self.desk.draw()
        else:
            if len(self.action.selected_cards) == 0:
                for card in self.action.selectable_cards:
                    self.player.put_card_to_hand(card)                 
                self.player.coalesce_hand()
                self.desk.changed.append('players_hand')                
                self.desk.changed.append('select_area')
                self.desk.draw()                    
            else:
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.action.skipped_cards.append(card)
                self.desk.coalesce_select_area()                    
                self.desk.changed.append('select_area')
                self.desk.draw()                    

            hand_count = len(self.player.hand)
            if hand_count < 7 and len(self.player.deck.cards) + len(self.player.discard.cards) > 0:    
                self.action.selectable_cards = []
                self.action.selected_cards = {}
                self.desk.select_area = False
                self.desk.select_area_piles = []
                self.action.to_select = 1
                self.action.phase = 'select'
                self.do_action()
            else:
                self.desk.select_area = False
                for card in self.action.skipped_cards:               
                    self.player.put_card_to_discard(card)
                self.action.cleanup()

                self.desk.changed.append('players_discard')                
                self.desk.draw()

