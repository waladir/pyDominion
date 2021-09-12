from libs.classes.card import Card
from libs.classes.trigger import Trigger

class Lighthouse(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'lighthouse'
        self.name = 'Maják' 
        self.name_en = 'Lighthouse'
        self.expansion = 'Seaside'
        self.image = 'Lighthouse.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = 'duration'
        self.price = 2
        self.value = 0

        self.phase = 'action'
        self.selected_card = None
        self.trigger = None   
        self.triggers = []

    def do_action(self):
        self.player.actions = self.player.actions + 1
        self.player.treasure = self.player.treasure + 1
        self.desk.changed.append('info')
        self.skip_cleanup = True
        self.triggers.append(Trigger(self, self.player, 'next_round_start', 'next_round'))
        trigger = Trigger(self, self.player, 'attack', 'end_of_round')
        trigger.duration_end = self.player.game.round + 1
        self.triggers.append(trigger)
        self.action.cleanup()
        self.desk.draw()        

    def do_trigger_start(self):
        from libs.events import create_event     
        if self.trigger.type == 'next_round_start':
            self.player.treasure = self.player.treasure + 1
            self.desk.changed.append('info')
            self.skip_cleanup = True
            self.desk.triggers.remove(self.trigger)
            self.triggers.remove(self.trigger)
            del self.trigger            
            self.desk.draw()
        elif self.trigger.type == 'attack':
            create_event(self.player.game.get_me(), 'send_reaction', { 'player' : self.player.name, 'defend' : 1, 'end' : 0 }, self.player.game.get_other_players_names())
            self.desk.add_message('Díky kartě Maják jsi se ubránil útoku')
            
    def do_trigger_end(self):
        pass