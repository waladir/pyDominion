from libs.api import call_api
import debug
from libs.classes.card import Card
from libs.classes.action import Action
from libs.classes.trigger import Trigger

import json

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd
from libs.library.Seaside import Seaside

def get_class(player, card_name):
    for expansion in player.game.expansions:
        cards = globals()[expansion].get_cards()
        if card_name in cards:
            return globals()[expansion].get_class(card_name)
    return None

def create_event(player, event_type, event, for_players):   
    if debug.events == True:
        print(json.dumps({ event_type : event }))
        print(for_players)
    data = call_api({ 'function' : 'create_event', 'id' : player.game.id, 'event' : json.dumps({ event_type : event }), 'for_players' : json.dumps(for_players) })

def get_events(player):
    data = call_api({ 'function' : 'get_events', 'id' : player.game.id, 'player' : player.name })
    for item in data:
        if debug.events == True:
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
            if event_type == 'played_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' vyložil kartu ' + event[event_type]['card_name'])  
            if event_type == 'gain_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' získal kartu ' + event[event_type]['card_name'])    
            if event_type == 'gain_card_to_deck':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' získal kartu ' + event[event_type]['card_name'] + ' a odložil ji nasvůj dobírací balíček')    
            if event_type == 'move_card_from_discard_to_deck':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' přesunul kartu ' + event[event_type]['card_name'] + ' z odkládacího na dobírací balíček')    
            if event_type == 'move_card_from_hand_to_deck':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' dal kartu z ruky na dobírací balíček')    
            if event_type == 'showed_card_from_deck':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' ukázal kartu ' + event[event_type]['card_name'] + ' ze svého dobíracího balíčku')  
            if event_type == 'showed_card_from_hand':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' ukázal kartu ' + event[event_type]['card_name'] + ' ze své ruky')                    
            if event_type == 'draw_card':
                karty = ''
                count = int(event[event_type]['count'])
                if count == 1:
                    karty = 'kartu'
                elif count > 1 and  count < 5:
                    karty = 'karty'
                else:
                    karty = 'karet'
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' si  líznul ' + str(count) + ' ' + karty + ' z dobíracího balíčku')    
            if event_type == 'trash_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' zahodil kartu ' + event[event_type]['card_name'] + ' na smetiště')    
            if event_type == 'discard_card':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' odložil kartu ' + event[event_type]['card_name'] + ' na odkládací balíček')    
            if event_type == 'return_hidden_card_to_hand':
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' vrátil vyloženou kartu zpět do ruky')    


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
                    player.game.desk.basic_piles[event[event_type]['position']].add_card(card, event[event_type]['append'], False, int(event[event_type]['hidden_pile']))
                    player.game.desk.changed.append('basic')
                if event[event_type]['place'] == 'kingdom':
                    player.game.desk.kingdom_piles[event[event_type]['position']].add_card(card, event[event_type]['append'], False, int(event[event_type]['hidden_pile']))
                    player.game.desk.changed.append('kingdom')
                if event[event_type]['place'] == 'trash':
                    player.game.desk.trash.add_card(card, event[event_type]['append'], False, int(event[event_type]['hidden_pile']))
                    player.game.desk.changed.append('trash')
                if event[event_type]['place'] == 'play_area':
                    player.game.desk.coalesce_play_area()
                    player.game.desk.put_card_to_play_area(card, False, int(event[event_type]['hidden_pile']))
                    player.game.desk.changed.append('play_area')
                player.game.desk.draw()

            if event_type == 'do_draw_card':
                player.move_cards_from_deck_to_hand(1)
                player.game.desk.changed.append('players_deck')
                player.game.desk.changed.append('players_hand')
                player.game.desk.changed.append('players_discard')
                player.game.desk.draw()                

            if event_type == 'return_card_to_deck':
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                if player.name == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' vrátil vaši kartu ' + card.name  + ' na dobírací balíček')  
                    player.deck.add_card(card)
                    player.game.desk.changed.append('player_deck')
                    player.game.desk.draw()                
                elif event[event_type]['attacking_player'] == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' vrátil kartu ' + card.name  + ' na svůj dobírací balíček')    
                else:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' vrátil kartu ' + card.name  + ' hráče ' + event[event_type]['player'] + ' na dobírací balíček')    
            
            if event_type == 'discard_card_from_deck':
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                if player.name == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' dal vaši kartu ' + card.name  + ' na odkládací balíček')    
                    player.discard.add_card(card)
                    player.game.desk.changed.append('players_discard')
                    player.game.desk.draw()                
                elif event[event_type]['attacking_player'] == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' dal kartu ' + card.name  + ' na svůj odkládací balíček')    
                else:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' dal kartu ' + card.name  + ' hráče ' + event[event_type]['player'] + ' na odkládací balíček')    

            if event_type == 'trash_card_from_deck':
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                if player.name == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' zahodil vaši kartu ' + card.name + ' na smetiště')    
                    player.game.desk.trash.add_card(card)
                    player.game.desk.changed.append('trash')
                    player.game.desk.draw()                
                elif event[event_type]['attacking_player'] == event[event_type]['player']:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' zahodil kartu ' + card.name + ' na smetiště')    
                else:
                    player.game.desk.add_message('Hráč ' + event[event_type]['attacking_player'] + ' zahodil kartu ' + card.name + ' hráče ' + event[event_type]['player'] + ' na smetiště')    

            if event_type == 'get_card_from_supply':
                if player.name == event[event_type]['player']:
                    for pile in player.game.desk.basic_piles + player.game.desk.kingdom_piles:
                        card = pile.top_card()
                        if card is not None and card.name == event[event_type]['card_name']:
                            card = pile.get_top_card()
                            player.put_card_to_discard(card)
                            player.game.desk.add_message('Při útoku hráče ' + event[event_type]['player'] + ' jsi získal kartu ' + card.name) 
                            create_event(player, 'gain_card', { 'player' : player.name, 'card_name' : card.name }, player.game.get_other_players_names())

            if event_type == 'pass_card':
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' ti předal kartu ' + card.name)
                player.put_card_to_hand(card)
                player.game.desk.changed.append('players_hand')
                player.game.desk.draw()

            if event_type == 'put_trigger_on_pile':
                selected_pile = None
                selected_pile_card = None
                played_card = None
                for pile in player.desk.get_all_piles():
                    if pile.place == event[event_type]['pile_place'] and pile.position == event[event_type]['pile_position']:
                        selected_pile = pile
                        cardClass = get_class(player, selected_pile.card_name)
                        selected_pile_card = cardClass() 
                for pile in player.game.desk.play_area_piles:
                    card = pile.top_card()
                    if card is not None and card.name_en == event[event_type]['card_name']:
                        played_card = card
                played_card.trigger = Trigger(played_card, player, event[event_type]['type'], event[event_type]['duration'], pile = selected_pile)
                played_card.trigger.description = event[event_type]['description']
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' umístil token '  + played_card.name + ' na balíček karet ' + selected_pile_card.name)
                player.game.desk.changed.append(selected_pile.place)
                player.game.desk.changed.append('basic')
                player.game.desk.draw()
                player.game.desk.redraw_borders()

            if event_type == 'request_reaction':
                player.phase = 'attacked_reaction'                
                player.game.desk.changed.append('info')
                player.game.desk.draw()
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                card.pile = None
                card.game = player.game
                card.desk = player.game.desk
                card.player = player                
                player.game.desk.add_message('Hráč ' + event[event_type]['player'] + ' zaútočil kartou ' + card.name)                
                action = Action(card, player)
                action.do_check_reaction()

            if event_type == 'send_reaction':
                if player.phase == 'attack_wait_for_reaction':
                    action = player.actions_to_play[0]
                    action.get_reaction(event[event_type]['player'], int(event[event_type]['defend']), int(event[event_type]['end']))

            if event_type == 'attack':
                player.phase = 'attacked'                
                player.game.desk.changed.append('info')
                player.game.desk.draw()
                cardClass = get_class(player, event[event_type]['card_name'])
                card = cardClass() 
                card.pile = None
                card.game = player.game
                card.desk = player.game.desk
                card.player = player                
                action = Action(card, player)
                player.actions_to_play.append(action)
                if len(player.actions_to_play) == 1:
                    action.do_attacked()                

            if event_type == 'attack_respond':
                if player.phase == 'attack_wait_for_respond':
                    action = player.actions_to_play[0]
                    action.get_attack_respond(event[event_type]['player'], json.loads(event[event_type]['data']))

            if event_type == 'end_game': 
                player.phase = 'end_game'
                player.game.state = 'end'
                points = player.get_points()
                player.results.append({ 'player' : player.name, 'points' : points })
                create_event(player, 'results', { 'player_name' : player.name, 'points' : points }, player.game.get_other_players_names())
            if event_type == 'results':
                player.results.append({ 'player' : event[event_type]['player_name'], 'points' : int(event[event_type]['points'])})  

