from libs.classes.card import Card

class Diplomat(Card):
    def __init__(self):
        self.id = 'diplomat'
        self.name = 'Diplomat' 
        self.name_en = 'Diplomat'
        self.expansion = 'Intrigue2nd'
        self.image = 'Diplomat.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'reaction'
        self.price = 4
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False   
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            if len(self.player.hand) <= 5:
                self.player.actions = self.player.actions + 2
                self.desk.changed.append('info')
            self.desk.draw()
        self.action.cleanup()

    def do_reaction(self):
        from libs.events import create_event
        self.action.cleanup()
        self.player.phase = 'wait'
        if len(self.player.hand) >= 5:
            self.player.move_cards_from_deck_to_hand(2)



        self.desk.changed.append('players_hand')
        self.desk.changed.append('info')
        self.desk.changed.append('action_button')
        self.desk.draw()
        self.player.game.switch_player = True
        create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : self.name }, self.player.game.get_other_players_names())
        create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.player.attack_card.name_en }, self.player.game.get_other_players_names())
