from libs.classes.card import Card
from libs.classes.action import Action

class Throne_Room(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'throne_room'
        self.name = 'Trůnní sál' 
        self.name_en = 'Throne_Room'
        self.expansion = 'Dominion2nd'
        self.image = 'Throne_Room.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'select_to_play'

    def do_action(self):
        if self.phase == 'select_to_play':
            selectable_piles = []
            for pile in self.player.hand:
                card = pile.top_card()
                if 'action' in card.type:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'play_card'
                self.desk.add_message('Vyber kartu, kterou zahraješ 2x')
                self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'play_card':
            if len(self.desk.selected_piles) == 0:
                self.action.cleanup()
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.player.coalesce_hand()
                    self.desk.put_card_to_play_area(card) 
                    self.desk.changed.append('players_hand')
                    self.desk.changed.append('play_area')
                    self.desk.draw()
                    for i in range(2):
                        cardClass = pile.get_class(card.name_en)
                        virtual_card = cardClass() 
                        virtual_card.pile = None
                        virtual_card.game = self.player.game
                        virtual_card.desk = self.player.game.desk
                        virtual_card.player = self.player                          
                        action = Action(virtual_card, self.player)
                        self.player.actions_to_play.append(action)
                self.desk.clear_select()
                self.action.cleanup()        

