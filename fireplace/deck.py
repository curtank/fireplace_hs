from .utils import CardList


class Deck(CardList):
	MAX_CARDS = 30
	MAX_UNIQUE_CARDS = 2
	MAX_UNIQUE_LEGENDARIES = 1

	def __init__(self, cards=None):
		super().__init__(cards or [])
		self.hero = None

	def __repr__(self):
		return "<Deck (%i cards)>" % (len(self))
prepareddruiddeck=['Innervate',
'Innervate',
'Jade Idol',
'Jade Idol',
'Living Roots',
'Wild Growth',
'Wild Growth',
 'Wrath',
 'Wrath',
 'Feral Rage',
 'Feral Rage',
 'Jade Blossom',
 'Jade Blossom',
'Mulch',
 'Fandral Staghelm',
'Swipe',
'Swipe',
'Druid of the Claw',
'Druid of the Claw',
'Nourish',
'Nourish',
'Jade Behemoth',
'Jade Behemoth',
'Ancient of War',
'Jade Spirit',
'Jade Spirit',
'Azure Drake',
'Azure Drake',
'Aya Blackpaw',
  'Gadgetzan Auctioneer',]
preparedwarriordeck=['Upgrade!',
'Upgrade!',
'Fiery War Axe',
'Fiery War Axe',
 'Heroic Strike',
 'Heroic Strike',
 'Bloodsail Cultist',
 'Bloodsail Cultist',
'Frothing Berserker',
'Frothing Berserker',
'Kor\'kron Elite',
'Kor\'kron Elite',
'Mortal Strike',
'Mortal Strike',
'Arcanite Reaper',
'Arcanite Reaper',
 'Patches the Pirate',

'Sir Finley Mrrgglton',
 'Southsea Deckhand',
 'Southsea Deckhand',
'Bloodsail Raider',
'Bloodsail Raider',
'Southsea Captain',
'Southsea Captain',
'Dread Corsair',
'Dread Corsair',
'Naga Corsair',
'Leeroy Jenkins'

  ]