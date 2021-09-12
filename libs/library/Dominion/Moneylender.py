from libs.classes.card import Card

class Moneylender(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'moneylender'
        self.name = 'Lichvář' 
        self.name_en = 'Moneylender'
        self.expansion = 'Dominion'
        self.image = 'Moneylender.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 4
        self.value = 0

        self.phase = 'select_to_trash'

    def do_action(self):
        from libs.events import create_event
        if self.phase == 'select_to_trash':
            selectable_piles = []
            for pile in self.player.hand:
                card = pile.top_card()
                if card.name == 'Měďák':
                    selectable_piles.append(pile)
            if len(selectable_piles) > 0:
                self.player.activity.action_card_select(to_select = 1, select_type = 'optional', select_action = 'select', piles = selectable_piles, info = [])
                self.phase = 'trash_card'
                self.desk.add_message('Můžeš vybrat kartu Mědák, kterou zahodíš na smetiště')
                self.desk.draw()                
            else:
                self.action.cleanup()
        elif self.phase == 'trash_card':
            for pile in self.desk.selected_piles:
                card = pile.get_top_card()
                self.player.coalesce_hand()
                self.desk.trash.add_card(card)
                self.player.treasure = self.player.treasure + 3
                create_event(self.player.game.get_me(), 'trash_card', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
            self.player.coalesce_hand()
            self.action.cleanup()
            self.desk.changed.append('players_hand')
            self.desk.changed.append('info')
            self.desk.changed.append('trash')
            self.desk.draw()  

