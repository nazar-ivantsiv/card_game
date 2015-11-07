#! /usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
from random import randint

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

class Deck(list):

	TRUMP_SUIT = 0

	def __init__(self, player_name, cards=0, is_main_deck=0):
		'''
		player_name - the NAME
		cards - CARDS to put into current instance of Deck
		is_main_deck - if created instance of class is the MAIN deck
		'''
		self.name = player_name
		self.is_main_deck = is_main_deck
		self.trick = set()
		self.marriage_score = 0

		if self.is_main_deck:
			self.extend([(c,s) for s in SUITS for c in CARDS])
		elif cards:
			self.extend(cards)
		else:
			pass	# Leave Deck an empty list


	def shuffle_deck(self):
		shuffle(self)

	def give_cards(self, qty=10):
		return [self.pop() for i in range(qty)]

	def count_score(self, minus=0 , check_for_marriages=0):		#substract minus to get ESTIMATE SCORE to bit
		cards_count = {k:0 for k in SCORES.keys()}		#initialize keys

		if check_for_marriages:
			for c,s in self:							#check for marriages
				if (c == 'K')and(('Q',s) in self):
					cards_count[s+' marriage'] = 1

		for c,s in self:
			cards_count[c] += 1	#...if the card is in user_cards

		for c,s in self.trick:
			cards_count[c] += 1	#...if the card is in user_cards

		score = sum([(cards_count.get(k,0) * v) for k,v in SCORES.items()])	#sum(qty * score)
		return score + self.marriage_score - minus

	def print_cards(self):
		if Deck.TRUMP_SUIT != 0:
			print('### Current trump: {} ###'.format(Deck.TRUMP_SUIT))

		for num,item in enumerate(self):
			print('{}: {}'.format(num,item))

	def sort_by_suit(self):
		def get_key(item):	# Sort by SECOND key of item
			return item[1]
		self.sort(key=get_key)

	def has_marriage(self, card):
		#Therer is marriage with current card
		if ((card[0] == 'K') and ( ('Q', card[1]) in self)) \
			or( (card[0] == 'Q') and ( ('K', card[1]) in self)):
			if (self.TRUMP_SUIT != card[1]):
				Deck.TRUMP_SUIT = card[1]	# Change TRUMP for all instances
				print('### NEW trump is: {} ###'.format(self.TRUMP_SUIT))
				self.marriage_score += SCORES[self.TRUMP_SUIT+' marriage']

	def get_min_card(self, suit=0):
		if suit != 0:
			suit_deck = [i for i in self if i[1] == suit]
		else:
			suit_deck = self

		if suit_deck != []:
			min_card = suit_deck[0]
			for item in suit_deck:
				if SCORES[min_card[0]] > SCORES[item[0]]:
					min_card = item
			return min_card
		else:
			return self.get_min_card()

	def get_max_card(self, suit=0):
		if suit != 0:
			suit_deck = [i for i in self if i[1] == suit]
		else:
			suit_deck = self

		if suit_deck != []:
			max_card = suit_deck[0]
			for item in suit_deck:
				if SCORES[max_card[0]] < SCORES[item[0]]:
					max_card = item
			return max_card
		else:
			return self.get_min_card()			# If there are no cards of current suit

	def make_turn(self, user_card=0):
		if self.name == 'user':
			self.print_cards()

			while True:
				try:
					user_card_idx = int(raw_input( 'YOUR turn (0-{}): '
													''.format(len(self)-1) 
													))
				except ValueError:
					continue
				if (user_card_idx in range(len(self))):
					break

			card = self[user_card_idx]
			print('YOUR turn: {}\n'.format(card))
			return card

		elif self.name == 'comp':
			if (user_card > 0):											#If on USERS turn
				if self.TRUMP_SUIT != 0:								#Check for the MAX TRUMP
					comp_card = self.get_max_card(self.TRUMP_SUIT)
					if comp_card == 0:									#No trumps in deck
						comp_card = self.get_min_card(user_card[1])	#Get MIN card matching user_suit
				else:
					comp_card = self.get_min_card(user_card[1])		#Give MIN to user if no marriages were made
			else:														#If On COMPS turn
				if self.TRUMP_SUIT != 0:								#Check for the MAX TRUMP
					comp_card = self.get_max_card(self.TRUMP_SUIT)
					if comp_card == 0:									#No trumps in deck
						comp_card = self.get_max_card()					#Get MAX card
				else:
					comp_card = self.get_max_card()						#Get MAX card

			print('COMP turn: {}\n'.format(comp_card))
			return comp_card

################################################################################

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
		elif (bet['user'] + increment) <= comp_max_bet:	# If Comp can give +10 more than user - GO
			bet['comp'] = bet['user'] + increment			# Comp bids +10
		else:
			bet['comp'] = 0							# Comp PASS
			break

	return bet

