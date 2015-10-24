## this program visualizes the game of life board in real time
## ideally the server and this will connect, and the server will pass on all the "Move" messages transparently

board = []

def getmoves(tlv):
    leng = int(tlv[2:4],16)
    movs = [(int(tlv[i:i+4],16),int(tlv[i+4:i+8],16)) for i in range(4,4+leng*2,8)]
    return movs

def setup():
    global board
    size(1024,1024)
    board = [[0 for i in range(SIZE)] for i in range(SIZE)]
    
def draw():
    pass #um later

