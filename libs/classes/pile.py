import os
import random
import math

import pygame

from libs.config import image_x, image_y, image_spacing, image_left_margin

from libs.library.Dominion import Dominion
from libs.library.Dominion2nd import Dominion2nd
from libs.library.Intrigue import Intrigue
from libs.library.Intrigue2nd import Intrigue2nd

from libs.events import create_event

class Pile():
    def __init__(self, place, position, game):
        self.place = place
        self.position = position
        self.cards = []
        self.game = game
    
    def get_class(self, card_name):
        for expansion in self.game.expansions:
            cards = globals()[expansion].get_cards()
            if card_name in cards:
                return globals()[expansion].get_class(card_name)
        return None

    def create_pile(self, card_name, count):
        for i in range(count):
            cardClass = self.get_class(card_name)
            self.create_card(cardClass)
            self.card_id = self.cards[0].id
            self.card_name = self.cards[0].name_en

    def create_players_pile(self):
        # self.create_pile('Copper', 7)
        # self.create_pile('Estate', 3)
        self.create_pile('Witch', 7)
        self.create_pile('Moat', 7)
        self.shuffle()        

    def create_card(self, cardClass):
        card = cardClass()
        card.pile = self
        card.game = self.game
        card.desk = self.game.desk
        card.player = self.game.desk.player
        self.cards.insert(0, card)


    def add_card(self, card, append = False, event = True):
        card.pile = self
        card.game = self.game
        card.desk = self.game.desk
        card.player = self.game.desk.player
        if append == True:
            self.cards.append(card)
        else:
            self.cards.insert(0, card)
        if event == True and (self.place == 'basic' or self.place == 'kingdom' or self.place == 'thrash' or self.place == 'play_area'):
            create_event(self, 'add_card', { 'place' : self.place, 'position' : self.position, 'card_name' : card.name_en, 'append' : append }, self.game.get_other_players_names())

    def top_card(self):
        if len(self.cards) > 0:
            return self.cards[0]
        return None

    def get_top_card(self, event = True):
        if len(self.cards) > 0:
            card = self.cards[0]
            self.cards.remove(card)
            if event == True and (self.place == 'basic' or self.place == 'kingdom' or self.place == 'thrash' or self.place == 'play_area'):
                if self.place == 'play_area':
                    create_event(self, 'remove_card', { 'place' : self.place, 'card_id' : card.id }, self.game.get_other_players_names())
                else:
                    create_event(self, 'remove_card', { 'place' : self.place, 'position' : self.position }, self.game.get_other_players_names())
                self.game.check_end(card)
            return card

    def shuffle(self):
        random.shuffle(self.cards)

    def get_coordinates(self, desk = None):
        font = pygame.font.Font('freesansbold.ttf', 20)
        if self.place == 'basic' or self.place == 'kingdom':
            if self.place == 'basic':
                y = 30
            if self.place == 'kingdom':
                y = 290
            x = image_left_margin + self.position * (image_x + image_spacing)
        if self.place == 'trash':
            x = 1762
            y = 290
        if self.place == 'players_deck':
            x = 2
            y = 838
        if self.place == 'players_hand':
            position_offset = math.floor((8 - desk.players_hand_count) / 2)
            if self.position - desk.players_hand_offset >= 0 and self.position - desk.players_hand_offset < 8:
                x = image_left_margin + 300 + ((self.position - desk.players_hand_offset) + position_offset) * (image_x + image_spacing)
                y = 838
            else:
                x = -1
                y = -1
        if self.place == 'players_discard':
            x = 1762
            y = 838
        if self.place == 'play_area':
            position_offset = math.floor((12 - desk.play_area_count) / 2)
            if self.position >= 0 and self.position < 12:
                x = image_left_margin + (self.position + position_offset) * (image_x + image_spacing)
                y = 575
            else:
                x = -1
                y = -1
        if self.place == 'select_area':
            position_offset = math.floor((12 - desk.select_area_count) / 2)
            if self.position - desk.select_area_offset >= 0 and self.position - desk.select_area_offset < 12:
                x = image_left_margin + ((self.position - desk.select_area_offset) + position_offset) * (image_x + image_spacing)
                y = 575
            else:
                x = -1
                y = -1
        return x, y

    def draw_pile(self, SCREEN, desk = None, not_show = False):
        x, y = self.get_coordinates(desk)
        card = self.top_card()
        if self.place != 'players_hand' and self.place != 'select_area':
            if len(self.cards) > 0:
                if self.place != 'play_area' or len(self.cards) > 1:
                    font = pygame.font.Font('freesansbold.ttf', 18)
                    text = font.render(str(len(self.cards)), True, (0, 255, 0))
                    textRect = text.get_rect()
                    textRect.center = (x + image_x/2, y-8) 
                    SCREEN.blit(text, textRect)   
        if self.place == 'players_hand' and desk.select_area == False:
            if len(desk.player.hand) > desk.players_hand_count:
                if desk.players_hand_offset > 0:
                    if self.position - desk.players_hand_offset == 0:
                        font = pygame.font.Font('freesansbold.ttf', 25)
                        text = font.render('<<<', True, (255, 255, 255))
                        textRect = text.get_rect()
                        textRect.center = (x + 75, y-15) 
                        SCREEN.blit(text, textRect)                 
                elif self.position - desk.players_hand_offset == 0:
                    pygame.draw.rect(SCREEN, (0, 0, 0), (x, y - 2 - 30, 140, 30))
                if desk.players_hand_offset + desk.players_hand_count < len(desk.player.hand):
                    if self.position - desk.players_hand_offset == 7:
                        font = pygame.font.Font('freesansbold.ttf', 25)
                        text = font.render('>>>', True, (255, 255, 255))
                        textRect = text.get_rect()
                        textRect.center = (x + 75, y-15) 
                        SCREEN.blit(text, textRect)                 
                elif self.position - desk.players_hand_offset == 7:
                    pygame.draw.rect(SCREEN, (0, 0, 0), (x, y - 2 - 30, 140, 30))
        if self.place == 'select_area' and desk.select_area == True:
            if len(desk.select_area_piles) > desk.select_area_count:
                if desk.select_area_offset > 0:
                    if self.position - desk.select_area_offset == 0:
                        font = pygame.font.Font('freesansbold.ttf', 25)
                        text = font.render('<<<', True, (255, 255, 255))
                        textRect = text.get_rect()
                        textRect.center = (x + 75, y-15) 
                        SCREEN.blit(text, textRect)                 
                elif self.position - desk.select_area_offset == 0:
                    pygame.draw.rect(SCREEN, (0, 0, 0), (x, y - 2 - 15, 140, 30))
                if desk.select_area_offset + desk.select_area_count < len(desk.select_area_piles):
                    if self.position - desk.select_area_offset == 11:
                        font = pygame.font.Font('freesansbold.ttf', 25)
                        text = font.render('>>>', True, (255, 255, 255))
                        textRect = text.get_rect()
                        textRect.center = (x + 75, y-15) 
                        SCREEN.blit(text, textRect)                 
                elif self.position - desk.select_area_offset == 11:
                    pygame.draw.rect(SCREEN, (0, 0, 0), (x, y - 2 - 15, 140, 30))
                                
        if self.place == 'players_deck':
            not_show = True
        if card is not None:   
            card.draw_card(SCREEN, (x, y), not_show)  

    def border_pile(self, SCREEN, color, desk):
        x, y = self.get_coordinates(desk)
        if x > 0 and y > 0:
            pygame.draw.rect(SCREEN, color, (x, y, image_x + 8, 2))
            pygame.draw.rect(SCREEN, color, (x + image_x + 8 - 2, y, 2, image_y))
            pygame.draw.rect(SCREEN, color, (x, y, 2, image_y))
            pygame.draw.rect(SCREEN, color, (x, y + image_y, image_x + 8 - 2, 2))
            pygame.display.update()

    def test_coordinates(self, x, y, desk):
        pile_x, pile_y = self.get_coordinates(desk)
        if x > pile_x and x < pile_x + image_x and y > pile_y and y < pile_y + image_y:
            return True
        else:
            return False