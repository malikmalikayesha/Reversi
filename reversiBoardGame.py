import pygame
import sys
import time 
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 550
HEIGHT = 550
ROWS = 8
COLS = 8
SQUARE_SIZE = (HEIGHT // ROWS)
EMPTY = 0
BLACK = -1
WHITE = 1

# Colors
black = (10, 10, 10)
white = (255, 255, 255)
red = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH + 140, HEIGHT))
pygame.display.set_caption("REVERSI")

# Create the initial board state
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
board[3][3] = 1
board[3][4] = -1
board[4][3] = -1
board[4][4] = 1

# Load images
bg_img = pygame.Surface((WIDTH + 140, HEIGHT))
bg_img.fill((24, 78, 51))
game_over_img = pygame.image.load("go_bg.png")
game_over_img = pygame.transform.scale(game_over_img, (370, 170))
board_img = pygame.image.load("board.jpg")
board_img = pygame.transform.scale(board_img, (WIDTH, HEIGHT))
white_disc_img = pygame.image.load("white_disc.png")
white_disc_img = pygame.transform.scale(white_disc_img, (SQUARE_SIZE, SQUARE_SIZE))
black_disc_img = pygame.image.load("black_disc.png")
black_disc_img = pygame.transform.scale(black_disc_img, (SQUARE_SIZE, SQUARE_SIZE))

# Tree visualization globals
tree_depth = 0
node_count = 0

# Function to draw the board
def draw_board():
    screen.blit(bg_img, (0, 0))
    screen.blit(board_img, (0, 0))
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                screen.blit(white_disc_img, ((col * SQUARE_SIZE), (row * SQUARE_SIZE)))
            elif board[row][col] == -1:
                screen.blit(black_disc_img, ((col * SQUARE_SIZE), (row * SQUARE_SIZE)))


def get_valid_moves(color):
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(row, col, color):
                moves.append((row, col))
    return moves

def discs_flipped_if_move(row, col, color):
    # Returns the number of discs that would be flipped if move is made
    count = 0
    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            if drow == 0 and dcol == 0:
                continue
            r, c = row + drow, col + dcol
            temp_count = 0
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == -color:
                temp_count += 1
                r += drow
                c += dcol
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == color:
                count += temp_count
    return count

def print_hill_climbing_header():
    print("\n" + "="*80)
    print("🏔️  HILL CLIMBING ALGORITHM VISUALIZATION")
    print("="*80)

def print_hill_climbing_step(iteration, current_move, current_score, valid_moves, all_scores):
    print(f"\n📈 ITERATION {iteration}")
    print(f"Current best move: {current_move} (Score: {current_score})")
    print("All available moves and their scores:")
    for i, (move, score) in enumerate(zip(valid_moves, all_scores)):
        marker = "🎯" if move == current_move else "  "
        print(f"  {marker} Move {move}: {score} discs flipped")

def hill_climbing_move():
    print_hill_climbing_header()
    
    valid_moves = get_valid_moves(BLACK)
    if not valid_moves:
        print("❌ No valid moves available for BLACK")
        return
    
    # Calculate scores for all moves
    all_scores = [discs_flipped_if_move(move[0], move[1], BLACK) for move in valid_moves]
    
    current_move = random.choice(valid_moves)
    current_score = discs_flipped_if_move(current_move[0], current_move[1], BLACK)
    
    print(f"🎲 Random starting move: {current_move} (Score: {current_score})")
    print_hill_climbing_step(0, current_move, current_score, valid_moves, all_scores)
    
    improved = True
    iterations = 0
    max_iterations = 10

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        
        print(f"\n🔍 Searching for better moves in iteration {iterations}...")
        
        for move in valid_moves:
            if move == current_move:
                continue
            score = discs_flipped_if_move(move[0], move[1], BLACK)
            print(f"  Evaluating {move}: {score} vs current {current_score}")
            
            if score > current_score:
                print(f"  ✅ Found better move! {move} ({score}) > {current_move} ({current_score})")
                current_move = move
                current_score = score
                improved = True
        
        if improved:
            print_hill_climbing_step(iterations, current_move, current_score, valid_moves, all_scores)
        else:
            print("  ❌ No better moves found - local optimum reached!")

    print(f"\n🎯 FINAL DECISION: Move {current_move} with score {current_score}")
    print("="*80)
    
    make_move(current_move[0], current_move[1], BLACK)

