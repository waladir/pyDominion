# 2
from libs.library.Seaside.Embargo import Embargo
from libs.library.Seaside.Haven import Haven
from libs.library.Seaside.Lighthouse import Lighthouse
# Native Village
from libs.library.Seaside.Pearl_Diver import Pearl_Diver

# 3
# Ambassador
# Fishing Village
# Lookout
# Smugglers
# Warehouse

# 4
# Caravan
# Cutpurse
# Island
# Navigator
# Pirate Ship
# Salvager
# Sea Hag
# Treasure Map

# 5
from libs.library.Seaside.Bazaar import Bazaar
# Explorer
# Ghost Ship
# Metchant Ship
# Outpost
# Tactician
# Treasury
# Wharf

def get_cards(type = None, kingdom_card = None):
    cards = {}
    card_names = ['Embargo', 'Haven', 'Bazaar', 'Lighthouse', 'Pearl_Diver']
    for card_name in card_names:
        cardClass = get_class(card_name)
        card = cardClass()
        if (type is None or type in card.type) and (kingdom_card is None or card.kingdom_card == kingdom_card):
            cards.update({ card.name_en : { 'id' : card.id, 'name' : card.name, 'name_en' : card.name_en, 'image' : card.image, 'expansion' : card.expansion, 'type' : card.type, 'subtype' : card.subtype, 'price' : card.price, 'value' : card.value }})
    return cards

def get_class(className):
    return globals()[className]

