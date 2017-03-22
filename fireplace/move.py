def choosebestmove(gamenews):
	max=float("-inf")
	for gamenew in gamenews:
		reward=getreward(gamenew)
		if max<reward:
			max=reward
			game=gamenew
	return game
def iterto(list,i):
	t=None
	for j in range(i):
		t=list.next()
		pass
	return t
	pass
def heropowermove(game,herpower_already_targetting=False,
		herpower_target=-1):
	gamenew=copy.deepcopy(game)
	player = gamenew.current_player
	heropower = player.hero.power
	if heropower.is_usable():
		if heropower.requires_target():
			if herpower_already_targetting:
				targets=gamenew.current_player.hero.power.targets
				target=target[herpower_target]
				#print(target)
				heropower.use(target=target)
				#gamenews.append(move(gamenew))
				
				pass
			else:
				for i in range(len(heropower.targets)):
					gamenews.append(heropowermove(gamenew,herpower_already_targetting=True,herpower_target=i))
				pass
		else:
			heropower=gamenew.current_player.hero.power
			heropower.use()
		gamenews.append(move(gamenew))
	game=choosebestmove(game)
	return game
	pass
def playcardmove(game,alreadychoosecard=False,
		choosedcard=-1,
		alreadymustchoose=False,
		mustchoose=-1,
		choosetarget=False,
		target=-1):
	gamenews=[]
	gamenew=copy.deepcopy(game)
	gamenews.append(gamenew)
	player = gamenew.current_player
	if alreadychoosecard:
		card=player.hand[choosedcard]
		if card.is_playable():
			#target = None
			if card.must_choose_one:
				showgamestate(gamenew)
				input("must choose happen")
				card=random.choice(card.choosecards)
			tar=None
			if card.requires_target():
				if choosetarget:
					tar = card.targets[target]

					pass
				else:
					for i in range(len(card.targets)):
						gamenews.append(playcardmove(gamenew,alreadychoosecard=True,choosedcard=choosedcard,choosetarget=True,target=i))
					pass
				pass
			card.play(target=tar)
			if player.choice:
				showgamestate(gamenew)
				input("playerchoice")
				choice = random.choice(player.choice.cards)
				
				player.choice.choose(choice)
				#gamenews.append(move(gamenew))
				#choicenum+=1
				#print("Choosing card %r" % (choice))
				
			gamenews.append(gamenew)
			#stopatthismove
			gamenews.append(move(game))
			pass

		pass
	else:
		for i in range(len(player.hand)):
			gamenews.append(playcardmove(gamenew,alreadychoosecard=True,choosedcard=i))
			pass
		pass
	return choosebestmove(game)

	pass
def playerchoice(game,playerdecided=False,playerchoice=-1):
	import copy
	gamenews=[]
	gamenew=copy.deepcopy(game)
	player=gamenew.current_player
	
	if player.choice:
		if playerdecided:
			player.choice.choose(playerchoice)
		else:
			for i in range(len(player.choice.cards)):
				gamenews.append(playerchoice(game,playerdecided=True,playerchoice=i)
		gamenews.append(gamenew)
	return(choosebestmove(gamenews))

def move(game,
		herpower_already_targetting=False,
		herpower_target=-1,
		alreadychoosecard=False,
		choosedcard=-1,
		alreadymustchoose=False,
		mustchoose=-1,
		):
	import copy
	gamenews=[]
	gamenews.append(heropowermove(game))
	gamenews.append(playcardmove(game))
	return choosebestmove(gamenews)
	
	
	
	

	
	

def moveold(game: ".game.Game") -> ".game.Game":
	import copy
	gamenews=[]
	#gamenew=copy.deepcopy(game)
	player = game.current_player
	
	heropower = player.hero.power
	if heropower.is_usable():
		if heropower.requires_target():
			for i in range(len(heropower.targets)):
				gamenew=copy.deepcopy(game)
				targets=gamenew.current_player.hero.power.targets
				target=iterto(targets,i)
				#print(target)
				heropower.use(target=target)
				gamenews.append(move(gamenew))
		else:
			gamenew=copy.deepcopy(game)
			heropower=gamenew.current_player.hero.power
			heropower.use()
			gamenews.append(move(gamenew))
			
	
		iterate over our hand and play whatever is playable
		for card in player.hand:
			if card.is_playable() and random.random() < 0.5:
				target = None
				if card.must_choose_one:
					card = random.choice(card.choose_cards)
				if card.requires_target():
					target = random.choice(card.targets)
				print("Playing %r on %r" % (card, target))
				card.play(target=target)

				if player.choice:
					choice = random.choice(player.choice.cards)
					print("Choosing card %r" % (choice))
					player.choice.choose(choice)
				break
				gamenews.append(move(gamenew))

			continue
			
		 Randomly attack with whatever can attack
	gamenew=copy.deepcopy(game)
	for character in player.characters:
		
		if character.can_attack():
			gamenew=copy.deepcopy(game)
			character.attack(random.choice(character.targets))
			gamenews.append(move(gamenew))

		break

	cardnum=0
	for card in player.hand:
		
		if card.is_playable():
			target = None
			if card.must_choose_one:
				card = random.choice(card.choose_cards)
			if card.requires_target():
				targetnum=0
				for target in card.targets:
					gamenew=copy.deepcopy(game)
					player = game.current_player
					cardnew=player.hand[cardnum]
					target = cardnew.targets[targetnum]
					
					#print("Playing %r on %r" % (card, target))
					card.play(target=target)
					gamenews.append(move(gamenew))
					targetnum+=1

			if player.choice:
				#choice = random.choice(player.choice.cards)
				choicenum=0
				for card in player.choice.cards:
					gamenew=copy.deepcopy(game)
					player = game.current_player
					choice= player.choice.cards[choicenum]
					with open('outforplaycard','a') as f:
						f.write("Playing %r on %r" % (card, target))
					#print("Playing %r on %r" % (card, target)
					player.choice.choose(choice)
					gamenews.append(move(gamenew))
					choicenum+=1
					pass
				#print("Choosing card %r" % (choice))
				
			break
			#gamenews.append(move(gamenew))
		cardnum+=1
		
	charindex=0
	for character in player.characters:
		#character=player.characters[charindex]
		if character.can_attack():
			targetindex=0
			for target in character.targets:
				gamenew=copy.deepcopy(game)

				#player = gamenew.current_player
				charactersnew=gamenew.current_player.characters
				cha=charactersnew[charindex]
				tar=cha.targets[targetindex]
				cha.attack(tar)
				gamenews.append(move(gamenew))
				targetindex+=1
		charindex+=1
		

	#do nothing
	gamenews.append(game)
	
	max=float("-inf")
	for gamenew in gamenews:
		reward=getreward(gamenew)
		if max<reward:
			max=reward
			game=gamenew
			
			pass
	
	#game=random.choice(gamenews)
	showgamestate(game)
	input("press Enter")
	
	#gamenews.append(gamenew)
	