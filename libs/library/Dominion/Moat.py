from libs.classes.card import Card

class Moat(Card):
    def __init__(self):
        self.id = 'moat'
        self.name = 'Hradní příkop' 
        self.name_en = 'Moat'
        self.expansion = 'Dominion'
        self.image = 'Moat.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'reaction'
        self.price = 2
        self.value = 0

    def do_action(self):
        if self.action.bonuses == True:
            self.action.bonuses = False   
            self.player.move_cards_from_deck_to_hand(2)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
        self.action.cleanup()

    def do_reaction(self):
        from libs.events import create_event
        create_event(self.player.game.get_me(), 'showed_card_from_hand', { 'player' : self.player.name, 'card_name' : self.name }, self.player.game.get_other_players_names())
        create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.action.attack_card.name_en, 'end': 0, 'defend' : 1 }, self.player.game.get_other_players_names())
        self.action.cleanup()
        self.player.phase = 'wait'
        self.desk.changed.append('players_hand')
        self.desk.changed.append('info')
        self.desk.changed.append('action_button')
        self.desk.draw()
        self.player.game.switch_player = True
