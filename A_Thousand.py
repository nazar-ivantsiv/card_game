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

min_bet = 100
last_bet = [0, min_bet] #[comp, user]

deck = [(c,s) for s in SUITS for c in CARDS]  #create DECK
shuffle(deck)	#shuffle DECK

comp_deck = [deck.pop() for i in range(10)]
user_deck = [deck.pop() for i in range(10)]
stock = [[deck.pop() for i in range(2)], [deck.pop() for i in range(2)]]


def count_score(user_cards, bias=0 , marriages=0):					#use bias to get ESTIMATE SCORE
	cards_count = {k:0 for k in SCORES.keys()}		#initialize keys

	if marriages:
		for c,s in user_cards:							#check for marriages
			if (c == 'K')and(('Q',s) in user_cards):
				cards_count[s+' marriage'] = 1

	for c,s in user_cards:
		cards_count[c] += 1	#...if the card is in user_cards

	score = sum([(cards_count.get(k,0) * v) for k,v in SCORES.items()])	#sum(qty * score)
	return score - bias

def print_cards(cards):
	for num,item in enumerate(cards):
		print('{}: {}'.format(num,item))

def print_bet(bet):
	print('COMP: {}'.format(bet[0]))
	print('YOU: {}'.format(bet[1]))

def bidding(last_bet, comp_score):
	#Initialize
	if last_bet[1] > 0:
		bet = [min_bet, 0]
	else: 
		bet = [0, min_bet]

	#Comps bet
	if (comp_score > bet[0]):
			bet = [(comp_score / 10)*10, 0]

	print_bet(bet)

	#Users bet
	user_input = int(raw_input('>>'))

	if user_input > bet[0]:
		bet = [0, user_input]

	return bet


def compare_cards(card1, card2, trump_suit):
	card1_score = count_score({card1})
	card2_score = count_score({card2})

	if trump_suit == '':	#No trump
		if card1_score > card2_score:
			return 0, card1_score
		else:
			return 1, card2_score
	else:
		if trump_suit in SUITS:
			if (card1[1] == trump_suit) and (card2[1] == trump_suit):
				if card1_score > card2_score:
					return 0, card1_score
				else:
					return 1, card2_score
			elif (card1[1] == trump_suit) and (card2[1] != trump_suit):
				return 0, card1_score
			else:
				return 1, card2_score	#0 or 1 - card idx, score

def get_max_card(deck, suit=0):
	if suit != 0:
		suit_deck = [i for i in deck if i[1] == suit]
	else:
		suit_deck = deck

	max_card = ['','']
	for item in suit_deck:
		if SCORES[max_card[0]] < SCORES[item[0]]:
			max_card = item

	return max_card

def get_min_card(deck, suit=0):
	if suit != 0:
		suit_deck = [i for i in deck if i[1] == suit]
	else:
		suit_deck = deck

	min_card = ['','']
	for item in suit_deck:
		if SCORES[min_card[0]] > SCORES[item[0]]:
			min_card = item

	return min_card

def comp_turn(comp_deck, trump_suit, user_card=0):
	if (user_card > 0):												#If on USERS turn
		if trump_suit > 0:											#Check for the MAX TRUMP
			comp_card = get_max_card(comp_deck, trump_suit)
			if comp_card == ['','']:										#No trumps in deck
				comp_card = get_min_card(comp_deck, user_card[1])	#Get MIN card matching user_suit
		else:
			comp_card = get_max_card(comp_deck, user_suit[1])		#Get MAX if no marriages were made
	else:															#If On COMPS turn
		if trump_suit > 0:											#Check for the MAX TRUMP
			comp_card = get_max_card(comp_deck, trump_suit)
			if comp_card == ['','']:										#No trumps in deck
				comp_card = get_max_card(comp_deck)					#Get MAX card
		else:
			comp_card = get_max_card(comp_deck)						#Get MAX card

	print('COMP turn: {}'.format(comp_card))
	return comp_card

def user_turn(user_deck):
	print_cards(user_deck)

	while True:
		user_card_idx = int(raw_input('YOUR turn (0-{}): '.format(len(user_deck)-1)))
		if (user_card_idx in range(len(user_deck))):
			break

	print(user_deck[user_card_idx])
	return user_deck[user_card_idx]

def sort_by_suit(deck):
	pass
	return 0

### BIDDING ###
print_cards(user_deck)

bias = 20
comp_score = count_score(comp_deck, bias, 1)

last_bet = bidding(last_bet, comp_score)
print('Last bet: %s' % last_bet)

#CONVERT sets to lists and SORT
comp_deck = list(comp_deck)
user_deck = list(user_deck)
comp_deck.sort()
user_deck.sort()
#####################

### DEALING CARDS ###
if last_bet[0]:
	comp_deck.extend(stock[randint(0,1)])	#Add stock to comp_deck
	comp_deck.pop()
	comp_deck.pop()						#Put two cards to remaining stock

else:
	stock_idx = int(raw_input('Choose your stock (0,1): '))
	user_deck.extend(stock[stock_idx])

	print_cards(user_deck)
	card_1 = int(raw_input('First card to pass (0-11): '))
	card_2 = int(raw_input('Second card to pass (0-11): '))

	user_deck.pop(card_1)
	user_deck.pop(card_2-1)
#####################

### GAMEPLAY ###
if last_bet[1] > 0:	#First is users turn
	turn = 1
else:
	turn = 0	#First is comps turn

trump_suit = ''  #['spades', 'clubs', 'diamonds', 'hearts']
score = {'user':0, 'comp':0}

while (user_deck != list()):
	print('--------------')
	if turn:	#Users turn
		user_card = user_turn(user_deck)
		comp_card = comp_turn(comp_deck, trump_suit, user_card)

		#Therer is marriage with current card
		if ((user_card[0] == 'K') and ( ('Q', user_card[1]) in user_deck)) \
			or( (user_card[0] == 'Q') and ( ('K', user_card[1]) in user_deck)):
			if (trump_suit != user_card[1]):
				trump_suit = user_card[1]
				print('YOUR trump: {}'.format(trump_suit))
				score['user'] += SCORES[trump_suit+' marriage']


		win, scr = compare_cards(user_card, comp_card, trump_suit)

		print(win, scr)

		if win:
			score['user'] += scr
			turn = 1
		else:
			score['comp'] + scr
			turn = 0

		user_deck.remove(user_card)
		comp_deck.remove(comp_card)

	else:		#Comps turn
		comp_card = comp_turn(comp_deck, trump_suit)
		user_card = user_turn(user_deck)

		#Therer is marriage with current card
		if ((comp_card[0] == 'K') and ( ('Q', comp_card[1]) in comp_deck)) \
			or( (comp_card[0] == 'Q') and ( ('K', comp_card[1]) in comp_deck)):
			if (trump_suit != comp_card[1]):
				trump_suit = comp_card[1]
				print('COMP trump: {}'.format(trump_suit))
				score['comp'] += SCORES[trump_suit+' marriage']


		win, scr = compare_cards(user_card, comp_card, trump_suit)

		print(win, scr)

		if win:
			score['user'] += scr
			turn = 1
		else:
			score['comp'] + scr
			turn = 0

		user_deck.remove(user_card)
		comp_deck.remove(comp_card)

else:
	#+ marriages!
	for k,v in score.items():	#Calculate scores
		print('{}: {}'.format(k,v))

################
'''
TODO:
- Comp AI
- 
- Add marriage score only if user wins
- Sort cards by suit
- Bidding with 5 or 10 points increase
'''