# Function to check if a move is valid
def is_valid_move(row, col, color):
    if board[row][col] != 0:
        return False
    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            if drow == 0 and dcol == 0:
                continue
            r, c = row + drow, col + dcol
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == -color:
                r += drow
                c += dcol
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == color and (r - row != drow or c - col != dcol):
                return True
    return False


# Function to flip discs
def flip_discs(row, col, color):
    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            if drow == 0 and dcol == 0:
                continue
            r, c = row + drow, col + dcol
            discs_to_flip = []
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == -color:
                discs_to_flip.append((r, c))
                r += drow
                c += dcol
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == color and discs_to_flip:
                for flip_row, flip_col in discs_to_flip:
                    board[flip_row][flip_col] = color


# Function to make a move
def make_move(row, col, color):
    if not is_valid_move(row, col, color):
        return False
    board[row][col] = color
    flip_discs(row, col, color)
    return True


# Function to get the score
def get_score():
    white_score = sum(row.count(1) for row in board)
    black_score = sum(row.count(-1) for row in board)
    return white_score, black_score


# Function to check if the game is over
def is_game_over(board):
    # Check for a full board
    if all(all(cell != EMPTY for cell in row) for row in board):
        return True

    # Check for no valid moves for any one player
    elif not any(is_valid_move(row, col, BLACK) for row in range(ROWS) for col in range(COLS)) and \
            not any(is_valid_move(row, col, WHITE) for row in range(ROWS) for col in range(COLS)):
        return True

    return False


# Function to evaluate board
def evaluate_board(board):
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    return black_count - white_count

def print_alpha_beta_header():
    print("\n" + "="*80)
    print("🌳 ALPHA-BETA PRUNING MINIMAX TREE VISUALIZATION")
    print("="*80)

def print_node(depth, move, player, eval_value, alpha, beta, is_pruned=False, is_final=False):
    global node_count
    node_count += 1
    
    indent = "  " * depth
    player_symbol = "⚫" if player == "BLACK" else "⚪"
    
    if is_pruned:
        print(f"{indent}✂️  Node {node_count}: {player_symbol} Move{move} - PRUNED (α={alpha:.1f}, β={beta:.1f})")
    elif is_final:
        print(f"{indent}🎯 Node {node_count}: {player_symbol} Move{move} - Final Eval: {eval_value:.1f}")
    else:
        print(f"{indent}🔍 Node {node_count}: {player_symbol} Move{move} - Eval: {eval_value:.1f} (α={alpha:.1f}, β={beta:.1f})")

# Minimax algorithm with detailed visualization
def minimax(board, depth, maximizing_player, alpha, beta, move=None, original_depth=0):
    global tree_depth, node_count
    
    current_depth = original_depth - depth
    player_name = "BLACK" if maximizing_player else "WHITE"
    
    if depth == 0 or is_game_over(board):
        eval_val = evaluate_board(board)
        print_node(current_depth, move, player_name, eval_val, alpha, beta, is_final=True)
        return eval_val
    
    if maximizing_player:
        max_eval = float("-inf")
        print_node(current_depth, move, player_name, max_eval, alpha, beta)
        
        for row in range(ROWS):
            for col in range(COLS):
                if is_valid_move(row, col, BLACK):
                    # Make a copy of the board
                    board_copy = [row[:] for row in board]
                    
                    # Temporarily make the move
                    temp_board = board
                    board = board_copy
                    make_move(row, col, BLACK)
                    
                    eval_val = minimax(board, depth - 1, False, alpha, beta, (row, col), original_depth)
                    
                    # Restore the board
                    board = temp_board
                    
                    max_eval = max(max_eval, eval_val)
                    alpha = max(alpha, eval_val)
                    
                    if beta <= alpha:
                        print_node(current_depth + 1, (row, col), "WHITE", eval_val, alpha, beta, is_pruned=True)
                        break
                        
        return max_eval
    else:
        min_eval = float("inf")
        print_node(current_depth, move, player_name, min_eval, alpha, beta)
        
        for row in range(ROWS):
            for col in range(COLS):
                if is_valid_move(row, col, WHITE):
                    # Make a copy of the board
                    board_copy = [row[:] for row in board]
                    
                    # Temporarily make the move
                    temp_board = board
                    board = board_copy
                    make_move(row, col, WHITE)
                    
                    eval_val = minimax(board, depth - 1, True, alpha, beta, (row, col), original_depth)
                    
                    # Restore the board
                    board = temp_board
                    
                    min_eval = min(min_eval, eval_val)
                    beta = min(beta, eval_val)
                    
                    if beta <= alpha:
                        print_node(current_depth + 1, (row, col), "BLACK", eval_val, alpha, beta, is_pruned=True)
                        break
                        
        return min_eval

