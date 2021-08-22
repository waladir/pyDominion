from libs.classes.card import Card

class Council_Room(Card):
    def __init__(self):
        self.id = 'council_room'
        self.name = 'Zasedání rady' 
        self.name_en = 'Council_Room'
        self.expansion = 'Dominion'
        self.image = 'Council_Room.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

    def do_action(self):
        from libs.events import create_event
        if self.action.bonuses == True:
            self.action.bonuses = False     
            self.player.move_cards_from_deck_to_hand(4)
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.player.buys = self.player.buys + 1
            self.desk.changed.append('info')
            other_players = self.player.game.get_other_players_names()
            create_event(self.player.game.get_me(), 'do_draw_card', { 'player' : self.player.name, 'card_name' : self.name_en }, other_players)
            self.desk.draw()
        self.action.cleanup()
