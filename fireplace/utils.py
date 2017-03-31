import random
import os.path
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree
from hearthstone.enums import CardClass, CardType
import sys
import copy


# Autogenerate the list of cardset modules
_cards_module = os.path.join(os.path.dirname(__file__), "cards")
CARD_SETS = [cs for _, cs, ispkg in iter_modules([_cards_module]) if ispkg]


class CardList(list):
	def __contains__(self, x):
		for item in self:
			if x is item:
				return True
		return False

	def __getitem__(self, key):
		ret = super().__getitem__(key)
		if isinstance(key, slice):
			return self.__class__(ret)
		return ret

	def __int__(self):
		# Used in Kettle to easily serialize CardList to json
		return len(self)

	def contains(self, x):
		"True if list contains any instance of x"
		for item in self:
			if x == item:
				return True
		return False

	def index(self, x):
		for i, item in enumerate(self):
			if x is item:
				return i
		raise ValueError

	def remove(self, x):
		for i, item in enumerate(self):
			if x is item:
				del self[i]
				return
		raise ValueError

	def exclude(self, *args, **kwargs):
		if args:
			return self.__class__(e for e in self for arg in args if e is not arg)
		else:
			return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k) != v)

	def filter(self, **kwargs):
		return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k, 0) == v)

def prepare_collection(card_class:CardClass,exclude=[],includesets=["NEW1","EX1","OG","KAR","CS2"]):
	from . import cards	
	collection = []
	hero = card_class.default_hero
	#print(cards.db)


	for card in cards.db.keys():

		if card in exclude:
			continue

		cls = cards.db[card]
		clsin=False
		for cset in includesets:
			if cset in cls.id:
				clsin=True
				#print(cls.id+cls.name+str(cls.health)+str(cls.battlecry))
				break
			
			pass
		if not clsin:
			continue
			pass
		if 'Jade' in cls.name:
			#print(cls.id+cls.name+str(cls.health)+str(cls.battlecry))
			#input("findjade")
			pass
		
		if not cls.collectible:
			continue
		
		if cls.type == CardType.HERO:
			# Heroes are collectible...
			continue
		#print(cls)
		#print(cls.type)
		#print(cls.card_class)
		#print(cls.card_sets)
		if cls.card_class and cls.card_class != card_class:
			continue
		collection.append(cls)
		
		#print("got")
	return collection
	
	pass
def random_draft(card_class: CardClass,exclude=[]):
	"""
	Return a deck of 30 random cards for the \a card_class and NEUTRAL class
	"""
	scollection=prepare_collection(card_class,exclude)
	ccollection=prepare_collection(CardClass.NEUTRAL,exclude)
	collection=scollection+ccollection
	#print(len(collection))	
	#print(collection)
	from .deck import Deck
	deck = []
	while len(deck) < Deck.MAX_CARDS:
		card = random.choice(collection)
		if deck.count(card.id) < card.max_count_in_deck:
			deck.append(card.id)

	return deck

def draft_by_cards_name(cardsnamelist,card_class:CardClass):
	scollection=prepare_collection(card_class)
	ccollection=prepare_collection(CardClass.NEUTRAL)
	collection=scollection+ccollection
	
	from .deck import Deck

	deck = []
	for cardname in cardsnamelist:
		find=False
		for card in collection:
			
			if card.name==cardname:
				deck.append(card.id)
				find=True
				break
			
			pass
		if not find:
			print('cant find '+cardname)
			pass
		pass

	return deck

def random_class():
	return CardClass(random.randint(2, 10))


def get_script_definition(id):
	"""
	Find and return the script definition for card \a id
	"""
	for cardset in CARD_SETS:
		module = import_module("fireplace.cards.%s" % (cardset))
		if hasattr(module, id):
			return getattr(module, id)


def entity_to_xml(entity):
	e = ElementTree.Element("Entity")
	for tag, value in entity.tags.items():
		if value and not isinstance(value, str):
			te = ElementTree.Element("Tag")
			te.attrib["enumID"] = str(int(tag))
			te.attrib["value"] = str(int(value))
			e.append(te)
	return e


def game_state_to_xml(game):
	tree = ElementTree.Element("HSGameState")
	tree.append(entity_to_xml(game))
	for player in game.players:
		tree.append(entity_to_xml(player))
	for entity in game:
		if entity.type in (CardType.GAME, CardType.PLAYER):
			# Serialized those above
			continue
		e = entity_to_xml(entity)
		e.attrib["CardID"] = entity.id
		tree.append(e)

	return ElementTree.tostring(tree)


