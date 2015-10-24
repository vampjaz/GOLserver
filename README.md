## GOLserver: server for PPCG king-of-the-hill challenge

# [Current text for reference:](http://meta.codegolf.stackexchange.com/a/1332/16472)

**EDIT**: This challenge is looking for someone to either write and run an arena server, or someone that wants to rephrase the challenge so that an arena server is not needed and who is also prepared to run entries manually. Both options turned out to be more complicated for me than I originally envisioned. To make a long story short: it's yours!

---

# It's Life, Jim, but not as we know it

You probably know *Conway's Game of Life*, the famous cellular automaton invented by mathematician John Conway. *Life* is a set of rules that, together, allow you to simulate a two-dimensional board of cells. The rules decide which cells on the board live and  which ones die. With some imagination, you could say that *Life* is a zero-player game: a game with the objective to find patterns with interesting behavior, like the famous glider.

![Glider](http://upload.wikimedia.org/wikipedia/commons/f/f2/Game_of_life_animated_glider.gif)

A zero-player game... Until today. You are to write a program that plays the Game of Life - and plays it to win, King of the Hill-style. Your opponent (singular) of course tries to do the same. The winner is either the last bot with any live cells, or the player with the most live cells after 5 minutes of clock time.

## Game rules

The rules are *almost* the same as normal (B3/S23) Life:

* A live cell with fewer than two friendly neighbors dies from starvation.
* A live cell with two or three friendly neighbors survives.
* A live cell with more than three friendly neighbors dies from overpopulation.
* A dead cell with exactly three neighbors of the same player comes alive to fight for that player *provided there are no enemy neighbors*.

...but after each generation, both you and your opponent get the opportunity to intervene. You can awake up to a maximum of 30 cells to fight for you. (Who goes first is decided by the server.)

The board is a 1024&times;1024 cell square. All squares are initially dead. The borders do not wrap around (this is not a torus-shaped world) and are permanently dead.

This is is a contest in the spirit of *Battlebots* and *Core Wars*. However, unlike those two, you are supposed to run your implementation on your own machine. You fight the other contestants on a central arena server.

## Protocol

The arena server speaks a simple, compact [TLV](http://en.wikipedia.org/wiki/Type-length-value) protocol over TCP. Messages have the following format:

    tlvvvvvvv...
    ^ Type (1 byte, ASCII)
     ^ Length (1 byte, unsigned int)
      ^ Values (Exactly length bytes long)

The meaning of the value depends on the type of message. For example, for a move that sets (781,991) and (214, 1), the message would become (hex-encoded):

    4D08030D03DF00D60001
    --                   = The type (0x4D = M in ASCII)
      --                 = Length (8 bits)
        --------         = 718 and 991 encoded as network-order 16-bit integers
                -------- = ditto for (214,1)


You're probably going to want to write a client. Here's how:

1. Connect to the central arena server.
1. Send an **`I`**&#8203;dentification message with an identification string (up to 250 bytes of UTF-8).
1. Have your bot wait for a game to begin. The arena hosts one game at a time. You will fight either another contestant's bot, or  a training round against my entry, which is not included in the competition.
1. The game starts when you receive a **`S`**&#8203;tart message. Included in the message is the name of your opponent, which will start with "Training/" if you're up against the training bot.
1. When you receive a **`M`**&#8203;ove, apply it to your board. Moves are encoded as arrays of pairs of 16-bit unsigned integers. For each pair, set the cell at that X/Y-coordinate to the enemy's 'color'.
1. When you receive a **`G`**&#8203;eneration marker, evolve your current view of the game board one step according to the rules above.
1. When you receive a **`T`**&#8203;urn message, it's your turn. Reply with a Move as soon as possible. (Don't want to interfere? Send a Move message with zero moves.)
1. When you receive a **`B`**&#8203;ye message, the game is over and you can disconnect. The value will tell you your score and your opponent's, in that order, as a pair of 32-bit unsigned integers.
1. Reconnect when you're ready for another round.

Note that the server will *not* send you the entire state of the board at any time for bandwidth reasons. You'll have to keep track of the evolving yourself. ([Here](http://rosettacode.org/wiki/Conway%27s_Game_of_Life#C) are implementations of normal *Life* in many languages. You could probably base your implementation on one of those.)

## Competition rules

* You should **`I`**&#8203;dentify as `name/bot`, where *name* is your StackExchange user name and *bot* is a PG-rated but otherwise very intimidating name for your implementation (Glider of Doom? DiveBomber? Pufferfish?)
* If your implementation fails to follow the protocol, you'll be disconnected - and the game will be forfeited.
* You are not allowed to willfully take advantage of a fault in the arena server.
* Have your AI decide on moves in a sane time. Calculate strategies in advance if at all possible so you'll be able to send your next move as  fast as reasonably possible.
* Finally, please be nice to the server. It's there for your enjoyment.
* Not following these rules can lead to disqualification.

## Scoring

The bot with the largest KD spread, that is, the largest positive difference between the amount of wins and the amount of losses, wins.
