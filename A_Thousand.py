from random import shuffle, randint

CARDS = {'9','J','Q','K','10','A'}
SUITS = {'spades', 'clubs', 'diamonds', 'hearts'}
SCORES = {'9':0,
		  'J':2,
		  'Q':3,
		  'K':4,
		  '10':10,
		  'A':11,
		  'spades marriage':40,
		  'clubs marriage':60,
		  'diamonds marriage':80,
		  'hearts marriage':100,
		  }

MIN_BET = 100
WINNING_SCORE = 1000

def count_score(user_cards, minus=0 , marriages=0):					#substract minus to get ESTIMATE SCORE
	cards_count = {k:0 for k in SCORES.keys()}		#initialize keys

	if marriages:
		for c,s in user_cards:							#check for marriages
			if (c == 'K')and(('Q',s) in user_cards):
				cards_count[s+' marriage'] = 1

	for c,s in user_cards:
		cards_count[c] += 1	#...if the card is in user_cards

	score = sum([(cards_count.get(k,0) * v) for k,v in SCORES.items()])	#sum(qty * score)
	return score - minus

def print_cards(cards):
	for num,item in enumerate(cards):
		print('{}: {}'.format(num,item))

def print_bet(bet):
	print('COMP: {}'.format(bet['comp']))
	print('YOU: {}'.format(bet['user']))

def bidding(last_bet, comp_estimate):
	increment = 10
	#Initialize
	if last_bet['user'] > 0:
		bet = {'user':0, 'comp': MIN_BET}
	else: 
		bet = {'user': MIN_BET, 'comp': 0}

	comp_max_bet = (comp_estimate / 10)*10
	if comp_max_bet < MIN_BET: comp_max_bet = MIN_BET 
	#print(comp_max_bet)

	while True:
		print_bet(bet)
		if bet['comp'] >= bet['user']:
			try:
				user_input = int(raw_input('BET (\'0\'to PASS):'))
			except ValueError:
				continue
			user_input = int(round(user_input,-1))	# Round if user entered not divisible by 10
			if user_input == 0:						# User PASS
				bet['user'] = 0
				bet['comp'] = comp_max_bet			# Set Comps bet to MAX
				break
			elif user_input <= bet['comp']:			# User entered lower than comp bet
				continue
			else:
				bet['user'] = user_input		 	# Remember Users bet (round to 10)
		elif (bet['user'] + 10) <= comp_max_bet:	# If Comp can give +10 more than user - GO
			bet['comp'] = bet['user'] + 10			# Comp bids +10
		else:
			bet['comp'] = 0							# Comp PASS
			break

	return bet


def compare_cards(card1, card2, trump_suit, turn):
	card1_score = count_score({card1})
	card2_score = count_score({card2})
			
	if card1[1] != card2[1]:						# Suits are DIFFERENT -> check if trump -> compare
		if (trump_suit in SUITS) and ((card1[1] == trump_suit) or (card2[1] == trump_suit)):						# Trump specified
			if (card1[1] == trump_suit) and (card2[1] == trump_suit):
				if card1_score > card2_score:
					return 0, card1_score
			elif (card1[1] == trump_suit) and (card2[1] != trump_suit):
				return 0, card1_score
			elif (card1[1] != trump_suit) and (card2[1] == trump_suit):
				return 1, card2_score
		else:										# Suits are different, no trump in cards -> wins TURN
			return turn, [card1_score, card2_score][turn]
	else:											# Suits are the SAME
		if card1_score > card2_score:
			return 0, card1_score
		else:
			return 1, card2_score

def get_min_card(deck, suit=''):
	if suit != '':
		suit_deck = [i for i in deck if i[1] == suit]
	else:
		suit_deck = deck

	if suit_deck != []:
		min_card = suit_deck[0]
		for item in suit_deck:
			if SCORES[min_card[0]] > SCORES[item[0]]:
				min_card = item
		return min_card
	else:
		return get_min_card(deck)

