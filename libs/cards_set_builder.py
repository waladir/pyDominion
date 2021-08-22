import sys
import os

import math
import pygame
from pygame.locals import *
from libs.config import image_x, image_y, image_spacing, image_left_margin

def select_cards_to_cards_set(SCREEN, cards, selected_cards = None):
    global skip 
    skip = False
    SCREEN.fill(pygame.Color(0, 0, 0))
    x = 0
    y = 0  
    global selected
    selected = []  
    global select_offset
    select_offset = 0

    if selected_cards is not None:
        selected = selected_cards
        draw_selected(SCREEN, cards)

    draw(SCREEN, selected, cards)

    while skip ==  False:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()    
            if event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                if select_offset + 11 < len(cards):
                    select_offset = select_offset + 1
                    draw_select_area(SCREEN, cards)
            if event.type == pygame.KEYDOWN and event.key == K_LEFT:
                if select_offset > 0:
                    select_offset = select_offset - 1
                    draw_select_area(SCREEN, cards)
            if event.type == pygame.MOUSEBUTTONDOWN:            
                if event.button == 1:
                    x, y = event.pos 
                    select_card(SCREEN, cards, x, y)
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos 
            detect_hover(SCREEN, x, y)
    return selected

def select_card(SCREEN, cards, x, y):
    global select_offset
    global selected
    global skip

    if y > 830 and y < 830 + 240:
        x = x - image_left_margin
        position = math.floor(x/(image_x + 20)) + select_offset
        i = 0
        for card in cards:
            if i == position and position - select_offset < 11:
                if card in selected:
                    selected.remove(card)
                    color = (0, 0, 0)
                elif len(selected) < 10:
                    selected.append(card)
                    color = (150, 150, 150)
                draw_border(SCREEN, color, (image_left_margin + ((position - select_offset) * (image_x + 20)), 830))
                draw_selected(SCREEN, cards)
            i = i +1
    if x > 1700 and x < 1700+150 and y > 10 and y < 10+40 and len(selected) == 10:
        skip = True


def detect_hover(SCREEN, x, y):
    if x > 1700 and x < 1700+150 and y > 10 and y < 10+40:
        draw_action_button(SCREEN, (130, 130, 130))
    else:
        draw_action_button(SCREEN)

def draw_action_button(SCREEN, color = (150, 150, 150)):
    global selected
    x = 1700
    y = 10
    w = 160
    h = 40
    if len(selected) == 10:
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render('Konec výběru karet', True, (230, 230, 230))
        text_x = x + 10
        pygame.draw.rect(SCREEN, color, (x, y, w, h))
        SCREEN.blit(text, (text_x, y+13)) 
        pygame.display.update()                 
    else:
        pygame.draw.rect(SCREEN, (0, 0, 0), (x, y, w, h))
        pygame.display.update()   

def draw_card(SCREEN, card, position):
    base_dir = os.getcwd()
    library_dir = os.path.join(base_dir, 'libs', 'library')
    img = pygame.image.load(os.path.join(library_dir, card['expansion'], 'images', card['image']))    
    img = pygame.transform.smoothscale(img, (157, 240))
    SCREEN.blit(img, position)
    pygame.display.update()

def draw_selected_card(SCREEN, card, position):
    base_dir = os.getcwd()
    library_dir = os.path.join(base_dir, 'libs', 'library')
    img = pygame.image.load(os.path.join(library_dir, card['expansion'], 'images', card['image']))        
    img = pygame.transform.smoothscale(img, (235, 360))
    SCREEN.blit(img, position)
    pygame.display.update()


def draw_border(SCREEN, color, position):
    (x, y) = position
    pygame.draw.rect(SCREEN, color, (x - 2, y - 2, image_x + 8, 2))
    pygame.draw.rect(SCREEN, color, (x + image_x + 6, y-2, 2, image_y + 2))
    pygame.draw.rect(SCREEN, color, (x - 2, y - 2, 2, image_y + 2))
    pygame.draw.rect(SCREEN, color, (x - 2, y + image_y, image_x + 8, 2))
    pygame.display.update()

def draw_selected(SCREEN, cards):
    global selected
    pygame.draw.rect(SCREEN, (0, 0, 0), (0, 10, 1920, 10 + 360 * 2 + 20 ))
    y = 10
    i = 0
    for card in cards:
        if card in selected:
            if i < 5:
                draw_selected_card(SCREEN, cards[card], (270 + (i * (235 + 50)), y))
            else:
                draw_selected_card(SCREEN, cards[card], (270 + ((i - 5) * (235 + 50)), y + 360 + 20))
            i = i + 1
    draw_action_button(SCREEN)

def draw_select_area(SCREEN, cards):
    global select_offset
    global selected
    pygame.draw.rect(SCREEN, (0, 0, 0), (0, 830 - 20, 1920, 240 + 10 + 20))
    y = 830
    if len(cards) - select_offset > 11:
        last_card = 11 +  select_offset
    else:
        last_card = len(cards)
    i = 0
    for card in cards:
        if i >= select_offset and i < last_card:
            if card in selected:
                color = (150, 150, 150)
            else:
                color = (0, 0, 0)
            if select_offset > 0 and i - select_offset == 0:
                font = pygame.font.Font('freesansbold.ttf', 25)
                text = font.render('<<<', True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (image_left_margin + ((i - select_offset) * (image_x + 20)) + 75, y-15) 
                SCREEN.blit(text, textRect)  
            if last_card < len(cards) and i - select_offset == 10:
                font = pygame.font.Font('freesansbold.ttf', 25)
                text = font.render('>>>', True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (image_left_margin + ((i - select_offset) * (image_x + 20)) + 75, y-15) 
                SCREEN.blit(text, textRect)   
            draw_card(SCREEN, cards[card], (image_left_margin + ((i - select_offset) * (image_x + 20)), y))
            draw_border(SCREEN, color, (image_left_margin + ((i - select_offset) * (image_x + 20)), y))
        i = i + 1

def draw(SCREEN, selected, cards):
    draw_select_area(SCREEN, cards)
