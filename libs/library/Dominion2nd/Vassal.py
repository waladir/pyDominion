from libs.classes.card import Card
from libs.classes.action import Action

class Vassal(Card):
    def __init__(self):
        self.id = 'vassal'
        self.name = 'Vazal' 
        self.name_en = 'Vassal'
        self.expansion = 'Dominion2nd'
        self.image = 'Vassal.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

        self.to_discard = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False        
            self.player.treasure = self.player.treasure + 2
            self.desk.changed.append('info')
            self.desk.draw()

        if self.action.phase != 'select':
            card = self.player.deck.get_top_card()
            if card is not None:
                if 'action' in card.type:
                    self.action.to_select = 1
                    self.desk.put_card_to_select_area(card)
                    self.action.selectable_cards.append(card)
                    self.desk.select_area_type = 'play_action'
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Označ jestli má být karta zahrána. Jinak bude odložena na odkládací balíček'
                    self.action.phase = 'select'
                    self.desk.changed.append('select_area')
                else:
                    self.player.put_card_to_discard(card)
                    self.action.cleanup()
                    self.desk.changed.append('players_deck')
                    self.desk.changed.append('players_discard')
                self.desk.draw
            else:
                self.action.cleanup()
                self.desk.draw
        else:
            if len(self.action.selected_cards) == 0:
                for card in self.action.selectable_cards:
                    card.pile.get_top_card()
                    self.desk.coalesce_select_area()
                    self.player.put_card_to_discard(card)
                self.desk.changed.append('players_discard')
                self.desk.changed.append('play_area')                    
            else:
                for card in self.action.selected_cards:
                    card.pile.get_top_card()
                    self.desk.coalesce_select_area()
                    self.desk.put_card_to_play_area(card) 
                self.player.action = Action(card, self.player)
                self.player.action.do_action()
                self.desk.changed.append('play_area')                    
            self.action.cleanup()
            self.desk.draw            

