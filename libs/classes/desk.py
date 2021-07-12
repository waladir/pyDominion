        # 'basic'
        # 'kingdom'
        # 'trash'
        # 'players_deck'
        # 'players_discard'
        # 'players_hand'

import pygame
from libs.classes.pile import Pile
import time


class Desk():
    def __init__(self, SCREEN, cards_set, players_count, player):
        self.SCREEN = SCREEN
        self.player = player
        self.set_limits()
        self.selected = None
        self.create_basic(players_count)
        self.create_kingdom(cards_set, players_count)
        self.draw()
        self.detail_displayed = False

    def set_limits(self):
        self.basic_y = 30
        self.kingdom_y = 320
        self.image_x = 150
        self.image_y = 240
        self.margin_x = 10

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

        basic_pile = Pile('basic', 0)
        basic_pile.create_pile('Měďák', 60-players_count*7)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 1)
        basic_pile.create_pile('Stříbrňák', 40)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 2)
        basic_pile.create_pile('Zlaťák', 30)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 3)
        basic_pile.create_pile('Statek', victory_cards_count)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 4)
        basic_pile.create_pile('Vévodství', victory_cards_count)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 5)
        basic_pile.create_pile('Provincie', victory_cards_count)
        self.basic_piles.append(basic_pile)
        basic_pile = Pile('basic', 6)
        basic_pile.create_pile('Kletba', curse_cards_count)
        self.basic_piles.append(basic_pile)

    def create_kingdom(self, cards_set, players_count):
        position = 0
        self.kingdom_piles = []
        for card in cards_set:
            kingdom_pile = Pile('kingdom', position)
            kingdom_pile.create_pile(card, 10)
            self.kingdom_piles.append(kingdom_pile)            
            position = position + 1

    def draw(self):
        self.SCREEN.fill(pygame.Color(0, 0, 0))
        self.draw_basic()
        self.draw_kingdom()
        self.draw_player_deck()
        self.draw_player_hand()
        pygame.display.update()          

    def draw_basic(self):
        y = self.basic_y
        for pile in self.basic_piles:
            card = pile.top_card()
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(str(len(pile.cards)), True, (0, 102, 0))
            textRect = text.get_rect()
            textRect.center = (pile.position*160+75, y-10)   
            card.draw_card(self.SCREEN, (2+pile.position*(self.image_x+self.margin_x), y), False)  
            self.SCREEN.blit(text, textRect)
            if self.player.phase == 'buy' and self.player.buys > 0 and self.player.treasure >= card.price:         
                self.border_pile((0, 102, 0), 'basic', pile.position)
                
    def draw_kingdom(self):
        y = self.kingdom_y
        for pile in self.kingdom_piles:
            card = pile.top_card()
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(str(len(pile.cards)), True, (0, 102, 0))
            textRect = text.get_rect()
            textRect.center = (pile.position*160+75, y-10)            
            card.draw_card(self.SCREEN, (2+pile.position*(self.image_x+self.margin_x), y), False)  
            self.SCREEN.blit(text, textRect)
            if self.player.phase == 'buy' and self.player.buys > 0 and self.player.treasure >= card.price:         
                self.border_pile((0, 102, 0), 'kingdom', pile.position)

    def draw_player_deck(self):
            pile = self.player.deck
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(str(len(pile.cards)), True, (0, 102, 0))
            textRect = text.get_rect()
            textRect.center = (75, 840-10)     
            card = pile.top_card()       
            card.draw_card(self.SCREEN, (2, 850), True)  
            self.SCREEN.blit(text, textRect)

    def draw_player_hand(self):
            hand = self.player.hand
            for i in range(len(hand.cards)):
                card = hand.cards[i]
                if i < 9:
                    card.draw_card(self.SCREEN, (2+300 + i*(self.image_x+self.margin_x), 600), False)  
                else:
                    card.draw_card(self.SCREEN, (2+300 + (i-8)*(self.image_x+self.margin_x), 850), False)  
                if self.player.phase == 'buy' and self.player.buys > 0 and card.card_type == 'treasure':         
                    self.border_pile((255, 0, 0), 'players_hand', i)

    def border_pile(self, color, type, position):
        if type == 'kingdom':
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)-2, self.kingdom_y-2, self.image_x+2, 2))
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)+self.image_x, self.kingdom_y-2, 2, self.image_y+2))
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)-2, self.kingdom_y-2, 2, self.image_y+2))
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)-2, self.kingdom_y+self.image_y, self.image_x+4, 2))
        if type == 'basic':
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)-2, self.basic_y-2, self.image_x+2, 2))
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)+self.image_x, self.basic_y-2, 2, self.image_y+2))
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)-2, self.basic_y-2, 2, self.image_y+2))
            pygame.draw.rect(self.SCREEN, color, (2+position*(self.image_x+self.margin_x)-2, self.basic_y+self.image_y, self.image_x+4, 2))
        if type == 'players_hand':
            if position < 8:
                pygame.draw.rect(self.SCREEN, color, (2+300+position*(self.image_x+self.margin_x)-2, 600-2, self.image_x+2, 2))
                pygame.draw.rect(self.SCREEN, color, (2+300+position*(self.image_x+self.margin_x)+self.image_x, 600-2, 2, self.image_y+2))
                pygame.draw.rect(self.SCREEN, color, (2+300+position*(self.image_x+self.margin_x)-2, 600-2, 2, self.image_y+2))
                pygame.draw.rect(self.SCREEN, color, (2+300+position*(self.image_x+self.margin_x)-2, 600+self.image_y, self.image_x+4, 2))
            else:
                pygame.draw.rect(self.SCREEN, color, (2+300+(position-8)*(self.image_x+self.margin_x)-2, 850-2, self.image_x+2, 2))
                pygame.draw.rect(self.SCREEN, color, (2+300+(position-8)*(self.image_x+self.margin_x)+self.image_x, 850-2, 2, self.image_y+2))
                pygame.draw.rect(self.SCREEN, color, (2+300+(position-8)*(self.image_x+self.margin_x)-2, 850-2, 2, self.image_y+2))
                pygame.draw.rect(self.SCREEN, color, (2+300+(position-8)*(self.image_x+self.margin_x)-2, 850+self.image_y, self.image_x+4, 2))
        pygame.display.update()

    def get_border_color(self, type, position):
        if type == 'basic':
            pile = self.basic_piles[position]
            card = pile.top_card()
            if self.player.phase == 'buy' and self.player.buys > 0 and self.player.treasure >= card.price:         
                return (0, 102, 0)
        if type == 'kingdom':
            pile = self.kingdom_piles[position]
            card = pile.top_card()
            if self.player.phase == 'buy' and self.player.buys > 0 and self.player.treasure >= card.price:         
                return (0, 102, 0)
        if type == 'players_hand':
            card = self.player.hand.cards[position]
            if self.player.phase == 'buy' and self.player.buys > 0 and card.card_type == 'treasure':                     
                if card in self.player.activated_cards:
                    return (255, 255, 0)                    
                else:
                    return (255, 0, 0)
        return (0, 0, 0)
                
    def search_pile_coordinates(self, x, y):
        if y > self.kingdom_y and y < self.kingdom_y+self.image_y:
            if x < 9*(self.image_x+self.margin_x)+self.image_x:
                pile_position = int(x/(self.image_x+self.margin_x))
                if pile_position <= len(self.kingdom_piles):
                    return { 'kingdom' : pile_position}
        if y > self.basic_y and y < self.basic_y+self.image_y:
            if x < 6*(self.image_x+self.margin_x)+self.image_x:
                pile_position = int(x/(self.image_x+self.margin_x))
                if pile_position <= len(self.basic_piles):
                    return { 'basic' : pile_position}
        if y > 600 and x > 300:
            if x < 300+7*(self.image_x+self.margin_x)+self.image_x:
                pile_position = int((x-300)/(self.image_x+self.margin_x))
                if y > 850:
                    pile_position = pile_position + 8
                if pile_position <= len(self.player.hand.cards)-1:
                    return { 'players_hand' : pile_position}
        return None

    def detect_hover(self, x, y):
        if self.detail_displayed == False:
            if self.search_pile_coordinates(x, y) is not None:
                pile = self.search_pile_coordinates(x, y)
                for pile_type in pile:
                    if self.selected == None:
                        self.border_pile((0, 0, 255), pile_type, pile[pile_type])
                        self.selected = { pile_type : pile[pile_type] }
                    elif self.selected != { pile_type : pile[pile_type] }:
                            for selected in self.selected:
                                self.border_pile(self.get_border_color(selected, self.selected[selected]), selected, self.selected[selected])
                            self.border_pile((0, 0, 255), pile_type, pile[pile_type])
                            self.selected = { pile_type : pile[pile_type] }

    def show_card_detail(self, x, y):
        if self.detail_displayed == False:
            if self.search_pile_coordinates(x, y) is not None:
                pile = self.search_pile_coordinates(x, y)
                for pile_type in pile:
                    if pile_type == 'basic':
                        pile = self.basic_piles[pile[pile_type]]
                        card = pile.top_card()
                    elif pile_type == 'kingdom':
                        pile = self.kingdom_piles[pile[pile_type]]
                        card = pile.top_card()
                    elif pile_type == 'players_hand':
                        card = self.player.hand.cards[pile[pile_type]]
                    card.draw_card_detail(self.SCREEN)
                    pygame.display.update()
                    self.detail_displayed = True
        else:
            if x > 773 and x < 773 + 374 and y > 0 and y < 600:
                self.detail_displayed = False
                self.draw()

    def activate_card(self, x, y):
        if self.detail_displayed == False:
            if self.search_pile_coordinates(x, y) is not None:
                pile = self.search_pile_coordinates(x, y)
                for pile_type in pile:
                    if pile_type == 'basic':
                        pile = self.basic_piles[pile[pile_type]]
                        card = pile.top_card()
                    elif pile_type == 'kingdom':
                        pile = self.kingdom_piles[pile[pile_type]]
                        card = pile.top_card()
                    
                    elif pile_type == 'players_hand':
                        card = self.player.hand.cards[pile[pile_type]]
                        if self.player.phase == 'buy' and self.player.buys > 0 and card.card_type == 'treasure':
                            if card not in self.player.activated_cards:
                                self.player.activated_cards.append(card)
                                self.border_pile((255, 255, 0), pile_type, pile[pile_type])
                                self.player.treasure = self.player.treasure + card.value                     
                            else:
                                self.player.activated_cards.remove(card)
                                self.border_pile((255, 0, 0), pile_type, pile[pile_type])                        
                                self.player.treasure = self.player.treasure - card.value                     
                            print(self.player.treasure)
                        


               