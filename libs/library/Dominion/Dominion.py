from libs.library.Dominion.Copper import Copper
from libs.library.Dominion.Silver import Silver
from libs.library.Dominion.Gold import Gold

from libs.library.Dominion.Estate import Estate
from libs.library.Dominion.Duchy import Duchy
from libs.library.Dominion.Province import Province

from libs.library.Dominion.Curse import Curse

# 2
from libs.library.Dominion.Cellar import Cellar
from libs.library.Dominion.Chapel import Chapel
from libs.library.Dominion.Moat import Moat

# 3
from libs.library.Dominion.Chancellor import Chancellor
from libs.library.Dominion.Woodcutter import Woodcutter
from libs.library.Dominion.Village import Village
from libs.library.Dominion.Workshop import Workshop

# 4
from libs.library.Dominion.Bureaucrat import Bureaucrat
from libs.library.Dominion.Gardens import Gardens
from libs.library.Dominion.Feast import Feast
from libs.library.Dominion.Moneylender import Moneylender
from libs.library.Dominion.Militia import Militia
from libs.library.Dominion.Remodel import Remodel
from libs.library.Dominion.Smithy import Smithy
from libs.library.Dominion.Spy import Spy
from libs.library.Dominion.Thief import Thief
from libs.library.Dominion.Throne_Room import Throne_Room

# 5
from libs.library.Dominion.Market import Market
from libs.library.Dominion.Mine import Mine
from libs.library.Dominion.Festival import Festival
from libs.library.Dominion.Laboratory import Laboratory
from libs.library.Dominion.Library import Library
from libs.library.Dominion.Witch import Witch
from libs.library.Dominion.Council_Room import Council_Room

# 6
from libs.library.Dominion.Adventurer import Adventurer

def get_cards(type = None, kingdom_card = None):
    cards = {}
    card_names = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province', 'Curse', 'Cellar', 'Chapel', 'Moat', 'Chancellor', 'Woodcutter', 'Village', 'Workshop', 'Bureaucrat', 'Gardens', 'Feast', 'Moneylender', 'Militia', 'Remodel', 'Smithy', 'Spy', 'Thief', 'Throne_Room', 'Market', 'Mine', 'Festival', 'Laboratory', 'Library', 'Witch', 'Council_Room', 'Adventurer']
    for card_name in card_names:
        cardClass = get_class(card_name)
        card = cardClass()
        if (type is None or type in card.type) and (kingdom_card is None or card.kingdom_card == kingdom_card):
            cards.update({ card.name_en : { 'id' : card.id, 'name' : card.name, 'name_en' : card.name_en, 'image' : card.image, 'expansion' : card.expansion, 'type' : card.type, 'subtype' : card.subtype, 'price' : card.price, 'value' : card.value }})
    return cards

def get_class(className):
    return globals()[className]

