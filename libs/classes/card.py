import os
import pygame

from libs.cards import cards
from libs.expansions import expansions

class Card():
    def __init__(self, name):
        card_data = self.get_card_data(name)
        self.name = card_data['name'] 
        self.name_en = card_data['name_en']
        self.expansion = card_data['expansion']
        self.image = card_data['image']
        self.kingdom_card = card_data['kingdom_card']
        self.card_type = card_data['card_type']
        self.card_subtype = card_data['card_subtype']
        self.price = card_data['price']
        self.value = card_data['value']

    def get_card_data(self, name):
        for expansion in expansions:
            if expansions[expansion]['enabled'] == True:
                expansion_cards = cards[expansion]
                for card_id in expansion_cards:
                    if card_id == name:
                        return { 'name' : name, 'name_en' : expansion_cards[card_id]['name_en'], 'expansion' : expansion, 'image' : expansion_cards[card_id]['image'], 'kingdom_card' : expansion_cards[card_id]['kingdom_card'], 'card_type' : expansion_cards[card_id]['card_type'], 'card_subtype' : expansion_cards[card_id]['card_subtype'], 'price' : expansion_cards[card_id]['price'], 'value' : expansion_cards[card_id]['value'] }

    def draw_card(self, SCREEN, position, hidden = False):
        base_dir = os.getcwd()
        cards_images_dir = os.path.join(base_dir, 'resources','img','cards')
        if hidden == False:
            card = pygame.image.load(os.path.join(cards_images_dir, self.expansion, self.name_en + '.jpg'))    
            card = pygame.transform.scale(card, (150, 240))
            SCREEN.blit(card, position)
        else:
            card = pygame.image.load(os.path.join(cards_images_dir, 'back.jpg'))    
            card = pygame.transform.scale(card, (150, 240))
            SCREEN.blit(card, position)

    def draw_card_detail(self, SCREEN):
        base_dir = os.getcwd()
        cards_images_dir = os.path.join(base_dir, 'resources','img','cards')
        card = pygame.image.load(os.path.join(cards_images_dir, self.expansion, self.name_en + '.jpg'))    
        card = pygame.transform.scale(card,(374,600))
        SCREEN.blit(card, (773, 0))