def weighted_card_choice(source, weights: List[int], card_sets: List[str], count: int):
	"""
	Take a list of weights and a list of card pools and produce
	a random weighted sample without replacement.
	len(weights) == len(card_sets) (one weight per card set)
	"""

	chosen_cards = []

	# sum all the weights
	cum_weights = []
	totalweight = 0
	for i, w in enumerate(weights):
		totalweight += w * len(card_sets[i])
		cum_weights.append(totalweight)

	# for each card
	for i in range(count):
		# choose a set according to weighting
		chosen_set = bisect(cum_weights, random.random() * totalweight)

		# choose a random card from that set
		chosen_card_index = random.randint(0, len(card_sets[chosen_set]) - 1)

		chosen_cards.append(card_sets[chosen_set].pop(chosen_card_index))
		totalweight -= weights[chosen_set]
		cum_weights[chosen_set:] = [x - weights[chosen_set] for x in cum_weights[chosen_set:]]

	return [source.controller.card(card, source=source) for card in chosen_cards]


def setup_game() -> ".game.Game":
	from .game import Game
	from .player import Player
	from .deck import prepareddruiddeck,preparedwarriordeck
	
	print(len(prepareddruiddeck))
	#deck1=draft_by_cards_name(prepareddruiddeck,CardClass.DRUID)
	#deck2=draft_by_cards_name(preparedwarriordeck,CardClass.WARRIOR)
	deck1 = random_draft(CardClass.DRUID)
	#print(deck1)
	deck2 = random_draft(CardClass.WARRIOR)
	
	player1 = Player("Player1", deck1, CardClass.DRUID.default_hero)
	player2 = Player("Player2", deck2, CardClass.WARRIOR.default_hero)

	game = Game(players=(player1, player2))
	game.start()

	return game

def getreward(game:".game.Game"):
	player=game.current_player
	adavantage=0
	for cha in player.characters:
		adavantage+=cha.atk+cha.health+(cha.armor if cha.type==CardType.HERO else 0)
		pass
	for cha in player.opponent.characters:
		adavantage-=cha.atk+cha.health+(cha.armor if cha.type==CardType.HERO else 0)
		pass
	return adavantage
	pass

def move(game) :
	moveseqs=[]
	gamemovepairs=[]
	player = game.current_player
	input("s2")
	#if we are in choice state,we have to choice one  
	if player.choice:
		for choiceindex in range(len(player.choice.cards)):
			gamenew=copy.deepcopy(game)
			playernew = gamenew.current_player
			choice=playernew.choice.cards[choiceindex]
			print("Choosing card %r" % (choice))
			input("choice happen")
			player.choice.choose(choice)
			gamemovepairs.append((gamenew,moveseq))
			pass
	heropower = player.hero.power
	cardset=[card for card in player.hand if card.is_playable()]
	charset=[character for character in player.characters if character.can_attack()]

	if heropower.is_usable():
		if heropower.requires_target():
			for targetindex in range(len(heropower.targets)):
				gamenew=copy.deepcopy(game)
				playernew = gamenew.current_player
				print("useheropower")
				input("usepower")
				heropowernew=playernew.hero.power
				heropowernew.use(target=heropowernew.targets[targetindex])
				gamemovepairs.append((gamenew,moveseq))

				pass
			
		else:
			gamenew=copy.deepcopy(game)
			playernew = gamenew.current_player
			print("useheropower")
			input("usepower")
			heropowernew=playernew.hero.power
			heropowernew.use()
			gamemovepairs.append((gamenew,moveseq))

	# iterate over our hand and play whatever is playable
	
	print(cardset)
	#input("choosecard")
	if cardset:
		card=random.choice(cardset)
		target = None
		if card.must_choose_one:
			if not card.choose_cards :
				card = random.choice(card.choose_cards)
		if card.requires_target():
			if card.targets:
				target = random.choice(card.targets)
				pass
		print("Playing %r on %r" % (card, target))
		card.play(target=target)
	# Randomly attack with whatever can attack
	for cardindex in range(len(player.hand)):
		card=player.hand[cardindex]
		if card.is_playable():
			target = None
			if card.must_choose_one:
				for choiceindex in range(len(card.choose_cards)):
					
					pass
				pass
			else: 
				pass
			pass
		pass
	if charset:
		character=random.choice(charset)
		#input("s3")
		character.attack(random.choice(character.targets))
		#input("s")
	#print(game_state_to_xml(game))
	gamemovepairs.append(game,[])
	return gamemovepair
	pass
