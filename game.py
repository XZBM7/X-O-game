import pygame
import json
import random


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

def load_stats():
    try:
        with open('stats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"X": 0, "O": 0, "Draw": 0, "Games": 0}

def save_stats(stats):
    with open('stats.json', 'w') as f:
        json.dump(stats, f)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

font = pygame.font.SysFont(None, 45)  
large_font = pygame.font.SysFont(None, 150)  
small_font = pygame.font.SysFont(None, 35)


board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player = 'X'
ai_difficulty = 'easy'
colors = {'X': BLUE, 'O': RED}

def draw_board():
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if board[row][col]:
                text = large_font.render(board[row][col], True, colors[board[row][col]])
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    turn_text = font.render(f"Turn: {player}", True, BLACK)
    screen.blit(turn_text, (20, HEIGHT - 40))
    
    pygame.display.flip()



def check_winner():
    for row in range(GRID_SIZE):
        if len(set(board[row])) == 1 and board[row][0] != '':
            return board[row][0]
    for col in range(GRID_SIZE):
        if len(set([board[row][col] for row in range(GRID_SIZE)])) == 1 and board[0][col] != '':
            return board[0][col]
    if len(set([board[i][i] for i in range(GRID_SIZE)])) == 1 and board[0][0] != '':
        return board[0][0]
    if len(set([board[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)])) == 1 and board[0][GRID_SIZE - 1] != '':
        return board[0][GRID_SIZE - 1]
    return None

def is_board_full():
    return all(cell != '' for row in board for cell in row)

def ai_move():
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == '']
    if ai_difficulty == 'easy':
        return random.choice(empty_cells)
    elif ai_difficulty == 'medium':
        return medium_ai(empty_cells)
    elif ai_difficulty == 'hard':
        return hard_ai(empty_cells)

def medium_ai(empty_cells):
    for r, c in empty_cells:
        board[r][c] = 'O'
        if check_winner() == 'O':
            board[r][c] = ''
            return r, c
        board[r][c] = 'X'
        if check_winner() == 'X':
            board[r][c] = ''
            return r, c
        board[r][c] = ''
    return random.choice(empty_cells)

def hard_ai(empty_cells):
    best_move = None
    for r, c in empty_cells:
        board[r][c] = 'O'
        if check_winner() == 'O':
            best_move = (r, c)
        board[r][c] = 'X'
        if check_winner() == 'X':
            best_move = (r, c)
        board[r][c] = ''
        if best_move:
            return best_move
    return random.choice(empty_cells)

