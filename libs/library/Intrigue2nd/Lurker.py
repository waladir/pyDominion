from libs.classes.card import Card
from libs.events import create_event

class Lurker(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'lurker'
        self.name = 'Zákeřník' 
        self.name_en = 'Lurker'
        self.expansion = 'Intrigue2nd'
        self.image = 'Lurker.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 2
        self.value = 0

        self.phase = 'select_action'

    def do_action(self):
        if self.phase == 'select_action':
            self.player.actions = self.player.actions + 1
            self.desk.changed.append('info')            
            self.desk.draw()        
            selectable_piles = []
            if len(self.desk.trash.cards)  > 0:
                selectable_piles.append(self.desk.trash)
            for pile in self.desk.kingdom_piles:
                card = pile.top_card()
                if card is not None and 'action' in card.type:
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'choose_action'
                self.desk.add_message('nebo smetiště, je-li na něm nějaká karta, pokud z něj kartu získáš.')
                self.desk.add_message('Vyber kartu akční kartu ze společné zásoby, kterou dáš na smetiště,')
                self.desk.draw()                
            else:
                self.action.cleanup()
                self.desk.draw()                
        elif self.phase == 'choose_action':
            if len(self.desk.selected_piles) > 0:
                for pile in self.desk.selected_piles:
                    if pile.place == 'trash':
                        self.desk.clear_select()
                        selectable_piles = []
                        for card in self.desk.trash.cards:
                            if card is not None and 'action' in card.type:
                                self.desk.put_card_to_select_area(card)
                        for pile in self.desk.select_area_piles:
                            selectable_piles.append(pile)
                        if len(selectable_piles) > 0:
                            self.player.activity.action_card_select(to_select = 1, select_type = 'mandatory', select_action = 'select', piles = selectable_piles, info = [])
                            self.desk.select_area = True
                            self.desk.select_area_label = 'Vyber akční kartu ze smetiště, kterou získáš'
                            self.phase = 'gain_card'
                            self.desk.changed.append('select_area')
                            self.desk.draw()
                        else:
                            self.action.cleanup()
                            self.desk.draw()
                    if pile.place == 'kingdom':
                        card = pile.get_top_card()
                        self.desk.trash.add_card(card) 
                        create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + ' zahodil kartu ' + card.name + ' ze společné zásoby na smetiště'}, self.player.game.get_other_players_names())
                        self.desk.changed.append('kingdom')
                        self.desk.changed.append('trash')
                        self.action.cleanup()
                        self.desk.changed.append('info')
                        self.desk.draw()
            else:
                self.action.cleanup()
        elif self.phase == 'gain_card':
            for pile in self.desk.selected_piles:
                self.desk.selectable_piles.remove(pile)
                card = pile.get_top_card()
                self.player.put_card_to_discard(card)
                create_event(self.player.game.get_me(), 'info_message', { 'message' : 'Hráč ' + self.player.name + ' získal kartu ' + card.name + ' ze smetiště'}, self.player.game.get_other_players_names())
            self.desk.changed.append('players_discard')
            self.desk.coalesce_select_area()
            for pile in self.desk.selectable_piles:
                card = pile.get_top_card()
                self.desk.trash.add_card(card) 
            self.desk.coalesce_select_area()
            self.desk.changed.append('trash')
            self.desk.select_area = False
            self.desk.changed.append('info')                
            self.desk.changed.append('play_area')
            self.action.cleanup()
            self.desk.draw()                