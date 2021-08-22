from libs.library.Dominion2nd.Copper import Copper
from libs.library.Dominion2nd.Silver import Silver
from libs.library.Dominion2nd.Gold import Gold

from libs.library.Dominion2nd.Estate import Estate
from libs.library.Dominion2nd.Duchy import Duchy
from libs.library.Dominion2nd.Province import Province

from libs.library.Dominion2nd.Curse import Curse

# 2
from libs.library.Dominion2nd.Cellar import Cellar
from libs.library.Dominion2nd.Chapel import Chapel
from libs.library.Dominion2nd.Moat import Moat

# 3
from libs.library.Dominion2nd.Harbinger import Harbinger
from libs.library.Dominion2nd.Merchant import Merchant
from libs.library.Dominion2nd.Vassal import Vassal
from libs.library.Dominion2nd.Village import Village
from libs.library.Dominion2nd.Workshop import Workshop

# 4
from libs.library.Dominion2nd.Bureaucrat import Bureaucrat
from libs.library.Dominion2nd.Gardens import Gardens
from libs.library.Dominion2nd.Moneylender import Moneylender
from libs.library.Dominion2nd.Militia import Militia
from libs.library.Dominion2nd.Poacher import Poacher
from libs.library.Dominion2nd.Remodel import Remodel
from libs.library.Dominion2nd.Smithy import Smithy
from libs.library.Dominion2nd.Throne_Room import Throne_Room

# 5
from libs.library.Dominion2nd.Bandit import Bandit
from libs.library.Dominion2nd.Council_Room import Council_Room
from libs.library.Dominion2nd.Festival import Festival
from libs.library.Dominion2nd.Laboratory import Laboratory
from libs.library.Dominion2nd.Library import Library
from libs.library.Dominion2nd.Market import Market
from libs.library.Dominion2nd.Mine import Mine
from libs.library.Dominion2nd.Sentry import Sentry
from libs.library.Dominion2nd.Witch import Witch

# 6
from libs.library.Dominion2nd.Artisan import Artisan

def get_cards(type = None, kingdom_card = None):
    cards = {}
    card_names = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province', 'Curse', 'Cellar', 'Chapel', 'Moat', 'Harbinger', 'Merchant', 'Vassal', 'Village', 'Workshop', 'Bureaucrat', 'Gardens', 'Moneylender', 'Militia', 'Poacher', 'Remodel', 'Smithy', 'Throne_Room', 'Bandit', 'Council_Room', 'Festival', 'Laboratory', 'Library', 'Market', 'Mine', 'Sentry', 'Witch', 'Artisan']
    for card_name in card_names:
        cardClass = get_class(card_name)
        card = cardClass()
        if (type is None or type in card.type) and (kingdom_card is None or card.kingdom_card == kingdom_card):
            cards.update({ card.name_en : { 'id' : card.id, 'name' : card.name, 'name_en' : card.name_en, 'image' : card.image, 'expansion' : card.expansion, 'type' : card.type, 'subtype' : card.subtype, 'price' : card.price, 'value' : card.value }})
    return cards

def get_class(className):
    return globals()[className]

