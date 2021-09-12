import pygame
from libs.classes.pile import Pile
from libs.events import create_event
import traceback
from libs.classes.card import Card
from libs.classes.action import Action

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd
from libs.library.Seaside import Seaside

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

        self.selectable_piles = []
        self.selected_piles = []
        self.selectable_info = [] 
        self.selected_info = []
        self.to_select = 0
        self.select_type = 'optional' # [ optional | mandatory ]
        self.select_action = 'select' # [ select | play ]

        self.action_button_label = ''

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
        if redraw == False or self.get_redraw('messages') == True:
            self.draw_messages()
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
            pile.draw_pile(self.SCREEN, self)
                
    def draw_kingdom(self):
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (0, 290 - 15, 1600, 290 + 15))
        for pile in self.kingdom_piles:
            pile.draw_pile(self.SCREEN, self)

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
            font = pygame.font.Font('freesansbold.ttf', 17)
            if self.player.name == self.game.get_current_player():
                text = font.render('Vyložené karty', True, (150, 150, 150))
            else:
                text = font.render('Vyložené karty - ' + self.game.get_current_player(), True, (150, 150, 150))                                
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
        font = pygame.font.Font('freesansbold.ttf', 17)
        label = self.select_area_label
        text = font.render(label, True, (255, 255, 255))
        self.SCREEN.blit(text, (2, 540))
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
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, 10, 720, 40))
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, 40, 320, 40))
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(self.player.name + '    ' + 'Kolo: ' + str(self.game.round) + '    ' + 'Fáze: ' + self.player.get_phase(), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 10))
        text = font.render('Peněz: ' + str(self.player.treasure), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 40))
        text = font.render('Akcí: ' + str(self.player.actions), True, (255, 255, 255))
        self.SCREEN.blit(text, (x + 120, 40))
        text = font.render('Nákupů: ' + str(self.player.buys), True, (255, 255, 255))
        self.SCREEN.blit(text, (x + 120 + 100, 40))
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
        y = 42
        w = 180
        h = 35
        if self.action_button_label != '':
            pygame.draw.rect(self.SCREEN, color, (x, y, w, h))
            font = pygame.font.Font('freesansbold.ttf', 15)
            text = font.render(self.action_button_label, True, (230, 230, 230))
            text_rect = text.get_rect(center = ( x + w/2, y + h/2))
            self.SCREEN.blit(text, text_rect)    
            pygame.display.update()     
        else:
            pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
            pygame.display.update()     

    def get_border_color(self, pile):
        if len(pile.cards) > 0 or pile.place == 'players_deck' or pile.place == 'players_discard' or pile.place == 'trash':
            if (pile in self.selectable_piles or pile in self.selected_piles) and self.to_select > 0 and (len(self.selected_piles) + len(self.selected_info)) < self.to_select:
                if pile in self.selected_piles:
                    return (150,150,150)
                elif self.select_action == 'select' and not (self.player.phase == 'buy' and pile.place == 'players_hand'):
                    return (0, 255, 0)                    
                else:
                    return (255, 0, 0)
        cards_with_triggers = self.get_cards_with_triggers()
        card = pile.top_card()
        if card is not None and card in cards_with_triggers:
            return (255, 255, 0)

        return (0, 0, 0)

    def redraw_borders_info(self):
        x = 1200 
        y = 40
        l = 95
        sections = ['treasure', 'actions', 'buys']
        for section in sections:
            if self.selectable_info is not None and self.to_select > 0:
                if section in self.selectable_info:
                    color = (0, 255, 0)
                elif section in self.selected_info:
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
        for pile in self.get_all_piles():
            pile.border_pile(self.SCREEN, self.get_border_color(pile), self)
        self.redraw_borders_info()

    def get_all_piles(self):
        piles =  self.basic_piles + self.kingdom_piles + [ self.trash ] + [ self.player.deck ] + self.player.hand + [ self.player.discard ]
        if self.select_area == False:
            piles = piles + self.play_area_piles
        else:
            piles = piles + self.select_area_piles
        return  piles

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

    def put_card_to_play_area(self, card, event = True, hidden = 0):
        for pile in self.play_area_piles:
            if card.name == pile.top_card().name and hidden == 0:
                pile.add_card(card, True, event, hidden_pile = hidden)
                return
        pile = Pile('play_area', len(self.play_area_piles), self.game)
        pile.add_card(card, True, event, hidden_pile = hidden)
        self.play_area_piles.append(pile)

    def coalesce_play_area(self):
        play_area_piles = []
        for pile in self.play_area_piles:
            if len(pile.cards) > 0:
                play_area_piles.append(pile)
            else:
                del pile
        self.play_area_piles = play_area_piles
        i = 0
        for pile in self.play_area_piles:
            pile.position = i
            i = i + 1

    def click_on_pile(self, x, y):
        if self.detail_displayed == False:
            pile = self.find_pile_by_coordinates(x, y)
            if pile is not None:
                self.player.activity.click_on_pile(pile)
                    
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

    def find_pile_by_coordinates(self, x, y):
        for pile in  self.get_all_piles():
            if pile.test_coordinates(x, y, self) == True:
                return pile
        return None

    def detect_hover(self, x, y):
        if x > 1700 and x < 1700 + 180 and y > 42 and y < 42 + 35:
            self.draw_action_button((70, 70, 70))
        else:
            self.draw_action_button()

    def action_button_click(self, x, y):
        if self.action_button_label != '' and x > 1700 and x < 1700 + 180 and y > 42 and y < 42 + 35:
            self.player.activity.click_on_action_button()

    def click_on_info(self, x, y):
        if x > 1200 and x < 1200 + 120 + 100 + 110 and y > 45 and y < 45 + 20:
            if x > 1200 and x < 1200 + 95:
                section = 'treasure'
            elif x > 1200 + 120 and x < 1200 + 120 + 80:
                section = 'actions'
            else:
                section = 'buys'
            self.player.activity.click_on_info(section)                
    
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

    def get_pile_triggers(self, pile):
        triggers = []
        for trigger in self.triggers:
            if trigger.pile == pile:
                triggers.append(trigger)
        return triggers

    def clear_triggers(self, duration):
        for trigger in self.triggers:
            if trigger.duration == duration:
                if trigger.duration == 'end_of_round' and trigger.duration_end == self.game.round:
                    self.triggers.remove(trigger)
                    del trigger

    def create_select(self, to_select, select_type, select_action = 'select', piles = [], info = []):
        self.selectable_piles = piles
        self.selected_piles = []
        self.selectable_info = info
        self.selected_info = []
        self.to_select = to_select
        if self.to_select > len(self.selectable_piles) + len(self.selectable_info):
            self.to_select = len(self.selectable_piles) + len(self.selectable_info)
        self.select_type = select_type
        self.select_action = select_action

    def clear_select(self):
        self.selectable_piles = []
        self.selected_piles = []
        self.selectable_info = [] 
        self.selected_info = []
        self.to_select = 0
        self.select_type = 'optional'
        self.select_action = 'select'
        self.action_button_label = ''
