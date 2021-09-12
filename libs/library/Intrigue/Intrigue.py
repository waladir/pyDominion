# 2
from libs.library.Intrigue.Courtyard import Courtyard
from libs.library.Intrigue.Pawn import Pawn
from libs.library.Intrigue.Secret_Chamber import Secret_Chamber

# 3
from libs.library.Intrigue.Great_Hall import Great_Hall
from libs.library.Intrigue.Masquerade import Masquerade
from libs.library.Intrigue.Shanty_Town import Shanty_Town
from libs.library.Intrigue.Steward import Steward
from libs.library.Intrigue.Swindler import Swindler
from libs.library.Intrigue.Wishing_Well import Wishing_Well

# 4
from libs.library.Intrigue.Baron import Baron
from libs.library.Intrigue.Bridge import Bridge
from libs.library.Intrigue.Conspirator import Conspirator
from libs.library.Intrigue.Coppersmith import Coppersmith
from libs.library.Intrigue.Ironworks import Ironworks
from libs.library.Intrigue.Mining_Village import Mining_Village
from libs.library.Intrigue.Scout import Scout

# 5
from libs.library.Intrigue.Duke import Duke
from libs.library.Intrigue.Minion import Minion
from libs.library.Intrigue.Saboteur import Saboteur
from libs.library.Intrigue.Torturer import Torturer
from libs.library.Intrigue.Trading_Post import Trading_Post
from libs.library.Intrigue.Tribute import Tribute 
from libs.library.Intrigue.Upgrade import Upgrade

# 6
from libs.library.Intrigue.Harem import Harem
from libs.library.Intrigue.Nobles import Nobles

def get_cards(type = None, kingdom_card = None):
    cards = {}
    card_names = ['Courtyard', 'Pawn', 'Secret_Chamber', 'Great_Hall', 'Masquerade', 'Shanty_Town', 'Steward', 'Swindler', 'Wishing_Well', 'Baron', 'Bridge', 'Conspirator', 'Coppersmith', 'Ironworks', 'Mining_Village', 'Scout', 'Duke', 'Minion', 'Saboteur', 'Torturer', 'Trading_Post', 'Tribute', 'Upgrade', 'Harem', 'Nobles']
    for card_name in card_names:
        cardClass = get_class(card_name)
        card = cardClass()
        if (type is None or type in card.type) and (kingdom_card is None or card.kingdom_card == kingdom_card):
            cards.update({ card.name_en : { 'id' : card.id, 'name' : card.name, 'name_en' : card.name_en, 'image' : card.image, 'expansion' : card.expansion, 'type' : card.type, 'subtype' : card.subtype, 'price' : card.price, 'value' : card.value }})
    return cards

def get_class(className):
    return globals()[className]

