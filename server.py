## simplified server for http://meta.codegolf.stackexchange.com/a/1332/16472
## wish me luck

HOST="0.0.0.0"
PORT=31337

VISUALIZERHOST="0.0.0.0"
VISUALIZERPORT=12003

SIZE=1024  ## side length
LENGTH=3000 # round time in seconds
## on the board: 0 = off, 1 = player1, 2 = player2, 3 = neither??

import os,sys
import random
import socket
import time

class GameError:
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def getcell(board,x,y):
	# returns 0 if off the board
	if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
		return 0
	return board[x][y]

"""
# these ones use hex... oops

def sendtlv(sock,tid,tstr):
	s = "{:02x}{:02x}".format(ord(tid),len(tstr)).upper() + "".join("{:02x}".format(ord(c)).upper() for c in tstr)
	sock.sendall(s)

def gettlv(tlv):
	tid = chr(int(tlv[0:2],16))
	leng = int(tlv[2:4],16)
	if not leng = len(tlv[4:]):
		raise GameError("tlv length doesn't match")
	text = ''.join(chr(int(tlv[i:i+2],16)) for i in range(4,len(tlv),2))
	return tid,text

def getmoves(tlv):
	leng = int(tlv[2:4],16)
	if not leng = len(tlv[4:]):
		raise GameError("tlv move length doesn't match")
	movs = [(int(tlv[i:i+4],16),int(tlv[i+4:i+8],16)) for i in range(4,len(tlv),8)]
	return movs
"""

def sendtlv(sock,tid,tstr):
	s = "{}{}".format(tid,chr(len(tstr))) + tstr
	sock.sendall(s)

def gettlv(tlv):
	tid = tlv[0]
	leng = ord(tlv[1])
	if not leng = len(tlv[2:]):
		raise GameError("tlv length doesn't match")
	text = tlv[2:]
	return tid,text

def getmoves(tlv):
	leng = ord(tlv[1])
	if not leng = len(tlv[2:]):
		raise GameError("tlv move length doesn't match")
	movs = [(ord(tlv[i]) + 256*ord(tlv[i+1]),ord(tlv[i+2]) + 256*ord(tlv[i+3])) for i in range(2,len(tlv),4)]
	return movs

def iterlife(board):
	newboard = [[0 for i in range(SIZE)] for i in range(SIZE)]
	for x in range(SIZE):
		for y in range(SIZE):
			p1neighbors = sum([1 if c==1 else 0 for c in [board[x-1][y-1],board[x][y-1],board[x+1][y-1],board[x-1][y],board[x+1][y],board[x-1][y+1],board[x][y+1],board[x+1][y+1]]])
			p2neighbors = sum([1 if c==2 else 0 for c in [board[x-1][y-1],board[x][y-1],board[x+1][y-1],board[x-1][y],board[x+1][y],board[x-1][y+1],board[x][y+1],board[x+1][y+1]]])
			if board[x][y] == 0:
				if p1neighbors == 3 and p2neighbors == 0:
					newboard[x][y] = 1
				if p2neighbors == 3 and p1neighbors == 0:
					newboard[x][y] = 2
			elif board[x][y] == 1:
				if p1neighbors < 2 or p1neighbors > 3:
					newboard[x][y] = 0
				if p1neighbors == 2 or p1neighbors == 3:
					newboard[x][y] = 1
			elif board[x][y] == 2:
				if p2neighbors < 2 or p2neighbors > 3:
					newboard[x][y] = 0
				if p2neighbors == 2 or p2neighbors == 3:
					newboard[x][y] = 1
	return newboard

def countcells(board):
	p1cells = 0
	p2cells = 0
	for i in board:
		for c in i:
			if c == 1:
				p1cells+=1
			elif c == 2:
				p2cells+=1
	return p1cells,p2cells

def rungame(opp1,opp2):
	# set up variables
	# here we swap the two sockets at random:
	if random.random() > 0.5:
		temp = opp1
		opp1 = opp2
		opp2 = temp
		del temp
	time.sleep(1)
	i,p1name = gettlv(opp1.recv(1024))
	if not i == 'I':
		raise GameError("player 1 didn't identify properly")
	i,p2name = gettlv(opp2.recv(1024))
	if not i == 'I':
		raise GameError("player 2 didn't identify properly")
	board = [[0 for i in range(SIZE)] for i in range(SIZE)]
	playing = True ## no win conditions that i've seen
	p1score = 0
	p2score = 0
	rounds = 0
	starttime = time.time()
	print "variables set up"
	print "now starting {} vs. {}".format(p1name,p2name)
	sendtlv(opp1,'S',p2name)
	sendtlv(opp2,'S',p1name)
	while playing:
		board = iterlife(board)
		sendtlv(opp1,'G','')
		sendtlv(opp2,'G','')
		# count up cells
		p1score,p2score = countcells(board)
		'''if p1score == 0 or p2score == 0:  # not sure if needed
			print "player 1 ran out of cells" if p1score == 0 else "player 2 ran out of cells"
			playing = False
			break'''
		if time.time() > starttime + LENGTH:
			playing = False
			break
		# opp1 moves
		sendtlv(opp1,'T','')
		#time.sleep(2) # there's probably a better way to wait for a valid packet
		mv = opp1.recv(2048)
		i,t = gettlv(mv)
		if not i == 'M':
			raise GameError("opponent 1 didn't send a Move")
		moves = getmoves(mv)
		print "opponent 1 sent " + repr(moves)
		if len(moves) > 30:
			raise GameError("opponent 1 passed too many moves")
		opp2.sendall(mv) # should be the exact same format that it expects
		for i in moves:
			if board[i[0]][i[1]] == 0:
				board[i[0]][i[1]] = 1
		# opp2 moves
		sendtlv(opp2,'T','')
		#time.sleep(2) # there's probably a better way to wait for a valid packet
		mv = opp2.recv(2048)
		i,t = gettlv(mv)
		if not i == 'M':
			raise GameError("opponent 2 didn't send a move")
		moves = getmoves(mv)
		print "opponent 2 sent " + repr(moves)
		if len(moves) > 30:
			raise GameError("opponent 2 passed too many moves")
		opp1.sendall(mv) # should be the exact same format that it expects
		for i in moves:
			if board[i[0]][i[1]] == 0:
				board[i[0]][i[1]] = 2
	print "game finished"
	print "p1 cells left: {}, p2 cells left: {}".format(p1score,p2score)
	## figure out who won
	win = 0
	if p1score > p2score:
		win = 1
		print "player 1 ({}) won!".format(p1name)
	elif p2score > p1score:
		win = 2
		print "player 1 ({}) won!".format(p1name)
	else:
		win = -1
		print "there was a tie"
	## now to store the data. i'm thinking sqlite3


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(2)
	print "socket init complete"
	while True:
		a,addr = s.accept()
		print "accepted connection from " + addr + " (1/2)"
		b,addr = s.accept()
		print "accepted connection from " + addr + " (2/2)"
		print "starting..."
		rungame(a,b)

if __name__ == "__main__":
	main()
