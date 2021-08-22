from libs.api import call_api
from libs.classes.card import Card
from libs.classes.action import Action

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd

import json

def get_class(player, card_name):
    for expansion in player.game.expansions:
        cards = globals()[expansion].get_cards()
        if card_name in cards:
            return globals()[expansion].get_class(card_name)
    return None

def create_event(player, event_type, event, for_players):   
    data = call_api({ 'function' : 'create_event', 'id' : player.game.id, 'event' : json.dumps({ event_type : event }), 'for_players' : json.dumps(for_players) })

def get_events(player):
    data = call_api({ 'function' : 'get_events', 'id' : player.game.id, 'player' : player.name })
    for item in data:
        print(item)
        event = json.loads(item)
        for event_type in event:
            if event_type == 'joined':
                player.game.desk.add_message('Hráč ' + event[event_type] + ' se připojil ke hře')
            if event_type == 'start_turn':
                player.game.desk.add_message('Tah hráče ' + event[event_type] )
            if event_type == 'action':
                player.game.desk.add_message('Akční fáze hráče ' + event[event_type])
            if event_type == 'buy':
                player.game.desk.add_message('Fáze nákupu hráče ' + event[event_type])                                
            if event_type == 'bought_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' koupil kartu ' + event[event_type]['card_name'])    
            if event_type == 'played_action_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' zahrál akční kartu ' + event[event_type]['card_name'])  
            if event_type == 'gain_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' získal kartu ' + event[event_type]['card_name'])    
            if event_type == 'showed_card_from_deck':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' ukázal kartu ' + event[event_type]['card_name'] + ' ze svého dobíracího balíčku')  
            if event_type == 'showed_card_from_hand':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' ukázal kartu ' + event[event_type]['card_name'] + ' ze své ruky')                    
            if event_type == 'trash_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' zahodil kartu ' + event[event_type]['card_name'] + ' na smetiště')    
            if event_type == 'discard_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' odložil kartu ' + event[event_type]['card_name'] + ' na odkládací balíček')    
            if event_type == 'info_message':
                player.game.desk.add_message(event[event_type]['message'])    
            if event_type == 'message':
                player.game.desk.add_message(event[event_type]['player'] + ': ' + event[event_type]['message'])    


            if event_type == 'next_player':
                player.game.next_player()   

            if event_type == 'remove_card':
                if event[event_type]['place'] == 'basic':
                    player.game.desk.basic_piles[event[event_type]['position']].get_top_card(False)
                    player.game.desk.changed.append('basic')
                if event[event_type]['place'] == 'kingdom':
                    player.game.desk.kingdom_piles[event[event_type]['position']].get_top_card(False)
                    player.game.desk.changed.append('kingdom')
                if event[event_type]['place'] == 'trash':
                    player.game.desk.trash.get_top_card(False)
                    player.game.desk.changed.append('trash')
                if event[event_type]['place'] == 'play_area':    
                    for pile in player.game.desk.play_area_piles:
                        card = pile.top_card()
                        if card.id == event[event_type]['card_id']:
                            pile.get_top_card(False)
                        player.game.desk.coalesce_play_area()
                player.game.desk.changed.append('play_area')
                player.game.desk.draw()

            if event_type == 'add_card':
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass()                
                if event[event_type]['place'] == 'basic':
                    player.game.desk.basic_piles[event[event_type]['position']].add_card(card, event[event_type]['append'], False)
                    player.game.desk.changed.append('basic')
                if event[event_type]['place'] == 'kingdom':
                    player.game.desk.kingdom_piles[event[event_type]['position']].add_card(card, event[event_type]['append'], False)
                    player.game.desk.changed.append('kingdom')
                if event[event_type]['place'] == 'trash':
                    player.game.desk.trash.add_card(card, event[event_type]['append'], False)
                    player.game.desk.changed.append('trash')
                if event[event_type]['place'] == 'play_area':
                    player.game.desk.coalesce_play_area()
                    player.game.desk.put_card_to_play_area(card, False)
                    player.game.desk.changed.append('play_area')
                player.game.desk.draw()

            if event_type == 'do_draw_card':
                player.move_cards_from_deck_to_hand(1)
                player.game.desk.changed.append('players_deck')
                player.game.desk.changed.append('players_hand')
                player.game.desk.changed.append('players_discard')
                player.game.desk.draw()                

            if event_type == 'return_card_to_deck':
                if player.name == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' vrátil vaši kartu ' + event[event_type]['card_name'] + ' na dobírací balíček')    
                elif event[event_type]['attacking_player'] == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' vrátil kartu ' + event[event_type]['card_name'] + ' na svůj dobírací balíček')    
                else:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' vrátil kartu ' + event[event_type]['card_name'] + ' hráče ' + event[event_type]['player'] + ' na dobírací balíček')    
            
            if event_type == 'discard_card_from_deck':
                if player.name == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' dal vaši kartu ' + event[event_type]['card_name'] + ' na odkládací balíček')    
                    discarded = False
                    for card in player.deck.cards:
                        if card is not None and card.name == event[event_type]['card_name'] and discarded == False:
                            player.deck.cards.remove(card)
                            player.put_card_to_discard(card)  
                            discarded = True       
                    player.game.desk.changed.append('players_deck')
                    player.game.desk.changed.append('players_discard')
                    player.game.desk.draw()                
                elif event[event_type]['attacking_player'] == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' dal kartu ' + event[event_type]['card_name'] + ' na svůj odkládací balíček')    
                else:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' dal kartu ' + event[event_type]['card_name'] + ' hráče ' + event[event_type]['player'] + ' na odkládací balíček')    

            if event_type == 'check_reaction':
                player.phase = 'attacked_reaction'                
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                card.pile = None
                card.game = player.game
                card.desk = player.game.desk
                card.player = player                
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' zahrál kartu útoku ' + card.name)    
                player.action = Action(card, player)
                player.action.do_check_reaction()
                player.game.switch_player = True

            if event_type == 'attack_reaction':
                player.events.append({ 'event_type' : event_type, 'player' : event[event_type]['player'], 'card_name' : event[event_type]['card_name'], 'end' : event[event_type]['end'], 'defend' : event[event_type]['defend']})  

            if event_type == 'attack':
                player.phase = 'attacked'                
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                card.pile = None
                card.game = player.game
                card.desk = player.game.desk
                card.player = player                
                player.action = Action(card, player)
                player.action.do_attacked()
                player.game.switch_player = True

            if event_type == 'attack_respond':
                if 'cards' in event[event_type]:
                    player.events.append({ 'event_type' : event_type, 'player' : event[event_type]['player'], 'card_name' : event[event_type]['card_name'], 'cards' : event[event_type]['cards']})  
                else:
                    player.events.append({ 'event_type' : event_type, 'player' : event[event_type]['player'], 'card_name' : event[event_type]['card_name']})  

            if event_type == 'end_game': 
                player.phase = 'end_game'
                player.game.state = 'end'
                points = player.get_points()
                player.results.append({ 'player' : player.name, 'points' : points })
                create_event(player, 'results', { 'player_name' : player.name, 'points' : points }, player.game.get_other_players_names())
            if event_type == 'results':
                player.results.append({ 'player' : event[event_type]['player_name'], 'points' : int(event[event_type]['points'])})  

