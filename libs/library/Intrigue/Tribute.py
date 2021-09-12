import json
from libs.classes.card import Card

class Tribute(Card):
    def __init__(self):
        Card.__init__(self)        
        self.id = 'tribute'
        self.name = 'Dar poddaných' 
        self.name_en = 'Tribute'
        self.expansion = 'Intrigue'
        self.image = 'Tribute.png'
        self.kingdom_card = True
        self.type = ['action']
        self.subtype = None
        self.price = 5
        self.value = 0

        self.phase = 'action'

    def do_action(self):
        if self.phase == 'action':
            if self.player.game.current_player + 1 > len(self.player.game.players) - 1:
                player_name = self.player.game.players[0].name
            else:
                player_name = self.player.game.players[self.player.game.current_player + 1].name
            self.action.to_attack.append(player_name)
            self.phase = 'get_bonus'
            self.action.do_attack()
        elif self.phase == 'get_bonus':
            cards = []
            for data in self.action.data:
                for card_name in data['card_names']:
                    cardClass = self.player.deck.get_class(card_name)
                    card = cardClass() 
                    if card.name not in cards:
                        cards.append(card.name)
                        if 'action' in card.type:
                            self.player.actions = self.player.actions + 2
                        if 'treasure' in card.type:
                            self.player.treasure = self.player.treasure + 2
                        if 'victory' in card.type:
                            self.player.move_cards_from_deck_to_hand(3)
                    del card
            self.desk.changed.append('info')
            self.desk.changed.append('players_deck')
            self.desk.changed.append('players_hand')
            self.desk.draw()
            self.action.cleanup()        
            self.desk.draw()

    def do_attacked(self):
        from libs.events import create_event
        if self.phase == 'action':
            card_names = []
            cards = self.player.get_cards_from_deck(2)
            for card in cards:
                if card is not None:
                    self.desk.add_message('Ukázal jsi kartu ' + card.name + 'z dobíracího balíčku') 
                    create_event(self.player.game.get_me(), 'showed_card_from_deck', { 'player' : self.player.name, 'card_name' : card.name }, self.player.game.get_other_players_names())
                    card_names.append(card.name_en)
        create_event(self.player.game.get_me(), 'attack_respond', { 'player' : self.player.name, 'data' : json.dumps({ 'card_names' : card_names}) }, self.player.game.get_other_players_names())
        self.action.cleanup()
