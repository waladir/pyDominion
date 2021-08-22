from libs.classes.card import Card

class Shanty_Town(Card):
    def __init__(self):
        self.id = 'shanty_town'
        self.name = 'Chudinská čtvrť' 
        self.name_en = 'Shanty_Town'
        self.expansion = 'Intrigue2nd'
        self.image = 'Shanty_Town.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 3
        self.value = 0

    def do_action(self):
        action_cards = 0
        from libs.events import create_event
        if self.action.bonuses == True:
            self.action.bonuses = False
            self.player.actions = self.player.actions + 2            
            self.desk.changed.append('info')
            piles = self.player.hand
            for pile in piles:
                card = pile.top_card()
                create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                if 'action' in card.type:
                    action_cards = action_cards + 1
            if action_cards == 0:
                self.player.move_cards_from_deck_to_hand(2)
            self.action.cleanup()            
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()

