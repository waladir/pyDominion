# type : [card_played, set_price]
# duration : [end_of_round]

class Trigger():
    def __init__(self, card, player, type, duration, pile = None):
        self.card = card
        self.player = player
        self.type = type
        self.duration = duration
        self.duration_end = None
        self.pile = pile
        self.description = ''
        self.player.desk.triggers.append(self)

        self.card_played = None

    def run(self):
        self.card.trigger = self
        eval('self.card.do_trigger_start()')

    def end_run(self):
        self.card.trigger = self
        eval('self.card.do_trigger_end()')        

    

