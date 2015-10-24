## this program visualizes the game of life board in real time
## ideally the server and this will connect, and the server will pass on all the "Move" messages transparently

board = []

def getmoves(tlv):
    leng = int(tlv[2:4],16)
    movs = [(int(tlv[i:i+4],16),int(tlv[i+4:i+8],16)) for i in range(4,4+leng*2,8)]
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

def setup():
    global board
    size(1024,1024)
    board = [[0 for i in range(SIZE)] for i in range(SIZE)]
    
def draw():
    pass #um later