def get_max_card(deck, suit=''):
	if suit != '':
		suit_deck = [i for i in deck if i[1] == suit]
	else:
		suit_deck = deck

	if suit_deck != []:
		max_card = suit_deck[0]
		for item in suit_deck:
			if SCORES[max_card[0]] < SCORES[item[0]]:
				max_card = item
		return max_card
	else:
		return get_min_card(deck)				# If there are no cards of current suit

def comp_turn(comp_deck, trump_suit, user_card=0):
	if (user_card > 0):												#If on USERS turn
		if trump_suit != '':										#Check for the MAX TRUMP
			comp_card = get_max_card(comp_deck, trump_suit)
			if comp_card == 0:										#No trumps in deck
				comp_card = get_min_card(comp_deck, user_card[1])	#Get MIN card matching user_suit
		else:
			comp_card = get_min_card(comp_deck, user_card[1])		#Give MIN to user if no marriages were made
	else:															#If On COMPS turn
		if trump_suit != '':										#Check for the MAX TRUMP
			comp_card = get_max_card(comp_deck, trump_suit)
			if comp_card == 0:										#No trumps in deck
				comp_card = get_max_card(comp_deck)					#Get MAX card
		else:
			comp_card = get_max_card(comp_deck)						#Get MAX card

	print('COMP turn: {}\n'.format(comp_card))
	return comp_card

def user_turn(user_deck):
	print_cards(user_deck)

	while True:
		try:
			user_card_idx = int(raw_input('YOUR turn (0-{}): '.format(len(user_deck)-1)))
		except ValueError:
			continue
		if (user_card_idx in range(len(user_deck))):
			break

	print(user_deck[user_card_idx])
	return user_deck[user_card_idx]

def sort_by_suit(deck):
	sorted_deck = []
	for suit in SUITS:
		for item in deck:
			if item[1] == suit:
				sorted_deck.append(item)
	return sorted_deck

last_bet = {'user':MIN_BET, 'comp':0}
global_score = {'user':0, 'comp':0}