def compare_cards(card1, card2, turn):

	card1_score = SCORES[card1[0]]
	card2_score = SCORES[card2[0]]
			
	if card1[1] != card2[1]:						# Suits are DIFFERENT -> check if trump -> compare
		if (Deck.TRUMP_SUIT in SUITS) and ((card1[1] == Deck.TRUMP_SUIT) or \
							(card2[1] == Deck.TRUMP_SUIT)):						# Trump specified
			if (card1[1] == Deck.TRUMP_SUIT) and (card2[1] == Deck.TRUMP_SUIT):
				if card1_score > card2_score:
					return 0, card1_score
			elif (card1[1] == Deck.TRUMP_SUIT) and (card2[1] != Deck.TRUMP_SUIT):
				return 0, card1_score
			elif (card1[1] != Deck.TRUMP_SUIT) and (card2[1] == Deck.TRUMP_SUIT):
				return 1, card2_score
		else:										# Suits are different, no trump in cards -> wins TURN
			return turn, [card1_score, card2_score][turn]
	else:											# Suits are the SAME
		if card1_score > card2_score:
			return 0, card1_score
		else:
			return 1, card2_score

last_bet = {'user':MIN_BET, 'comp':0}
global_score = {'user':0, 'comp':0}

while True:

	### DEALING CARDS ###
	deck = Deck('main',0,1)
	deck.shuffle_deck()
	#	Init comp & user DECKS (cards)
	comp_deck = Deck('comp')
	user_deck = Deck('user')

	comp_deck.extend(deck.give_cards(10))
	user_deck.extend(deck.give_cards(10))

	#	Init two stocks to choose from
	stock = deck.give_cards(2), deck.give_cards(2)

	print('\n')
	print('Your cards:')
	user_deck.sort_by_suit()
	user_deck.print_cards()

	minus = 20
	comp_score = comp_deck.count_score(minus, 1)	# comp estimate SCORE

	last_bet = bidding(last_bet, comp_score)
	print('Last bet: %s' % last_bet)

	#SORT by name & by suit
	user_deck.sort()
	user_deck.sort_by_suit()
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
		#	Sort by suit for better appearance
		user_deck.sort()
		user_deck.sort_by_suit()

		user_deck.print_cards()
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
		comp_deck.remove(comp_deck.get_min_card())
		comp_deck.remove(comp_deck.get_min_card())						# Take two cards out of deck (to remaining stock)

	#####################

	### GAMEPLAY ###
	if last_bet['user'] > 0:	#First is users turn
		turn = 1
	else:
		turn = 0	#First is comps turn
		user_card = 0	# NO user turn

	while (user_deck != list()):
		print('\n')
		print('-' * 30)

		if turn:	#Users turn
			user_card = user_deck.make_turn()

			comp_card = comp_deck.make_turn(user_card)

			win, scr = compare_cards(comp_card, user_card, turn)

			if win:
				user_deck.has_marriage(user_card)	# Checks for marriage with current card
				user_deck.trick.add(user_card)
				user_deck.trick.add(comp_card)
				turn = 1
			else:
				turn = 0

		else:		#Comps turn
			comp_card = comp_deck.make_turn(user_card)

			user_card = user_deck.make_turn()

			win, scr = compare_cards(comp_card, user_card, turn)

			if win:
				turn = 1
			else:
				comp_deck.has_marriage(comp_card)	# Checks for marriage with current card
				comp_deck.trick.add(comp_card)
				comp_deck.trick.add(user_card)
				turn = 0

		print('{} wins'.format(['comp','user'][turn]))
		user_deck.remove(user_card)
		comp_deck.remove(comp_card)

	else:
		Deck.TRUMP_SUIT = 0

		# Calculate scores
		user_score = user_deck.count_score()
		comp_score = comp_deck.count_score()
		#print(user_deck.trick)
		#print(comp_deck.trick)


		if (last_bet['user'] > 0):
			if (last_bet['user'] > user_score):	# User didn't reach the BET (add negative score)
				user_score = -last_bet['user']
			else:
				user_score = last_bet['user']	# User has reached the BET (give him the BET score)
		elif (last_bet['comp'] > 0):
			if (last_bet['comp'] > comp_score):
				comp_score = -last_bet['comp']	# Comp didn't reach the BET (add negative score)
			else:
				comp_score = last_bet['comp']	# Comp has reached the BET (give him the BET score)


		print('####################\n')
		print('USER: {}'.format(user_score))
		print('COMP: {}'.format(comp_score))
		print('\n####################')
		raw_input('Press ENTER to go to the next game...')
		print('NEXT GAME:')
	################

	global_score['user'] += user_score
	global_score['comp'] += comp_score

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
'''