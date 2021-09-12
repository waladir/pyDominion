# 2
from libs.library.Intrigue2nd.Courtyard import Courtyard
from libs.library.Intrigue2nd.Lurker import Lurker
from libs.library.Intrigue2nd.Pawn import Pawn

# 3
from libs.library.Intrigue2nd.Masquerade import Masquerade
from libs.library.Intrigue2nd.Shanty_Town import Shanty_Town
from libs.library.Intrigue2nd.Steward import Steward
from libs.library.Intrigue2nd.Swindler import Swindler
from libs.library.Intrigue2nd.Wishing_Well import Wishing_Well

# 4
from libs.library.Intrigue2nd.Baron import Baron
from libs.library.Intrigue2nd.Bridge import Bridge
from libs.library.Intrigue2nd.Conspirator import Conspirator
from libs.library.Intrigue2nd.Diplomat import Diplomat
from libs.library.Intrigue2nd.Ironworks import Ironworks
from libs.library.Intrigue2nd.Mill import Mill
from libs.library.Intrigue2nd.Mining_Village import Mining_Village
from libs.library.Intrigue2nd.Secret_Passage import Secret_Passage

# 5
from libs.library.Intrigue2nd.Courtier import Courtier
from libs.library.Intrigue2nd.Duke import Duke
from libs.library.Intrigue2nd.Minion import Minion

from libs.library.Intrigue2nd.Patrol import Patrol
from libs.library.Intrigue2nd.Replace import Replace
from libs.library.Intrigue2nd.Torturer import Torturer
from libs.library.Intrigue2nd.Trading_Post import Trading_Post
from libs.library.Intrigue2nd.Upgrade import Upgrade

# 6
from libs.library.Intrigue2nd.Harem import Harem
from libs.library.Intrigue2nd.Nobles import Nobles

def get_cards(type = None, kingdom_card = None):
    cards = {}
    card_names = ['Courtyard', 'Lurker', 'Pawn', 'Masquerade', 'Shanty_Town', 'Steward', 'Swindler', 'Wishing_Well', 'Baron', 'Bridge', 'Conspirator', 'Diplomat', 'Ironworks', 'Mill', 'Mining_Village', 'Secret_Passage', 'Courtier', 'Duke', 'Minion', 'Patrol', 'Replace', 'Torturer', 'Trading_Post', 'Upgrade', 'Harem', 'Nobles']
    for card_name in card_names:
        cardClass = get_class(card_name)
        card = cardClass()
        if (type is None or type in card.type) and (kingdom_card is None or card.kingdom_card == kingdom_card):
            cards.update({ card.name_en : { 'id' : card.id, 'name' : card.name, 'name_en' : card.name_en, 'image' : card.image, 'expansion' : card.expansion, 'type' : card.type, 'subtype' : card.subtype, 'price' : card.price, 'value' : card.value }})
    return cards

def get_class(className):
    return globals()[className]