def useheropower(game:".game.Game",target=-1):
	heropower=game.current_player.hero.power
	if heropower.requires_target() and target >= 0 :
		heropower.use(target=heropower.targets[target])
	elif target<0:
		heropower.use()
	pass
def usechoice(game:".game.Game",target=-1):
	player=game.current_player
	if player.choice:
		choice = player.choice.cards[target]
		print("Choosing card %r" % (choice))
		input("choice happen")
		player.choice.choose(choice)
	else:
		input("no choice but usechoice")
	pass
def useplaycard(game:".game.Game",cardindex,mustchooseindex=-1,targetindex=-1):
	player=game.current_player
	
	card=player.hand[cardindex]
	target = None
	if card.must_choose_one :
		if mustchooseindex >= 0:
			card = card.choose_cards[mustchooseindex]
		else:
			input("mustchooseerror mustchoose"+str(card.must_choose_one)+str(mustchooseindex))
			return
	if card.requires_target():
		if card.targets:
			target = card.targets[targetindex]
		else:
			input("require_target but no suitable target")
			return	 
			pass
	input("Playing %r on %r" % (card, target))
	card.play(target=target)
def useattack(game:".game.Game",chaindex,targetindex):
	character=game.current_player.characters[chaindex]
	input("atk"+str(character)+str(targetindex))
	character.attack(character.targets[targetindex])
def play_turnnew(game: ".game.Game") -> ".game.Game":
	game,moveseq=move(game)
	game.end_turn()
	return game
	pass
def generateonemove(parameter_list):
	pass
def play_turn(game: ".game.Game") -> ".game.Game":
	ittime=15
	while ittime>0:
		ittime-=1
		player = game.current_player
		input("s2")
		#if we are in choice state,we have to choice one  
		if player.choice:
			tar = random.choice(range(len(player.choice.cards)))
			usechoice(game,tar)
			changeflag=True
			continue
		heropower = player.hero.power
		cardset=[card for card in player.hand if card.is_playable()]
		charset=[character for character in player.characters if character.can_attack()]
		if heropower.is_usable():
			if heropower.requires_target():
				tar=random.choice(range(len(heropower.targets)))
				useheropower(game,tar)
				#heropower.use(target=random.choice(heropower.targets))
			else:
				useheropower(game)
				#heropower.use()
			continue

		# iterate over our hand and play whatever is playable
		
		print(cardset)
		#input("choosecard")
		if cardset:
			cardindex=random.choice(range(len(player.hand)))
			card=player.hand[cardindex]
			if card.is_playable():
				targetindex=-1
				mustchoice=-1
				if card.must_choose_one:
					mustchoice = random.choice(range(len(card.choose_cards)))
					card=card.choose_cards[mustchoice]
				if card.requires_target():
					if not card.targets:
						continue
					targetindex = random.choice(range(len(card.targets)))
				
				useplaycard(game,cardindex,mustchoice,targetindex)
				continue
		# Randomly attack with whatever can attack
		if charset:
			characterindex=random.choice(range(len(player.characters)))
			character=player.characters[characterindex]
			if character.can_attack():
				targetindex=random.choice(range(len(character.targets)))
				useattack(game,characterindex,targetindex)
				pass
			#input("s3")
			
			#input("s")
	#print(game_state_to_xml(game))
	game.end_turn()
	return game
def showgamestate(game):
	print(game.board)
	#print(game.decks)
	print(game.player1.hand)
	print(game.player2.hand)
	#print(game.hands)
	chas=game.characters
	for cha in chas:
		chasta=str(cha)+str(cha.atk)+' '+str(cha.health)
		chasta+=' '+str(cha.armor) if cha.type==CardType.HERO else ""
		print(chasta)
	print(str(getreward(game)))
	
	pass
def play_full_game() -> ".game.Game":
	game = setup_game()

	for player in game.players:
		print("Can mulligan %r" % (player.choice.cards))
		mull_count = random.randint(0, len(player.choice.cards))
		cards_to_mulligan = random.sample(player.choice.cards, mull_count)
		player.choice.choose(*cards_to_mulligan)
	t=0
	while True:
		with open('log','w+') as f:
			f.write("turnend"+str(t))
		showgamestate(game)
		input("Press Enter to continue...")
		t+=1
		game=play_turn(game)
		
		

	return game
