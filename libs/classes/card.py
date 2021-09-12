import os
import pygame

from libs.expansions import expansions

class Card():
    def __init__(self):
        self.pile = None
        self.desk = None
        self.game = None
        self.player = None
        self.action = None

        self.skip_cleanup = False
        self.hidden = 0

    def draw_card(self, SCREEN, position, hidden = False):
        base_dir = os.getcwd()
        library_dir = os.path.join(base_dir, 'libs', 'library')
        if hidden == False:
            card = pygame.image.load(os.path.join(library_dir, self.expansion, 'images', self.image))
            card = card.convert_alpha()
            card = pygame.transform.smoothscale(card, (157, 240)) 
            SCREEN.blit(card, position)
        else:
            card = pygame.image.load(os.path.join(library_dir, 'back.jpg'))    
            card = pygame.transform.scale(card, (157, 240))
            SCREEN.blit(card, position)

    def draw_card_detail(self, SCREEN):
        base_dir = os.getcwd()
        library_dir = os.path.join(base_dir, 'libs', 'library')
        if self.pile.hidden_pile != 1:
            card = pygame.image.load(os.path.join(library_dir, self.expansion, 'images', self.image))    
        else:
            card = pygame.image.load(os.path.join(library_dir, 'back.jpg'))    
        SCREEN.blit(card, (773, 0))