def display_result(result_text):
    screen.fill(WHITE)
    result_surface = font.render(result_text, True, BLACK)
    screen.blit(result_surface, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(1500) 


def show_exit_confirmation():
     while True:
        screen.fill(WHITE)
        title = font.render("Are you sure you want to exit?", True, RED)
        screen.blit(title, (WIDTH // 9, HEIGHT // 9))

        yes_button = pygame.draw.rect(screen, RED, (WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50))
        no_button = pygame.draw.rect(screen, GREEN, (WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 50))

        yes_text = font.render("Yes", True, WHITE)
        screen.blit(yes_text, (WIDTH // 2 - yes_text.get_width() // 2, HEIGHT // 2 + 10))
        no_text = font.render("No", True, WHITE)
        screen.blit(no_text, (WIDTH // 2 - no_text.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if yes_button.collidepoint(x, y):
                    pygame.quit()
                    exit()
                elif no_button.collidepoint(x, y):
                    return  
                
def main_menu():
    global ai_difficulty
    while True:
        screen.fill(WHITE)
        title = font.render("Tic-Tac-Toe", True, BLACK)
        screen.blit(title, (WIDTH // 4, HEIGHT // 4))

        play_button = pygame.draw.rect(screen, GREEN, (WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50))
        settings_button = pygame.draw.rect(screen, YELLOW, (WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 50))
        stats_button = pygame.draw.rect(screen, BLUE, (WIDTH // 4, HEIGHT // 2 + 120, WIDTH // 2, 50))
        exit_button = pygame.draw.rect(screen, RED, (WIDTH // 4, HEIGHT // 2 + 180, WIDTH // 2, 50))

        title_text = font.render("Play", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 + 10))
        settings_text = font.render("Settings", True, BLACK)
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 2 + 70))
        stats_text = font.render("Statistics", True, WHITE)
        screen.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, HEIGHT // 2 + 130))
        exit_text = font.render("Exit", True, WHITE)
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 190))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button.collidepoint(x, y):
                    game_mode_menu()
                elif settings_button.collidepoint(x, y):
                    settings_menu()
                elif stats_button.collidepoint(x, y):
                    stats_menu()
                elif exit_button.collidepoint(x, y):
                    show_exit_confirmation()

def game_mode_menu():
    global ai_difficulty
    while True:
        screen.fill(WHITE)
        title = font.render("Select Game Mode", True, BLACK)
        screen.blit(title, (WIDTH // 4, HEIGHT // 4))

        player_vs_player_button = pygame.draw.rect(screen, GREEN, (WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50))
        player_vs_ai_button = pygame.draw.rect(screen, YELLOW, (WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 50))
        back_button = pygame.draw.rect(screen, RED, (WIDTH // 4, HEIGHT // 2 + 120, WIDTH // 2, 50))

        title_text = font.render("Play vs Friend", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 + 10))
        ai_text = font.render("Play vs AI", True, BLACK)
        screen.blit(ai_text, (WIDTH // 2 - ai_text.get_width() // 2, HEIGHT // 2 + 70))
        back_text = font.render("Back", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 130))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if player_vs_player_button.collidepoint(x, y):
                    play_game(False)
                elif player_vs_ai_button.collidepoint(x, y):
                    ai_difficulty_menu()
                elif back_button.collidepoint(x, y):
                    main_menu()

def ai_difficulty_menu():
    global ai_difficulty
    while True:
        screen.fill(WHITE)
        title = font.render("Select AI Difficulty", True, BLACK)
        screen.blit(title, (WIDTH // 4, HEIGHT // 4))

        easy_button = pygame.draw.rect(screen, GREEN, (WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50))
        medium_button = pygame.draw.rect(screen, YELLOW, (WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 50))
        hard_button = pygame.draw.rect(screen, RED, (WIDTH // 4, HEIGHT // 2 + 120, WIDTH // 2, 50))
        back_button = pygame.draw.rect(screen, BLUE, (WIDTH // 4, HEIGHT // 2 + 180, WIDTH // 2, 50))

        easy_text = font.render("Easy", True, WHITE)
        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 + 10))
        medium_text = font.render("Medium", True, BLACK)
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 + 70))
        hard_text = font.render("Hard", True, WHITE)
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 130))
        back_text = font.render("Back", True, BLACK)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 190))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_button.collidepoint(x, y):
                    ai_difficulty = 'easy'
                    play_game(True)
                elif medium_button.collidepoint(x, y):
                    ai_difficulty = 'medium'
                    play_game(True)
                elif hard_button.collidepoint(x, y):
                    ai_difficulty = 'hard'
                    play_game(True)
                elif back_button.collidepoint(x, y):
                    game_mode_menu()

def settings_menu():
    global colors
    while True:
        screen.fill(WHITE)
        title = font.render("Settings", True, BLACK)
        screen.blit(title, (WIDTH // 4, HEIGHT // 4))

        x_color_button = pygame.draw.rect(screen, colors['X'], (WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50))
        o_color_button = pygame.draw.rect(screen, colors['O'], (WIDTH // 4, HEIGHT // 2 + 60, WIDTH // 2, 50))
        back_button = pygame.draw.rect(screen, RED, (WIDTH // 4, HEIGHT // 2 + 120, WIDTH // 2, 50))

        x_color_text = font.render("X Color", True, BLACK)
        screen.blit(x_color_text, (WIDTH // 2 - x_color_text.get_width() // 2, HEIGHT // 2 + 10))
        o_color_text = font.render("O Color", True, BLACK)
        screen.blit(o_color_text, (WIDTH // 2 - o_color_text.get_width() // 2, HEIGHT // 2 + 70))
        back_text = font.render("Back", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 130))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x_color_button.collidepoint(x, y):
                    colors['X'] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif o_color_button.collidepoint(x, y):
                    colors['O'] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif back_button.collidepoint(x, y):
                    main_menu()

def stats_menu():
    stats = load_stats()
    while True:
        screen.fill(WHITE)
        title = font.render("Statistics", True, BLACK)
        screen.blit(title, (WIDTH // 4, HEIGHT // 4))

        x_wins_text = small_font.render(f"X Wins: {stats['X']}", True, BLACK)
        o_wins_text = small_font.render(f"O Wins: {stats['O']}", True, BLACK)
        draws_text = small_font.render(f"Draws: {stats['Draw']}", True, BLACK)
        games_text = small_font.render(f"Total Games: {stats['Games']}", True, BLACK)
        back_button = pygame.draw.rect(screen, RED, (WIDTH // 4, HEIGHT // 2 + 120, WIDTH // 2, 50))

        screen.blit(x_wins_text, (WIDTH // 4, HEIGHT // 2))
        screen.blit(o_wins_text, (WIDTH // 4, HEIGHT // 2 + 30))
        screen.blit(draws_text, (WIDTH // 4, HEIGHT // 2 + 60))
        screen.blit(games_text, (WIDTH // 4, HEIGHT // 2 + 90))
        back_text = font.render("Back", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 130))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.collidepoint(x, y):
                    main_menu()
    

def play_game(ai_mode):
    global board, player
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player = 'X'
    if ai_mode:
        ai_move()

    while True:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if board[row][col] == '':
                    board[row][col] = player
                    if check_winner():
                        display_result(f"{player} Wins!")
                        stats = load_stats()
                        stats[player] += 1
                        stats['Games'] += 1
                        save_stats(stats)
                        pygame.time.wait(3000)  
                        stats_menu() 
                        return
                    if is_board_full():
                        display_result("Draw!")
                        stats = load_stats()
                        stats['Draw'] += 1
                        stats['Games'] += 1
                        save_stats(stats)
                        pygame.time.wait(3000)  
                        stats_menu()  
                        return
                    player = 'O' if player == 'X' else 'X'
                    if ai_mode and player == 'O':
                        ai_row, ai_col = ai_move()
                        board[ai_row][ai_col] = 'O'
                        if check_winner():
                            display_result("O Wins!")
                            stats = load_stats()
                            stats['O'] += 1
                            stats['Games'] += 1
                            save_stats(stats)
                            pygame.time.wait(3000)  
                            stats_menu()  
                            return
                        if is_board_full():
                            display_result("Draw!")
                            stats = load_stats()
                            stats['Draw'] += 1
                            stats['Games'] += 1
                            save_stats(stats)
                            pygame.time.wait(3000)  
                            stats_menu()  
                            return
                        player = 'X'

if __name__ == "__main__":
    main_menu()


