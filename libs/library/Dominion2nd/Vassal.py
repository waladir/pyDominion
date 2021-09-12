from libs.classes.card import Card

class Vassal(Card):
    def __init__(self):
        Card.__init__(self)        
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

        self.phase = 'action'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'action':
            self.player.treasure = self.player.treasure + 2
            self.desk.changed.append('info')
            card = self.player.deck.get_top_card()
            if card is not None:
                create_event(self.player.game.get_me(), 'draw_card', { 'player' : self.player.name, 'count' : 1 }, self.player.game.get_other_players_names())
                if 'action' in card.type:
                    self.desk.put_card_to_select_area(card)
                    selectable_piles = []
                    for pile in self.desk.select_area_piles:
                        selectable_piles.append(pile)
                    self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'play', piles = selectable_piles, info = [])
                    self.desk.select_area = True
                    self.desk.select_area_label = 'Označ jestli má být karta zahrána. Pokud ukončíš výběr, bude odložena na odkládací balíček'
                    self.desk.changed.append('select_area')
                    self.phase = 'play_or_discard'
                else:
                    self.player.put_card_to_discard(card)
                    self.action.cleanup()
                    self.desk.changed.append('players_deck')
                    self.desk.changed.append('players_discard')
            else:
                self.action.cleanup()
            self.desk.draw()
        elif self.phase == 'play_or_discard':
            if len(self.desk.selected_piles) == 0:
                for pile in self.desk.selectable_piles:
                    card = pile.get_top_card()
                    self.desk.coalesce_select_area()
                    self.player.put_card_to_discard(card)
                    create_event(self.player.game.get_me(), 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                self.desk.changed.append('players_discard')
            else:
                for pile in self.desk.selected_piles:
                    card = pile.get_top_card()
                    self.desk.coalesce_select_area()
                    self.player.activity.play_card(card)
            self.desk.select_area = False
            self.desk.changed.append('play_area')                    
            self.action.cleanup()
            self.desk.draw()        

