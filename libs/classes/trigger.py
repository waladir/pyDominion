# type : [card_played, set_price]
# duration : [end_of_round]

class Trigger():
    def __init__(self, card, player, type, duration):
        self.card = card
        self.player = player
        self.type = type
        self.duration = duration
        self.duration_end = None
        self.player.desk.triggers.append(self)

        self.card_played = None

    def run(self):
        eval('self.card.do_trigger_start()')

    def end_run(self):
        eval('self.card.do_trigger_end()')        

    