def minimax_move():
    global node_count, board
    print_alpha_beta_header()
    
    valid_moves = get_valid_moves(BLACK)
    if not valid_moves:
        print("❌ No valid moves available for BLACK")
        return
    
    best_move = None
    best_value = float("-inf")
    node_count = 0
    search_depth = 3
    
    print(f"🎯 Starting minimax search with depth {search_depth}")
    print(f"📊 Valid moves: {valid_moves}")
    
    for move in valid_moves:
        move_row, move_col = move
        print(f"\n🔍 Evaluating move {move}:")
        
        # Make a copy and apply move
        board_copy = [board_row[:] for board_row in board]
        temp_board = board
        board = board_copy
        make_move(move_row, move_col, BLACK)
        
        # Run minimax
        value = minimax(board, search_depth - 1, False, float("-inf"), float("inf"), move, search_depth)
        
        # Restore board
        board = temp_board
        
        print(f"💯 Move {move} final value: {value}")
        
        if value > best_value:
            best_value = value
            best_move = move
            print(f"✅ New best move: {best_move} with value {best_value}")
    
    print(f"\n🎯 FINAL DECISION: Move {best_move} with value {best_value}")
    print(f"📈 Total nodes explored: {node_count}")
    print("="*80)
    
    if best_move:
        make_move(best_move[0], best_move[1], BLACK)
# Function to Show game is over
def show_game_over_message():
    font = pygame.font.Font(None, 36)
    f = pygame.font.Font(None, 20)
    white_score, black_score = get_score()
    replay_text = f.render("Press Spacebar to Play Again", True, white)
    if white_score == black_score:
        game_over_text = font.render("Tie Game", True, red)
        return game_over_text, replay_text
    elif white_score > black_score:
        game_over_text = font.render("Congratulations. You Won!", True, red)
        return game_over_text, replay_text
    elif white_score < black_score:
        game_over_text = font.render("Game Over. You lose!", True, red)
        return game_over_text, replay_text

# Algorithm selection
current_algorithm = "hill_climbing"  # default

turn = WHITE
black_move_time = None  # Track when to make black's move

print("🎮 REVERSI GAME STARTED")
print("🔄 Press 'H' for Hill Climbing, 'M' for Minimax during the game")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_game_over(board) and turn == WHITE:
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    col = x // SQUARE_SIZE
                    row = y // SQUARE_SIZE
                    if is_valid_move(row, col, WHITE):
                        make_move(row, col, WHITE)
                        turn = BLACK
                        black_move_time = time.time()  # Start timer for black's move
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                board[3][3] = 1
                board[3][4] = -1
                board[4][3] = -1
                board[4][4] = 1
                turn = WHITE
                black_move_time = None
                print("\n🔄 GAME RESET")
            elif event.key == pygame.K_h:
                current_algorithm = "hill_climbing"
                print(f"\n🏔️  Switched to Hill Climbing algorithm")
            elif event.key == pygame.K_m:
                current_algorithm = "minimax"
                print(f"\n🌳 Switched to Minimax with Alpha-Beta Pruning algorithm")

    draw_board()

    # Display
    white_score, black_score = get_score()
    font = pygame.font.Font(None, 36)
    white_text = font.render(f"White: {white_score}", True, white)
    black_text = font.render(f"Black: {black_score}", True, black)
    screen.blit(white_text, (565, 100))
    screen.blit(black_text, (565, 140))

    if not is_game_over(board):
        if turn == WHITE:
            if not any(is_valid_move(row, col, WHITE) for row in range(ROWS) for col in range(COLS)):
                turn = BLACK
                black_move_time = time.time()
        elif turn == BLACK:
            if black_move_time and (time.time() - black_move_time >= 2.5):
                if current_algorithm == "hill_climbing":
                    hill_climbing_move()
                else:
                    minimax_move()
                turn = WHITE
                black_move_time = None
    else:
        game_over_text, replay_text = show_game_over_message()
        game_over_text_pos = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        game_over_img_pos = game_over_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        replay_text_pos = replay_text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 28))
        screen.blit(game_over_img, game_over_img_pos)
        screen.blit(game_over_text, game_over_text_pos)
        screen.blit(replay_text, replay_text_pos)

    pygame.display.flip()