while True:

	### DEALING CARDS ###
	deck = [(c,s) for s in SUITS for c in CARDS]  #create DECK
	shuffle(deck)	#shuffle DECK

	comp_deck = [deck.pop() for i in range(10)]
	user_deck = [deck.pop() for i in range(10)]
	stock = [[deck.pop() for i in range(2)], [deck.pop() for i in range(2)]]

	#print('__comp cards:')
	#print_cards(sort_by_suit(comp_deck))
	#######################

	### BIDDING ###
	#print(chr(27) + "[2J")												# Cls Scr
	print('\n')
	print('Your cards:')
	print_cards(sort_by_suit(user_deck))

	minus = 20
	comp_score = count_score(comp_deck, minus, 1)

	last_bet = bidding(last_bet, comp_score)
	print('Last bet: %s' % last_bet)

	#SORT by name & by suit
	user_deck.sort()
	user_deck = sort_by_suit(user_deck)
	#####################

	### DEALING STOCK ###
	if last_bet['user']:
		while True:
			try:
				stock_idx = int(raw_input('Choose your stock (0,1): '))
				break
			except ValueError:
				continue

		user_deck.extend(stock[stock_idx])
		# Sort by suit for better appearance
		user_deck = sort_by_suit(user_deck)								#Sort again after adding stock

		print_cards(user_deck)
		while True:
			try:
				card_1 = int(raw_input('First card to pass (0-11): '))
				card_2 = int(raw_input('Second card to pass (0-11): '))
				break
			except ValueError:
				continue
		user_deck.pop(card_1)
		if card_1 < card_2 :
			user_deck.pop(card_2-1)
		else:
			user_deck.pop(card_2)
	else:
		comp_deck.extend(stock[randint(0,1)])							# Add stock to comp_deck
		comp_deck.remove(get_min_card(comp_deck))
		comp_deck.remove(get_min_card(comp_deck))						# Take two cards out of deck (to remaining stock)

	#####################

	### GAMEPLAY ###
	if last_bet['user'] > 0:	#First is users turn
		turn = 1
	else:
		turn = 0	#First is comps turn

	trump_suit = ''  #['spades', 'clubs', 'diamonds', 'hearts']

	trick = {'user':set(), 'comp':set()}
	score = {'user':0, 'comp':0}

	while (user_deck != list()):
		print('--------------')

		if turn:	#Users turn
			user_card = user_turn(user_deck)
			#Therer is marriage with current card
			if ((user_card[0] == 'K') and ( ('Q', user_card[1]) in user_deck)) \
				or( (user_card[0] == 'Q') and ( ('K', user_card[1]) in user_deck)):
				if (trump_suit != user_card[1]):
					trump_suit = user_card[1]
					print('YOUR trump: {}'.format(trump_suit))
					score['user'] += SCORES[trump_suit+' marriage']

			comp_card = comp_turn(comp_deck, trump_suit, user_card)

			win, scr = compare_cards(comp_card, user_card, trump_suit, turn)

			if win:
				trick['user'].add(user_card)
				trick['user'].add(comp_card)
				turn = 1
			else:
				turn = 0

		else:		#Comps turn
			comp_card = comp_turn(comp_deck, trump_suit)
			#Therer is marriage with current card
			if ((comp_card[0] == 'K') and ( ('Q', comp_card[1]) in comp_deck)) \
				or( (comp_card[0] == 'Q') and ( ('K', comp_card[1]) in comp_deck)):
				if (trump_suit != comp_card[1]):
					trump_suit = comp_card[1]
					print('COMP trump: {}'.format(trump_suit))
					score['comp'] += SCORES[trump_suit+' marriage']

			user_card = user_turn(user_deck)

			win, scr = compare_cards(comp_card, user_card, trump_suit, turn)

			if win:
				turn = 1
			else:
				trick['comp'].add(comp_card)
				trick['comp'].add(user_card)
				turn = 0


		user_deck.remove(user_card)
		comp_deck.remove(comp_card)

	else:
		# Calculate scores
		for k,v in trick.items():
			score[k] += count_score(v)	# Add card score (in trick) to marriages score

		print(score)
		print(trick['user'])
		print(trick['comp'])


		if (last_bet['user'] > 0):
			if (last_bet['user'] > score['user']):	# User didn't reach the BET (add negative score)
				score['user'] = -last_bet['user']
			else:
				score['user'] = last_bet['user']	# User has reached the BET (give him the BET score)
		elif (last_bet['comp'] > 0):
			if (last_bet['comp'] > score['comp']):
				score['comp'] = -last_bet['comp']	# Comp didn't reach the BET (add negative score)
			else:
				score['comp'] = last_bet['comp']	# Comp has reached the BET (give him the BET score)


		print('####################\n')
		print('USER: {}'.format(score['user']))
		print('COMP: {}'.format(score['comp']))
		print('\n####################')
		raw_input('Press ENTER to go to the next game...')
		print('NEXT GAME:')
	################

	global_score['user'] += score['user']
	global_score['comp'] += score['comp']

	print('GLOBAL SCORE: User: {} | Comp: {}'.format(global_score['user'],global_score['comp']))

	if global_score['user'] >= WINNING_SCORE:
		if global_score['comp'] != WINNING_SCORE:
			print('*** YOU WIN! ***')
		else:
			print('*** DRAW ***')
		break
	elif global_score['comp'] >= WINNING_SCORE:
		print('*** COMP WIN! ***')


'''
TODO:
- Add possibility to recalculate bid after getting STOCK (user & comp)
- Check if user uses a correct card
- lower comp_max_score if there are no Aces (only marriages)
- Check for 4 x'9' in the deck and shuffle again
- 
- 
- DONE. Sort cards by suit
- DONE. Where does Comp miss some cards???
- DONE. Add user $ comp tricks (win pairs)
- DONE. Add marriage score only if user wins
- DONE. Bidding with 5 or 10 points increase
'''