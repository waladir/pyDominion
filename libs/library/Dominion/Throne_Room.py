from libs.classes.card import Card

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd

from libs.classes.action import Action

class Throne_Room(Card):
    def __init__(self):
        self.id = 'throne_room'
        self.name = 'Trůnní sál' 
        self.name_en = 'Throne_Room'
        self.expansion = 'Dominion'
        self.image = 'Throne_Room.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.actions = []

    def do_action(self):
        if self.action.phase != 'select':
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                if 'action' in card.type:
                    self.action.selectable_cards.append(card)
            if len(self.action.selectable_cards) > 0:
                self.action.to_select = 1
                self.action.phase = 'select'
                self.desk.draw()
            else:
                self.action.cleanup()
        else:
            if len(self.action.selected_cards) == 0:
                self.action.cleanup()
            else:
                for selected in self.action.selected_cards:
                    pile = self.action.selected_cards[selected]
                    card = pile.get_top_card()
                    self.player.coalesce_hand()
                    self.desk.put_card_to_play_area(card) 
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('play_area')
                    self.desk.draw()
                    for i in range(2):
                        cardClass = Dominion.get_class(card.name_en)
                        card_to_play = cardClass() 
                        card_to_play.pile = None
                        card_to_play.game = self.player.game
                        card_to_play.desk = self.player.game.desk
                        card_to_play.player = self.player                          
                        action = Action(card_to_play, self.player)
                        self.player.action = action
                        self.player.actions_to_play.append(action)
                        self.player.action = self.action
                        self.action.phase = 'play_action'
            self.action.cleanup()        

