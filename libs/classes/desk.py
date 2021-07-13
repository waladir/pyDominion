import pygame
from libs.classes.pile import Pile
import time


class Desk():
    def __init__(self, SCREEN, cards_set, players_count, game, player):
        self.SCREEN = SCREEN
        self.game = game
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
        self.draw_players_deck()
        self.draw_players_hand()
        self.draw_players_discard()
        self.draw_info()
        self.draw_action_button()
        self.redraw_borders()
        pygame.display.update()          

    def draw_basic(self):
        y = self.basic_y
        for pile in self.basic_piles:
            card = pile.top_card()
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(str(len(pile.cards)), True, (0, 102, 0))
            textRect = text.get_rect()
            textRect.center = (pile.position*160+75, y-10)  
            if card is not None:   
                card.draw_card(self.SCREEN, (2+pile.position*(self.image_x+self.margin_x), y), False)  
            self.SCREEN.blit(text, textRect)
                
    def draw_kingdom(self):
        y = self.kingdom_y
        for pile in self.kingdom_piles:
            card = pile.top_card()
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(str(len(pile.cards)), True, (0, 102, 0))
            textRect = text.get_rect()
            textRect.center = (pile.position*160+75, y-10)    
            if card is not None:   
                card.draw_card(self.SCREEN, (2+pile.position*(self.image_x+self.margin_x), y), False)  
            self.SCREEN.blit(text, textRect)

    def draw_players_deck(self):
        pile = self.player.deck
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(str(len(pile.cards)), True, (0, 102, 0))
        textRect = text.get_rect()
        textRect.center = (75, 840-10)     
        card = pile.top_card()      
        if card is not None:   
            card.draw_card(self.SCREEN, (2, 850), True)  
        self.SCREEN.blit(text, textRect)

    def draw_players_hand(self):
        hand = self.player.hand
        for i in range(len(hand.cards)):
            card = hand.cards[i]
            if card is not None:   
                if i < 9:
                    card.draw_card(self.SCREEN, (2+300 + i*(self.image_x+self.margin_x), 600), False)  
                else:
                    card.draw_card(self.SCREEN, (2+300 + (i-8)*(self.image_x+self.margin_x), 850), False)  

    def draw_players_discard(self):
        pile = self.player.discard
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(str(len(pile.cards)), True, (0, 102, 0))
        textRect = text.get_rect()
        textRect.center = (1845, 840-10)     
        card = pile.top_card()    
        if card is not None:   
            card.draw_card(self.SCREEN, (1768, 850), False)  
        self.SCREEN.blit(text, textRect)                

    def draw_info(self):  
        x = 1200
        pygame.draw.rect(self.SCREEN, (0, 0, 0), (1200, 10, 400, 270))
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(self.player.name, True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 10))
        text = font.render('Kolo: ' + str(self.game.round), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 45))
        text = font.render('Peněz: ' + str(self.player.treasure), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 70))
        text = font.render('Akcí: ' + str(self.player.actions), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 95))
        text = font.render('Nákupů: ' + str(self.player.buys), True, (255, 255, 255))
        self.SCREEN.blit(text, (x, 120)) 
        pygame.display.update()       

    def draw_action_button(self, color = (100, 100, 100)):
        x = 1700
        y = 10
        w = 150
        h = 40
        if self.player == self.game.players[self.game.current_player]:
            if self.player.phase == 'buy':
                pygame.draw.rect(self.SCREEN, color, (x, y, w, h))
                font = pygame.font.Font('freesansbold.ttf', 15)
                text = font.render('Ukončit nákup', True, (230, 230, 230))
                self.SCREEN.blit(text, (x+28, y+13))    
                pygame.display.update()     
            else:
                pygame.draw.rect(self.SCREEN, (0, 0, 0), (x, y, w, h))
                pygame.display.update()     

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
        if type == 'players_discard':
                pygame.draw.rect(self.SCREEN, color, (1768-2, 850-2, self.image_x+2, 2))
                pygame.draw.rect(self.SCREEN, color, (1768+self.image_x, 850-2, 2, self.image_y+2))
                pygame.draw.rect(self.SCREEN, color, (1768-2, 850-2, 2, self.image_y+2))
                pygame.draw.rect(self.SCREEN, color, (1768-2, 850+self.image_y, self.image_x+4, 2))

        pygame.display.update()

    def get_border_color(self, type, position):
        if type == 'basic':
            pile = self.basic_piles[position]
            card = pile.top_card()
            if self.player.phase == 'buy':
                if self.player.buys > 0 and self.player.treasure >= card.price and card not in self.player.activated_cards:         
                    return (0, 255, 0)
                if card in self.player.activated_cards:
                    return (255, 255, 0) 

        if type == 'kingdom':
            pile = self.kingdom_piles[position]
            card = pile.top_card()
            if self.player.phase == 'buy':         
                if self.player.buys > 0 and self.player.treasure >= card.price and card not in self.player.activated_cards:         
                    return (0, 255, 0)
                if card in self.player.activated_cards:
                    return (255, 255, 0) 

        if type == 'players_hand':
            card = self.player.hand.cards[position]
            if self.player.phase == 'buy' and card.card_type == 'treasure':                     
                if card in self.player.activated_cards:
                    return (255, 255, 0)                    
                else:
                    return (255, 0, 0)

        if type == 'players_discard':
            card = self.player.discard.top_card()
            if self.player.phase == 'buy':  
                if card in self.player.activated_cards:
                    return (255, 255, 0)                    
                 
        return (0, 0, 0)

    def redraw_borders(self):
        for pile in self.basic_piles:
            self.border_pile(self.get_border_color('basic', pile.position),'basic', pile.position)
        for pile in self.kingdom_piles:
            self.border_pile(self.get_border_color('kingdom', pile.position),'kingdom', pile.position)
        hand = self.player.hand
        for i in range(len(hand.cards)):
            self.border_pile(self.get_border_color('players_hand', i), 'players_hand', i)
        self.border_pile(self.get_border_color('players_discard', 0), 'players_discard', 0)


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
        if y > 850 and x > 1768:
            return { 'players_discard' : 0}
        return None

    def detect_hover(self, x, y):
        if self.detail_displayed == False:
            if self.search_pile_coordinates(x, y) is not None:
                pile = self.search_pile_coordinates(x, y)
                for pile_type in pile:
                    if self.selected == None:
                        if self.get_border_color(pile_type, pile[pile_type]) == (0, 0, 0):
                            if pile_type != 'players_discard' or len(self.player.discard.cards):
                                self.border_pile((0, 0, 255), pile_type, pile[pile_type])
                                self.selected = { pile_type : pile[pile_type] }
                    elif self.selected != { pile_type : pile[pile_type] }:
                        for selected in self.selected:
                            self.border_pile(self.get_border_color(selected, self.selected[selected]), selected, self.selected[selected])
                            if pile_type != 'players_discard' or len(self.player.discard.cards):
                                if self.get_border_color(pile_type, pile[pile_type]) == (0, 0, 0):
                                    self.border_pile((0, 0, 255), pile_type, pile[pile_type])
                        self.selected = { pile_type : pile[pile_type] }
            elif self.selected is not None:
                self.selected = None
                self.redraw_borders()

        if x > 1700 and x < 1700+150 and y > 10 and y < 10+40:
            self.draw_action_button((130, 130, 130))
        else:
            self.draw_action_button()


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
                    elif pile_type == 'players_discard':
                        card = self.player.discard.top_card()
                    if card is not None:   
                        card.draw_card_detail(self.SCREEN)
                        pygame.display.update()
                        self.detail_displayed = True
        else:
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
                        if self.player.phase == 'buy':
                            if self.player.buys > 0 and card.price <= self.player.treasure:
                                    card = pile.get_top_card()
                                    self.player.put_card_to_discard(card)
                                    self.player.activated_cards.update({ card : pile })
                                    self.player.buys = self.player.buys - 1
                                    self.player.treasure = self.player.treasure - card.price    
                                    self.draw()

                    elif pile_type == 'kingdom':
                        pile = self.kingdom_piles[pile[pile_type]]
                        card = pile.top_card()
                        if self.player.phase == 'buy':
                            if self.player.buys > 0 and card.price <= self.player.treasure:
                                    card = pile.get_top_card()
                                    self.player.put_card_to_discard(card)
                                    self.player.activated_cards.update({ card : pile })
                                    self.player.buys = self.player.buys - 1
                                    self.player.treasure = self.player.treasure - card.price     
                                    self.draw()

                    elif pile_type == 'players_hand':
                        card = self.player.hand.cards[pile[pile_type]]
                        if self.player.phase == 'buy' and card.card_type == 'treasure':
                            if card not in self.player.activated_cards:
                                self.player.activated_cards.update({ card : self.player.hand })
                                self.player.treasure = self.player.treasure + card.value                     
                            elif self.player.treasure - card.value >= 0:
                                del self.player.activated_cards[card]
                                self.player.treasure = self.player.treasure - card.value  

                    elif pile_type == 'players_discard':
                        card = self.player.discard.top_card()                    
                        if self.player.phase == 'buy' and card in self.player.activated_cards:
                            card = self.player.discard.get_top_card()      
                            self.player.activated_cards[card].add_card(card)
                            del self.player.activated_cards[card]
                            self.player.buys = self.player.buys + 1
                            self.player.treasure = self.player.treasure + card.price     
                            self.draw()                                           

                self.redraw_borders()   
                self.draw_info()
    
    def action_button_click(self, x, y):
        if x > 1700 and x < 1700+150 and y > 10 and y < 10+40:
            self.player.phase = 'cleanup'
            for card in self.player.activated_cards:
                for pile in self.basic_piles:
                    if card == pile.top_card():
                        pile.get_top_card()
                for pile in self.kingdom_piles:
                    if card == pile.top_card():
                        pile.get_top_card()
            self.player.cleanup_phase(self)


               