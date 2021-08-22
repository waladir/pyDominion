import pygame
from libs.classes.pile import Pile
from libs.events import create_event
import time
import traceback
from libs.classes.card import Card
from libs.classes.action import Action

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd

class Desk():
    def __init__(self, SCREEN, cards_set, players_count, game, player):
        self.SCREEN = SCREEN
        self.cards_set = cards_set
        self.game = game
        self.game.desk = self
        self.player = player
        self.player.desk = self
        self.messages = []
        self.detail_displayed = False
        self.players_hand_offset = 0
        self.select_area_offset = 0        
        self.select_area = False
        self.select_area_label = ''
        self.select_area_hide_cards = False
        self.changed = []

        self.chat = ''

        self.create_basic(players_count)
        self.create_kingdom(cards_set, players_count)
        self.create_trash()
        self.play_area_piles = []
        self.select_area_piles = []

        self.triggers = []

    def get_class(self, card_name):
        for expansion in self.game.expansions:
            cards = globals()[expansion].get_cards()
            if card_name in cards:
                return globals()[expansion].get_class(card_name)
        return None

    def create_basic(self, players_count):
        self.basic_piles = []
        if players_count == 2:
            victory_cards_count = 8
            curse_cards_count = 10
        elif players_count == 3:
            victory_cards_count = 12
            curse_cards_count = 20
        else:
            victory_cards_count = 12
            curse_cards_count = 30

        basic_pile = Pile('basic', 0, self.game)
        basic_pile.create_pile('Copper', 60-players_count*7)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 1, self.game)
        basic_pile.create_pile('Silver', 40)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 2, self.game)
        basic_pile.create_pile('Gold', 30)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 3, self.game)
        basic_pile.create_pile('Estate', victory_cards_count)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 4, self.game)
        basic_pile.create_pile('Duchy', victory_cards_count)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 5, self.game)
        basic_pile.create_pile('Province', victory_cards_count)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 6, self.game)
        basic_pile.create_pile('Curse', curse_cards_count)
        self.basic_piles.append(basic_pile)

    def create_kingdom(self, cards_set, players_count):
        position = 0
        self.kingdom_piles = []
        sorted_cards = {}
        cards = {}
        for expansion in self.game.expansions:
            expansion_cards = globals()[expansion].get_cards(kingdom_card = True)
            cards = {**cards, **expansion_cards}    

        sorted_card_names = sorted(cards, key=lambda x: cards[x]['price'])
        for card_name in sorted_card_names:
            sorted_cards.update({ card_name :cards[card_name] })

        for card in sorted_cards:
            if card in cards_set:
                kingdom_pile = Pile('kingdom', position, self.game)
                kingdom_pile.create_pile(card, 10)
                self.kingdom_piles.append(kingdom_pile)            
                position = position + 1

    def create_trash(self):
        pile = Pile('trash', 0, self.game)
        self.trash = pile
        
    def get_redraw(self, place):
        if place in self.changed:
            self.changed.remove(place)
            return True
        else:
            return False

    def draw(self, redraw = True):
        # traceback.print_stack()
        if redraw == False:
            self.SCREEN.fill(pygame.Color(0, 0, 0))
        if redraw == False or self.get_redraw('basic') == True:
            self.draw_basic()
        if redraw == False or self.get_redraw('kingdom') == True:
            self.draw_kingdom()
        if redraw == False or self.get_redraw('trash') == True:
            self.draw_trash()
        if redraw == False or self.get_redraw('players_deck') == True:
            self.draw_players_deck()
        if redraw == False or self.get_redraw('players_hand') == True:
            self.draw_players_hand()
        if redraw == False or self.get_redraw('players_discard') == True:
            self.draw_players_discard()
        if redraw == False or self.get_redraw('play_area') == True or self.get_redraw('select_area') == True:
            self.draw_play_area()
        if redraw == False or self.get_redraw('info') == True:
            self.draw_info()
        if redraw == False or self.get_redraw('action_button') == True:
            self.draw_action_button()
        if self.get_redraw('results') == True:
            self.draw_results()        
        else:
            if self.detail_displayed == False:
                self.redraw_borders()
        pygame.display.update()          

    def draw_basic(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (0, 0 , 1190, 30 + 240 + 2))
        for pile in self.basic_piles:
            pile.draw_pile(self.SCREEN)
                
    def draw_kingdom(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (0, 290 - 15, 1600, 290 + 15))
        for pile in self.kingdom_piles:
            pile.draw_pile(self.SCREEN)

    def draw_trash(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (1762 - 2, 290 - 15, 290, 290 + 15))
        pile = self.trash
        pile.draw_pile(self.SCREEN)

    def draw_players_deck(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (0, 838 - 15, 2 + 2 + 150 + 2, 240 + 10 + 2 + 4))
        pile = self.player.deck
        pile.draw_pile(self.SCREEN)

    def draw_players_hand(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (2 + 300 - 2, 838 - 2, 1280 + 2, 240 + 4))
        self.player.coalesce_hand()
        self.players_hand_count = len(self.player.hand) - self.players_hand_offset
        if self.players_hand_count > 8:
           self.players_hand_count = 8 
        for i in range(self.players_hand_count):
            pile = self.player.hand[i + self.players_hand_offset] 
            pile.draw_pile(self.SCREEN, self)

    def draw_players_discard(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (1762 - 2, 838 - 15, 290, 240 + 10 + 20 + 4))
        pile = self.player.discard
        pile.draw_pile(self.SCREEN)

    def draw_play_area(self):
        if self.select_area == False:
            pygame.draw.rect(self.SCREEN, (0, 0, 0), (0, 570 - 2 - 10 - 20, 1920, 240 + 10 + 20 + 4 + 5 ))
            font = pygame.font.Font('freesansbold.ttf', 15)
            text = font.render('Vyložené karty', True, (150, 150, 150))
            self.SCREEN.blit(text, (2, 540))
            self.coalesce_play_area()
            self.play_area_count = len(self.play_area_piles)
            if self.play_area_count > 12:
                self.play_area_count = 12 
            for i in range(self.play_area_count):
                pile = self.play_area_piles[i] 
                pile.draw_pile(self.SCREEN, self)
            self.redraw_borders()
            pygame.display.update()
        else:
            self.draw_select_area()

    def draw_select_area(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (0, 570 - 2 - 10 - 20, 1920, 240 + 10 + 20 + 4 + 5 ))
        font = pygame.font.Font('freesansbold.ttf', 20)
        label = self.select_area_label
        text = font.render(label, True, (150, 150, 150))
        self.SCREEN.blit(text, (2, 545))
        self.coalesce_select_area()
        self.select_area_count = len(self.select_area_piles) - self.select_area_offset
        if self.select_area_count > 12:
            self.select_area_count = 12 
        for i in range(self.select_area_count):
            pile = self.select_area_piles[i + self.select_area_offset] 
            pile.draw_pile(self.SCREEN, self, not_show = self.select_area_hide_cards)
        self.redraw_borders()
        pygame.display.update()

    def draw_info(self):  
        x = 1200
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (1200, 10, 490, 60))
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(self.player.name + '    ' + 'Kolo: ' + str(self.game.round) + '    ' + 'Fáze: ' + self.player.get_phase(), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 10))
        text = font.render('Peněz: ' + str(self.player.treasure), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 45))
        text = font.render('Akcí: ' + str(self.player.actions), True, (255, 255, 255))
        self.SCREEN.blit(text, (x + 120, 45))
        text = font.render('Nákupů: ' + str(self.player.buys), True, (255, 255, 255))
        self.SCREEN.blit(text, (x + 120 + 100, 45))
        pygame.display.update()

    def draw_messages(self):
        x = 1200
        y = 80
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (1200, 80, 720, 160))
        font = pygame.font.Font('freesansbold.ttf', 17)
        for message in self.messages:
            text = font.render(message, True, (180, 180, 0))
            self.SCREEN.blit(text, (x, y))
            y = y + 20
        pygame.display.update()

    def draw_chat(self):
        x = 1200
        y = 240
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (1200, 240, 720, 30))
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(self.chat[-50:], True, (150, 150, 150))
        self.SCREEN.blit(text, (x, y))
        pygame.display.update()        

    def draw_results(self):
        y = 300
        self.SCREEN.fill(pygame.Color(0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 30)
        i = 0
        for result in self.player.results:
            text = font.render(result['player'] + ': ' + str(result['points']) + ' vítězných bodů', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (960, y + i) 
            i = i + 50
            self.SCREEN.blit(text, textRect) 
        pygame.display.update()        
        
    def draw_action_button(self, color = (100, 100, 100)):
        x = 1700
        y = 10
        w = 160
        h = 40
        if self.player == self.game.players[self.game.current_player]:
            if self.player.phase == 'buy' or self.player.phase == 'action':
                pygame.draw.rect(self.SCREEN, color, (x, y, w, h))
                font = pygame.font.Font('freesansbold.ttf', 15)
                if self.player.phase == 'buy':
                    text = font.render('Konec fáze nákupu', True, (230, 230, 230))
                    text_x = x + 10
                elif self.player.phase == 'action' or self.player.phase == 'attack':
                    if self.player.action is None:
                        text = font.render('Konec akční fáze', True, (230, 230, 230))
                        text_x = x + 20
                    else:
                        if self.player.action.phase == 'select':
                            if len(self.player.action.selectable_piles) > 0 and self.player.action.select_piles == 'mandatory':
                                pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
                                pygame.display.update()                 
                                return
                            elif len(self.player.action.selectable_cards) > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select and self.player.action.select_cards == 'mandatory':
                                pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
                                pygame.display.update()                 
                                return
                            else:
                                text = font.render('Ukončit výběr', True, (230, 230, 230))
                                text_x = x + 30
                        else:
                            text = font.render('Konec akční fáze', True, (230, 230, 230))
                            text_x = x + 20
                self.SCREEN.blit(text, (text_x, y+13))    
                pygame.display.update()                 
            else:
                pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
                pygame.display.update()     
        elif self.player.phase == 'attacked_reaction' or self.player.phase == 'attacked':
            pygame.draw.rect(self.SCREEN, color, (x, y, w, h))
            font = pygame.font.Font('freesansbold.ttf', 15)
            if len(self.player.action.selectable_piles) > 0 and self.player.action.select_piles == 'mandatory':
                pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
                pygame.display.update()                 
                return
            elif len(self.player.action.selectable_cards) > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select and self.player.action.select_cards == 'mandatory':
                pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
                pygame.display.update()                 
                return
            else:
                text = font.render('Ukončit výběr', True, (230, 230, 230))
                text_x = x + 30 
            self.SCREEN.blit(text, (text_x, y+13))    
            pygame.display.update()     
        else:
            pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
            pygame.display.update()   

    def get_border_color(self, pile):
        if pile.place == 'basic' or pile.place == 'kingdom':
            card = pile.top_card()
            if card is not None:
                if self.player.phase == 'buy':
                    if self.player.buys > 0 and self.player.treasure >= card.price:         
                        return (0, 255, 0)
                if self.player.phase == 'action' and self.player.action is not None:
                    if self.player.action is not None and self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:         
                        return (0, 255, 0)
                    if card in self.player.action.selected_cards:
                        return (150,150,150)

        if pile.place == 'trash':
            if self.player.phase == 'action' and self.player.action is not None:
                if self.player.action.selectable_piles is not None and pile in self.player.action.selectable_piles and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                    return (0, 255, 0)

        if pile.place == 'players_deck':
            if self.player.phase == 'action' and self.player.action is not None:
                if len(self.player.deck.cards) > 0:
                    if self.player.action.selectable_piles is not None and pile in self.player.action.selectable_piles and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                        return (0, 255, 0)
                    if pile in self.player.action.selected_piles:
                        return (150,150,150)

        if pile.place == 'players_hand':
            card = pile.top_card()
            if card is not None:
                if self.player.phase == 'buy' and 'treasure' in card.type:
                    return (255, 0, 0)
                if self.player.phase == 'action':
                    if 'action' in card.type and self.player.actions > 0 and self.player.action is None:                     
                        return (255, 0, 0)
                    if self.player.action is not None and self.player.action.phase == 'select':
                        if self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                            return (0, 255, 0)
                        if card in self.player.action.selected_cards:
                            return (150,150,150)
                if self.player.phase == 'attacked':
                    if self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                        return (0, 255, 0)
                    if card in self.player.action.selected_cards:
                        return (150,150,150)
                if self.player.phase == 'attacked_reaction':
                    if self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                        return (255, 0, 0)
                    if card in self.player.action.selected_cards:
                        return (150,150,150)

        if pile.place == 'select_area':
            card = pile.top_card()
            if card is not None:
                if self.player.phase == 'action' or self.player.phase == 'attacked_reaction' or self.player.phase == 'attack':
                    if 'action' in card.type and self.select_area_type == 'play_action' and self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select: 
                        return (255, 0, 0)
                    if 'action' in card.type and self.select_area_type == 'select_action' and self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select: 
                        return (0, 255, 0)                    
                    if self.select_area_type == 'select_action' and self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select: 
                        return (0, 255, 0)                    
                    if card in self.player.action.selected_cards:
                        return (150,150,150)

        if pile.place == 'play_area':
            card = pile.top_card()
            if card is not None:
                if card in self.get_cards_with_triggers():
                    return (255, 255, 0)
                if (self.player.phase == 'action' or self.player.phase == 'attacked_reaction') and self.player.action is not None:
                    if self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select: 
                        return (0, 255, 0)                    
                    if card in self.player.action.selected_cards:
                        return (150,150,150)                        

        if pile.place == 'players_discard':
            if self.player.phase == 'action' and self.player.action is not None:
                if self.player.action.selectable_piles is not None and pile in self.player.action.selectable_piles and self.player.action.to_select > 0 and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                    return (0, 255, 0)
        return (0, 0, 0)

    def redraw_borders_info(self):
        x = 1200 
        y = 45
        l = 95
        sections = ['treasure', 'actions', 'buys']
        for section in sections:
            if self.player.action is not None and self.player.action.selectable_info is not None and self.player.action.to_select > 0:
                if section in self.player.action.selectable_info:
                    color = (0, 255, 0)
                elif section in self.player.action.selected_info:
                    color = (150,150,150)
                else:
                    color = (0, 0, 0)
            else:
                color = (0, 0, 0)
            if section == 'actions':
                x = x + 120
                l = 80
            if section == 'buys':
                x = x + 100
                l = 110
            pygame.draw.rect(self.SCREEN, color, (x - 4 , y - 4 , l + 4 + 4, 2))
            pygame.draw.rect(self.SCREEN, color, (x + l + 4, y - 4, 2, 20 + 4 + 4))
            pygame.draw.rect(self.SCREEN, color, (x - 4 , y - 4 , 2, 20 + 4 + 4))
            pygame.draw.rect(self.SCREEN, color, (x - 4 , y + 20 + 2, l + 4 + 4, 2))
            pygame.display.update()                

    def redraw_borders(self):
        for pile in  self.get_all_piles():
            if (pile.place != 'play_area' and pile.place != 'select_area') or (pile.place == 'play_area' and self.select_area == False) or (pile.place == 'select_area' and self.select_area == True):
                pile.border_pile(self.SCREEN, self.get_border_color(pile), self)
        self.redraw_borders_info()

    def get_all_piles(self):
        return self.basic_piles + self.kingdom_piles + [ self.trash ] + [ self.player.deck ] + self.player.hand + [ self.player.discard ] + self.select_area_piles + self.play_area_piles

    def put_card_to_select_area(self, card):
        pile = Pile('select_area', len(self.select_area_piles), self.game)
        pile.add_card(card, True)
        self.select_area_piles.append(pile)

    def coalesce_select_area(self):
        for pile in self.select_area_piles:
            if len(pile.cards) == 0:
                self.select_area_piles.remove(pile)
                del pile
        i = 0
        for pile in self.select_area_piles:
            pile.position = i
            i = i + 1

    def put_card_to_play_area(self, card, event = True):
        self.coalesce_play_area()
        for pile in self.play_area_piles:
            if card.name == pile.top_card().name:
                pile.add_card(card, True, event)
                return
        pile = Pile('play_area', len(self.play_area_piles), self.game)
        pile.add_card(card, True, event)
        self.play_area_piles.append(pile)

    def coalesce_play_area(self):
        for pile in self.play_area_piles:
            if len(pile.cards) == 0:
                self.play_area_piles.remove(pile)
                del pile
        i = 0
        for pile in self.play_area_piles:
            pile.position = i
            i = i + 1

    def play_card_from_hand(self, pile):
        card = pile.top_card()
        triggers = self.get_triggers('card_played')
        if (self.player.phase == 'buy' and 'treasure' in card.type) or (self.player.phase == 'action' and 'action' in card.type and self.player.action is None):
            card = pile.get_top_card()
            self.player.coalesce_hand()
            for trigger in triggers:
                trigger.card_played = card
                trigger.run()
            self.put_card_to_play_area(card)
            if 'treasure' in card.type:
                self.player.treasure = self.player.treasure + card.value 
            if 'action' in card.type:
                self.player.actions = self.player.actions - 1
                self.player.action = Action(card, self.player)
                self.player.action.do_action()
            for trigger in triggers:
                trigger.card_played = card
                trigger.end_run()                
            self.changed.append('players_hand')
            self.changed.append('play_area')
            self.changed.append('info')
            self.draw()

    def click_on_card(self, x, y):
        if self.detail_displayed == False:
            pile = self.find_pile_by_coordinates(x, y)
            if pile is not None:
                if pile.place == 'basic' or pile.place == 'kingdom':                
                    card = pile.top_card()
                    if card is not None:
                        if self.player.phase == 'buy':
                            if self.player.buys > 0 and card.price <= self.player.treasure:
                                card = pile.get_top_card()
                                self.player.put_card_to_discard(card)
                                self.player.buys = self.player.buys - 1
                                self.player.treasure = self.player.treasure - card.price    
                                create_event(self, 'bought_card', { 'player' : self.player.name, 'card_name' : card.name }, self.game.get_other_players_names())
                                self.changed.append('basic')
                                self.changed.append('kingdom')
                                self.changed.append('play_area')
                                self.changed.append('players_discard')
                                self.changed.append('info')
                                self.draw()
                        if self.player.phase == 'action':
                            if self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:         
                                card = pile.top_card()
                                self.player.action.select_card(card, pile)
                                self.redraw_borders()
                elif pile.place == 'trash':
                    if self.player.action is not None and self.player.action.selectable_piles is not None and pile in self.player.action.selectable_piles: 
                        self.player.action.selectable_piles.remove(pile)        
                        self.player.action.selected_piles.append(pile)
                        if (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) == self.player.action.to_select:
                            self.player.action.to_select = -1
                            if self.player.phase == 'action':
                                self.player.action.do_action()
                elif pile.place == 'players_deck':
                    if self.player.action is not None and self.player.action.selectable_piles is not None and pile in self.player.action.selectable_piles: 
                        self.player.action.selectable_piles.remove(pile)        
                        self.player.action.selected_piles.append(pile)
                        if (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) == self.player.action.to_select:
                            self.player.action.to_select = -1
                            if self.player.phase == 'action':
                                self.player.action.do_action()
                        self.redraw_borders()
                elif pile.place == 'players_hand':
                    card = pile.top_card()
                    if card is not None:
                        if self.player.phase == 'buy' and 'treasure' in card.type and self.player.action is None:
                            self.play_card_from_hand(pile)
                        if self.player.phase == 'action':
                            if 'action' in card.type and self.player.actions > 0 and self.player.action is None:
                                self.play_card_from_hand(pile)
                            if self.player.action is not None and self.player.action.phase == 'select':
                                if self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select and card != self.player.action.card: 
                                    self.player.action.select_card(card, pile)
                                    self.redraw_borders()
                        if self.player.phase == 'attacked_reaction' or self.player.phase == 'attacked':
                            if self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select: 
                                self.player.action.select_card(card, pile)
                                self.redraw_borders()
                elif pile.place == 'players_discard':
                    if self.player.action is not None and self.player.action.selectable_piles is not None and pile in self.player.action.selectable_piles: 
                        self.player.action.selectable_piles.remove(pile)        
                        self.player.action.selected_piles.append(pile)
                        if (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) == self.player.action.to_select:
                            self.player.action.to_select = -1
                            if self.player.phase == 'action':
                                self.player.action.do_action()

                elif pile.place == 'play_area':
                    card = pile.top_card()
                    if card is not None:
                        if (self.player.phase == 'action' or self.player.phase == 'attacked_reaction') and self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                            self.player.action.select_card(card, pile)
                            self.redraw_borders()

                elif pile.place == 'select_area':
                    card = pile.top_card()
                    if card is not None:
                        if (self.player.phase == 'action' or self.player.phase == 'attacked_reaction' or self.player.phase == 'attack') and self.player.action.selectable_cards is not None and card in self.player.action.selectable_cards and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select:
                            self.player.action.select_card(card, pile)
                            self.redraw_borders()                         
    
    def find_pile_by_coordinates(self, x, y):
        for pile in  self.get_all_piles():
            if pile.test_coordinates(x, y, self) == True:
                return pile
        return None

    def detect_hover(self, x, y):
        if x > 1700 and x < 1700+150 and y > 10 and y < 10+40:
            self.draw_action_button((130, 130, 130))
        else:
            self.draw_action_button()

    def show_card_detail(self, x, y):
        if self.detail_displayed == False:
            pile = self.find_pile_by_coordinates(x, y)
            if pile is not None and pile.place != 'players_deck':
                card = pile.top_card()
                if card is not None:   
                    card.draw_card_detail(self.SCREEN)
                    pygame.display.update()
                    self.detail_displayed = True
        else:
            self.detail_displayed = False
            self.draw(False)

    def action_button_click(self, x, y):
        if x > 1700 and x < 1700+150 and y > 10 and y < 10+40:
            if self.player.phase == 'buy':
                self.player.phase = 'cleanup'
                self.player.cleanup_phase()
            if self.player.phase == 'action' or self.player.phase == 'select':
                if self.player.action is None:
                    self.player.phase = 'buy'
                    create_event(self.player, 'buy', self.player.name, self.game.get_other_players_names())
                    self.add_message('Začátek fáze nákupu')
                else:
                    self.player.action.to_select = -1
                    self.player.action.do_action()
            if self.player.phase == 'attacked':
                if (len(self.player.action.selectable_piles) == 0 and len(self.player.action.selectable_cards) == 0) or self.player.action.select_piles != 'mandatory':
                    self.player.action.do_attack()
            if self.player.phase == 'attacked_reaction':
                if (len(self.player.action.selectable_piles) == 0 and len(self.player.action.selectable_cards) == 0) or self.player.action.select_piles != 'mandatory':
                    action = self.player.action
                    for card in self.player.action.selected_cards:
                        self.player.action = Action(card, self.player)
                        self.player.action.attack_card = action.attack_card
                        self.player.action.do_reaction()
                    self.player.action = action
                    if len(self.player.action.selected_cards) > 0:
                        create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.player.action.attack_card.name_en, 'end' : 1, 'defend' : 0 }, self.player.game.get_other_players_names())
                if self.player.phase != 'wait' and len(self.player.action.selected_cards) == 0:
                    self.player.phase = 'wait'
                    self.player.game.switch_player = True
                    create_event(self.player.game.get_me(), 'attack_reaction', { 'player' : self.player.name, 'card_name' : self.player.action.attack_card.name_en, 'end' : 1, 'defend' : 0 }, self.player.game.get_other_players_names())
            self.changed.append('info')
            self.changed.append('action_button')
            self.draw()

    def click_on_info(self, x, y):
        if x > 1200 and x < 1200 + 120 + 100 + 110 and y > 45 and y < 45 + 20:
            if x > 1200 and x < 1200 + 95:
                section = 'treasure'
            elif x > 1200 + 120 and x < 1200 + 120 + 80:
                section = 'actions'
            else:
                section = 'buys'
            if self.player.action is not None and self.player.action.phase == 'select':
                if self.player.action.selectable_info is not None and section in self.player.action.selectable_info and (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) < self.player.action.to_select: 
                    self.player.action.selectable_info.remove(section)
                    self.player.action.selected_info.append(section)   
                    if (len(self.player.action.selected_cards) + len(self.player.action.selected_piles) + len(self.player.action.selected_info)) == self.player.action.to_select:
                        self.player.action.to_select = -1
                        if self.player.phase == 'action':
                            self.player.action.do_action()
            self.draw()            
    
    def add_message(self, message):
        self.messages.insert(0, message)
        if len(self.messages) > 8:
            self.messages.pop()
        self.draw_messages()

    def get_triggers(self, type):
        triggers = []
        for trigger in self.triggers:
            if trigger.type == type:
                triggers.append(trigger)
        return triggers

    def get_cards_with_triggers(self):
        cards = []
        for trigger in self.triggers:
                cards.append(trigger.card)
        return cards

    def clear_triggers(self, duration):
        for trigger in self.triggers:
            if trigger.duration == duration:
                if trigger.duration == 'end_of_round' and trigger.duration_end == self.game.round:
                    self.triggers.remove(trigger)
                    del trigger

