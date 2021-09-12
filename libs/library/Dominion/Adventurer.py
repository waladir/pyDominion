from libs.classes.card import Card

class Adventurer(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'adventurer'
        self.name = 'Dobrodruh' 
        self.name_en = 'Adventurer'
        self.expansion = 'Dominion'
        self.image = 'Adventurer.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 6
        self.value = 0



    def do_action(self):
        from libs.events import create_event
        to_discard = []
        hand_count = len(self.player.hand)
        skip = False
        got = 0
        while skip == False and got < 2:
            cards = self.player.get_cards_from_deck(1)  
            if len(cards) > 0:
                for card in cards:
                    if card is None:
                        skip = True
                    else:
                        create_event(self.player.game.get_me(), 'draw_card', { 'player' : self.player.name, 'count' : 1 }, self.player.game.get_other_players_names())          
                        if 'treasure' in card.type:
                            self.player.put_card_to_hand(card)                                             
                            self.player.coalesce_hand()
                            got = got + 1
                        else:
                            to_discard.append(card)
            else:
                skip = True
        for card in to_discard:
            self.player.put_card_to_discard(card)
            create_event(self, 'discard_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
        self.action.cleanup()
        self.desk.changed.append('players_deck')
        self.desk.changed.append('players_hand')                
        self.desk.changed.append('players_discard')                
        self.desk.draw()
