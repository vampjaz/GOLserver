## simplified server for http://meta.codegolf.stackexchange.com/a/1332/16472
## wish me luck

HOST="0.0.0.0"
PORT=31337

SIZE=1024  ## side length
## on the board: 0 = off, 1 = player1, 2 = player2, 3 = neither??

import os,sys
import random
import socket

def getcell(board,x,y):
	# returns 0 if off the board
	if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
		return 0
	return board[x][y]

def sendtlv(sock,tid,tstr):
	s = "{:02x}{:02x}".format(ord(tid),len(tstr)).upper() + "".join("{:02x}".format(ord(c)).upper() for c in tstr)
	sock.sendall(s)

def gettlv(tlv):
	tid = chr(int(tlv[0:2],16))
	leng = int(tlv[2:4],16)
	text = ''.join(chr(int(tlv[i:i+2],16)) for i in range(4,4+leng*2,2))
	return tid,text

def getmoves(tlv):
	leng = int(tlv[2:4],16)
	movs = [(int(tlv[i:i+4],16),int(tlv[i+4:i+8],16)) for i in range(4,4+leng*2,8)]
	return movs

def rungame(opp1,opp2):
	# set up variables
	board = [[0 for i in range(SIZE)] for i in range(SIZE)]
	playing = True ## no win conditions that i've seen
	p1score = 0
	p2score = 0
	while playing:
		pass ## tbd



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
