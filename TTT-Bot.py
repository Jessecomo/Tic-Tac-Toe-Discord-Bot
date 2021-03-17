import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix="!")

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command()
async def tictactoe(ctx):
        embed = discord.Embed(title="TicTacToe Help", description = "To start a game use !ttt and mention your opponent."\
        "\n eg. !ttt @opponent")
        await ctx.send(embed = embed)

@bot.command()
async def ttt(ctx, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        await ctx.send(embed = discord.Embed(title="To see what each square's number is type !board"))
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = ctx.author
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@bot.command()
async def board(ctx):
  embed = discord.Embed(title="What each square's number is", description = ":one::two::three:\n:four::five::six:\n:seven::eight::nine:")
  await ctx.send(embed = embed)



@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                if gameOver:
                    await ctx.send(mark + " wins! :trophy:")
                elif count >= 9:
                    await ctx.send("It's a tie!")
                    tie()

                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !ttt command.")

@bot.command()
async def end(ctx):
  global gameOver
  if not gameOver:
    gameOver = True
    await ctx.send("Stopping current game...")
  else:
    await ctx.send("There is currently no game running!")

def tie():
  global gameOver
  gameOver = True

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@ttt.error
async def ttt_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention an opponent for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping player (ie. @Opponent).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

bot.run('')
#Enter Discord Token Above
