import pygame
pygame.init()  
WIDTH, HEIGHT = 1200, 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 26, bold=True)
small_font = pygame.font.SysFont("Arial", 16)
big_font = pygame.font.SysFont("Arial", 48, bold=True)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
timer = pygame.time.Clock()

# Color scheme - Dark theme with neon
DARK_BG = (15, 15, 25)
DARK_PANEL = (25, 25, 40)
NEON_CYAN = (0, 255, 255)
NEON_MAGENTA = (255, 0, 255)
NEON_GREEN = (0, 255, 100)
NEON_PURPLE = (180, 0, 255)
NEON_PINK = (255, 20, 147)

# Board dimensions
BOARD_SIZE = 8
SQUARE_SIZE = 90
BOARD_X = 20
BOARD_Y = 20
SIDEBAR_X = 740

# Game pieces and their locations
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

turn_step = 0
selection = 100
valid_moves = []

# Tracking for special moves
white_king_moved = False
white_rook_moved = [False, False]  # queenside, kingside
black_king_moved = False
black_rook_moved = [False, False]  # queenside, kingside
last_pawn_move = None  # Track last pawn move for en passant
promotion_pending = False
promotion_piece_index = None
promotion_color = None

# Load piece images
black_rook = pygame.image.load("pieces/black rook.png")
black_rook = pygame.transform.scale(black_rook, (75, 75))
black_rook_small = pygame.transform.scale(black_rook, (30, 30))
black_queen = pygame.image.load("pieces/black queen.png")
black_queen = pygame.transform.scale(black_queen, (75, 75))
black_queen_small = pygame.transform.scale(black_queen, (30, 30))
black_king = pygame.image.load("pieces/black king.png")
black_king = pygame.transform.scale(black_king, (75, 75))
black_king_small = pygame.transform.scale(black_king, (30, 30))
black_bishop = pygame.image.load("pieces/black bishop.png")
black_bishop = pygame.transform.scale(black_bishop, (75, 75))
black_bishop_small = pygame.transform.scale(black_bishop, (30, 30))
black_knight = pygame.image.load("pieces/black knight.png")
black_knight = pygame.transform.scale(black_knight, (75, 75))
black_knight_small = pygame.transform.scale(black_knight, (30, 30))
black_pawn = pygame.image.load("pieces/black pawn.png")
black_pawn = pygame.transform.scale(black_pawn, (75, 75))
black_pawn_small = pygame.transform.scale(black_pawn, (30, 30))

black_images = [black_rook, black_knight, black_bishop, black_queen, black_king, black_pawn]
black_images_small = [black_rook_small, black_knight_small, black_bishop_small, black_queen_small, black_king_small, black_pawn_small]

white_rook = pygame.image.load("pieces/white rook.png")
white_rook = pygame.transform.scale(white_rook, (75, 75))
white_rook_small = pygame.transform.scale(white_rook, (30, 30))
white_queen = pygame.image.load("pieces/white queen.png")
white_queen = pygame.transform.scale(white_queen, (75, 75))
white_queen_small = pygame.transform.scale(white_queen, (30, 30))
white_king = pygame.image.load("pieces/white king.png")
white_king = pygame.transform.scale(white_king, (75, 75))
white_king_small = pygame.transform.scale(white_king, (30, 30))
white_bishop = pygame.image.load("pieces/white bishop.png")
white_bishop = pygame.transform.scale(white_bishop, (75, 75))
white_bishop_small = pygame.transform.scale(white_bishop, (30, 30))
white_knight = pygame.image.load("pieces/white knight.png")
white_knight = pygame.transform.scale(white_knight, (75, 75))
white_knight_small = pygame.transform.scale(white_knight, (30, 30))
white_pawn = pygame.image.load("pieces/white pawn.png")
white_pawn = pygame.transform.scale(white_pawn, (75, 75))
white_pawn_small = pygame.transform.scale(white_pawn, (30, 30))

white_images = [white_rook, white_knight, white_bishop, white_queen, white_king, white_pawn]
white_images_small = [white_rook_small, white_knight_small, white_bishop_small, white_queen_small, white_king_small, white_pawn_small]

piece_list = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']

counter = 0
winner = ""

def draw_board():
    # Draw main background
    screen.fill(DARK_BG)
    
    # Draw chessboard
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = (40, 40, 60)      # Dark square
            else:
                color = (60, 60, 90)      # Lighter dark square
            
            pygame.draw.rect(
                screen,
                color,
                (BOARD_X + col * SQUARE_SIZE, BOARD_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
    
    # Draw glowing board border
    pygame.draw.rect(screen, NEON_CYAN, (BOARD_X - 3, BOARD_Y - 3, BOARD_SIZE * SQUARE_SIZE + 6, BOARD_SIZE * SQUARE_SIZE + 6), 3)
    pygame.draw.rect(screen, NEON_MAGENTA, (BOARD_X - 2, BOARD_Y - 2, BOARD_SIZE * SQUARE_SIZE + 4, BOARD_SIZE * SQUARE_SIZE + 4), 1)
    
    # Draw sidebar background
    pygame.draw.rect(screen, DARK_PANEL, (SIDEBAR_X, 0, WIDTH - SIDEBAR_X, HEIGHT))
    pygame.draw.line(screen, NEON_CYAN, (SIDEBAR_X - 3, 0), (SIDEBAR_X - 3, HEIGHT), 3)

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (BOARD_X + white_location[i][0] * SQUARE_SIZE + 7, BOARD_Y + white_location[i][1] * SQUARE_SIZE + 7))
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, NEON_GREEN, (BOARD_X + white_location[i][0] * SQUARE_SIZE, BOARD_Y + white_location[i][1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
    
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (BOARD_X + black_location[i][0] * SQUARE_SIZE + 7, BOARD_Y + black_location[i][1] * SQUARE_SIZE + 7))
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, NEON_CYAN, (BOARD_X + black_location[i][0] * SQUARE_SIZE, BOARD_Y + black_location[i][1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

def check_options(pieces, locations, color_str):
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, color_str)
        elif piece == 'rook':
            moves_list = check_rook(location, color_str)
        elif piece == 'knight':
            moves_list = check_knight(location, color_str)
        elif piece == 'bishop':
            moves_list = check_bishop(location, color_str)
        elif piece == 'queen':
            moves_list = check_queen(location, color_str)
        elif piece == 'king':
            moves_list = check_king(location, color_str)
        
        all_moves_list.append(moves_list)
    return all_moves_list

def check_pawn(position, color_str):
    moves_list = []
    if color_str == 'white':
        # Forward move
        if (position[0], position[1] + 1) not in white_location and \
            (position[0], position[1] + 1) not in black_location and position[1] + 1 < 8:
            moves_list.append((position[0], position[1] + 1))
        # Double move from starting position
        if (position[0], position[1] + 2) not in white_location and \
            (position[0], position[1] + 2) not in black_location and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        # Diagonal captures
        if (position[0] + 1, position[1] + 1) in black_location:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_location:
            moves_list.append((position[0] - 1, position[1] + 1))
        # En passant
        if last_pawn_move:
            last_from, last_to, last_color = last_pawn_move
            if last_color == 'black' and last_to[1] == position[1] and abs(last_from[0] - last_to[0]) == 2:
                if last_to[0] == position[0] + 1:
                    moves_list.append((position[0] + 1, position[1] + 1))
                elif last_to[0] == position[0] - 1:
                    moves_list.append((position[0] - 1, position[1] + 1))
    else:
        # Forward move
        if (position[0], position[1] - 1) not in white_location and \
            (position[0], position[1] - 1) not in black_location and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        # Double move from starting position
        if (position[0], position[1] - 2) not in white_location and \
            (position[0], position[1] - 2) not in black_location and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        # Diagonal captures
        if (position[0] + 1, position[1] - 1) in white_location:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_location:
            moves_list.append((position[0] - 1, position[1] - 1))
        # En passant
        if last_pawn_move:
            last_from, last_to, last_color = last_pawn_move
            if last_color == 'white' and last_to[1] == position[1] and abs(last_from[0] - last_to[0]) == 2:
                if last_to[0] == position[0] + 1:
                    moves_list.append((position[0] + 1, position[1] - 1))
                elif last_to[0] == position[0] - 1:
                    moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

def check_rook(position, color_str):
    moves_list = []
    if color_str == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        enemies_list = white_location
        friends_list = black_location
    for i in range(4):
        path = True
        chain = 1
        if i == 0: x, y = 0, 1
        elif i == 1: x, y = 0, -1
        elif i == 2: x, y = -1, 0
        else: x, y = 1, 0
        while path:
            if (position[0] + x * chain, position[1] + y * chain) not in friends_list and 0 <= position[0] + x * chain < 8 and 0 <= position[1] + y * chain < 8:
                moves_list.append((position[0] + x * chain, position[1] + y * chain))
                if (position[0] + x * chain, position[1] + y * chain) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_knight(position, color_str):
    if color_str == 'white':
        friends_list = white_location
    else:
        friends_list = black_location
    moves_list = []
    knight_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    for x, y in knight_moves:
        if (position[0] + x, position[1] + y) not in friends_list and 0 <= position[0] + x < 8 and 0 <= position[1] + y < 8:
            moves_list.append((position[0] + x, position[1] + y))
    return moves_list

def check_bishop(position, color_str):
    moves_list = []
    if color_str == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        enemies_list = white_location
        friends_list = black_location
    for i in range(4):
        path = True
        chain = 1
        if i == 0: x, y = 1, 1
        elif i == 1: x, y = -1, 1
        elif i == 2: x, y = 1, -1
        else: x, y = -1, -1
        while path:
            if (position[0] + x * chain, position[1] + y * chain) not in friends_list and 0 <= position[0] + x * chain < 8 and 0 <= position[1] + y * chain < 8:
                moves_list.append((position[0] + x * chain, position[1] + y * chain))
                if (position[0] + x * chain, position[1] + y * chain) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_queen(position, color_str):
    moves_list = []
    moves_list.extend(check_rook(position, color_str))
    moves_list.extend(check_bishop(position, color_str))
    return moves_list

def check_king(position, color_str):
    moves_list = []
    if color_str == 'white':
        enemies_list = black_location
        friends_list = white_location
        king_moved = white_king_moved
        rook_moved = white_rook_moved
    else:
        enemies_list = white_location
        friends_list = black_location
        king_moved = black_king_moved
        rook_moved = black_rook_moved
    
    # Normal king moves (1 square in any direction)
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x == 0 and y == 0:
                continue
            new_pos = (position[0] + x, position[1] + y)
            if new_pos not in friends_list and 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:
                moves_list.append(new_pos)
    
    # Castling
    if not king_moved:
        if color_str == 'white':
            # Kingside castling (h1)
            if not rook_moved[1] and (7, 0) in white_location:
                if (5, 0) not in white_location and (6, 0) not in white_location and (5, 0) not in black_location and (6, 0) not in black_location:
                    moves_list.append((6, 0))
            # Queenside castling (a1)
            if not rook_moved[0] and (0, 0) in white_location:
                if (1, 0) not in white_location and (2, 0) not in white_location and (3, 0) not in white_location:
                    if (1, 0) not in black_location and (2, 0) not in black_location and (3, 0) not in black_location:
                        moves_list.append((2, 0))
        else:
            # Kingside castling (h8)
            if not rook_moved[1] and (7, 7) in black_location:
                if (5, 7) not in white_location and (6, 7) not in white_location and (5, 7) not in black_location and (6, 7) not in black_location:
                    moves_list.append((6, 7))
            # Queenside castling (a8)
            if not rook_moved[0] and (0, 7) in black_location:
                if (1, 7) not in white_location and (2, 7) not in white_location and (3, 7) not in white_location:
                    if (1, 7) not in black_location and (2, 7) not in black_location and (3, 7) not in black_location:
                        moves_list.append((2, 7))
    
    return moves_list

def check_valid_moves():
    if turn_step < 2:
        valid_options = check_options(white_pieces, white_location, 'white')[selection]
    else:
        valid_options = check_options(black_pieces, black_location, 'black')[selection]
    return valid_options

def draw_valid(moves):
    if turn_step < 2:
        color = NEON_GREEN
    else:
        color = NEON_CYAN
    for move in moves:
        pygame.draw.circle(screen, color, (BOARD_X + move[0] * SQUARE_SIZE + SQUARE_SIZE // 2, BOARD_Y + move[1] * SQUARE_SIZE + SQUARE_SIZE // 2), 6)
        pygame.draw.circle(screen, color, (BOARD_X + move[0] * SQUARE_SIZE + SQUARE_SIZE // 2, BOARD_Y + move[1] * SQUARE_SIZE + SQUARE_SIZE // 2), 3)

def draw_captured():
    y_start = 30
    x_pos = SIDEBAR_X + 20
    max_per_row = 2
    
    # White captured pieces (black pieces)
    pygame.draw.line(screen, NEON_CYAN, (x_pos - 10, y_start - 15), (x_pos + 95, y_start - 15), 2)
    text = small_font.render("White Captured:", True, NEON_CYAN)
    screen.blit(text, (x_pos - 5, y_start - 30))
    
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        col = i % max_per_row
        row = i // max_per_row
        screen.blit(black_images_small[index], (x_pos + col * 50, y_start + row * 50))
    
    # Black captured pieces (white pieces)
    y_capture_black = y_start + 200
    pygame.draw.line(screen, NEON_CYAN, (x_pos - 10, y_capture_black - 15), (x_pos + 95, y_capture_black - 15), 2)
    text = small_font.render("Black Captured:", True, NEON_CYAN)
    screen.blit(text, (x_pos - 5, y_capture_black - 30))
    
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        col = i % max_per_row
        row = i // max_per_row
        screen.blit(white_images_small[index], (x_pos + col * 50, y_capture_black + row * 50))

def draw_promotion_menu():
    if promotion_pending:
        menu_x = SIDEBAR_X + 15
        menu_y = 300
        menu_items = ['Queen', 'Rook', 'Bishop', 'Knight']
        
        pygame.draw.rect(screen, DARK_PANEL, (menu_x - 15, menu_y - 30, 180, 225))
        pygame.draw.rect(screen, NEON_PINK, (menu_x - 15, menu_y - 30, 180, 225), 3)
        
        prompt = small_font.render("Promote Pawn:", True, NEON_PINK)
        screen.blit(prompt, (menu_x + 20, menu_y - 20))
        
        for i, item in enumerate(menu_items):
            text = small_font.render(item, True, NEON_CYAN)
            pygame.draw.rect(screen, (60, 60, 100), (menu_x, menu_y + 15 + i * 45, 150, 40), 0)
            pygame.draw.rect(screen, NEON_CYAN, (menu_x, menu_y + 15 + i * 45, 150, 40), 2)
            screen.blit(text, (menu_x + 50, menu_y + 22 + i * 45))

def handle_promotion(choice):
    global promotion_pending, promotion_piece_index, promotion_color
    global white_pieces, black_pieces
    
    promotion_options = ['queen', 'rook', 'bishop', 'knight']
    if 0 <= choice < len(promotion_options):
        new_piece = promotion_options[choice]
        if promotion_color == 'white':
            white_pieces[promotion_piece_index] = new_piece
        else:
            black_pieces[promotion_piece_index] = new_piece
        promotion_pending = False

def handle_castling(from_pos, to_pos, color):
    global white_rook_moved, black_rook_moved, white_king_moved, black_king_moved
    
    if color == 'white':
        white_king_moved = True
        if to_pos == (6, 0):  # Kingside
            white_rook_moved[1] = True
            rook_index = white_location.index((7, 0))
            white_location[rook_index] = (5, 0)
        elif to_pos == (2, 0):  # Queenside
            white_rook_moved[0] = True
            rook_index = white_location.index((0, 0))
            white_location[rook_index] = (3, 0)
    else:
        black_king_moved = True
        if to_pos == (6, 7):  # Kingside
            black_rook_moved[1] = True
            rook_index = black_location.index((7, 7))
            black_location[rook_index] = (5, 7)
        elif to_pos == (2, 7):  # Queenside
            black_rook_moved[0] = True
            rook_index = black_location.index((0, 7))
            black_location[rook_index] = (3, 7)

def handle_en_passant(from_pos, to_pos, color):
    global last_pawn_move
    
    if color == 'white' and to_pos[1] == from_pos[1] + 1 and to_pos[0] != from_pos[0]:
        # White pawn moving diagonally without capturing
        if (to_pos[0], to_pos[1] - 1) in black_location:
            enemy_index = black_location.index((to_pos[0], to_pos[1] - 1))
            captured_pieces_white.append(black_pieces[enemy_index])
            black_pieces.pop(enemy_index)
            black_location.pop(enemy_index)
    elif color == 'black' and to_pos[1] == from_pos[1] - 1 and to_pos[0] != from_pos[0]:
        # Black pawn moving diagonally without capturing
        if (to_pos[0], to_pos[1] + 1) in white_location:
            enemy_index = white_location.index((to_pos[0], to_pos[1] + 1))
            captured_pieces_black.append(white_pieces[enemy_index])
            white_pieces.pop(enemy_index)
            white_location.pop(enemy_index)
    
    # Track this pawn move
    last_pawn_move = (from_pos, to_pos, color)

# Main game loop
running = True
while running:
    timer.tick(FPS)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    
    draw_board()
    draw_pieces()
    draw_captured()
    
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    
    draw_promotion_menu()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if clicking on promotion menu
            if promotion_pending:
                menu_x = SIDEBAR_X + 15
                menu_y = 300
                if menu_x <= mouse_pos[0] <= menu_x + 150:
                    for i in range(4):
                        if menu_y + 15 + i * 45 <= mouse_pos[1] <= menu_y + 55 + i * 45:
                            handle_promotion(i)
                continue
            
            # Check if click is on board
            if mouse_pos[0] >= SIDEBAR_X or mouse_pos[0] < BOARD_X or mouse_pos[1] < BOARD_Y or mouse_pos[1] >= BOARD_Y + 720:
                continue
            
            col = (mouse_pos[0] - BOARD_X) // SQUARE_SIZE
            row = (mouse_pos[1] - BOARD_Y) // SQUARE_SIZE
            click_coord = (col, row)
            
            if turn_step == 0:
                if click_coord in white_location:
                    selection = white_location.index(click_coord)
                    turn_step = 1
            elif turn_step == 1:
                if click_coord in valid_moves and selection != 100:
                    old_location = white_location[selection]
                    white_location[selection] = click_coord
                    
                    # Check if moving a pawn or rook (for tracking moves)
                    if white_pieces[selection] == 'pawn':
                        # Check for en passant
                        if click_coord[0] != old_location[0] and click_coord not in black_location:
                            handle_en_passant(old_location, click_coord, 'white')
                        else:
                            # Regular move or capture
                            if click_coord in black_location:
                                black_piece = black_location.index(click_coord)
                                captured_pieces_white.append(black_pieces[black_piece])
                                if black_pieces[black_piece] == 'king':
                                    winner = "White"
                                    running = False
                                black_pieces.pop(black_piece)
                                black_location.pop(black_piece)
                            last_pawn_move = (old_location, click_coord, 'white')
                        
                        # Check for promotion
                        if click_coord[1] == 7:
                            promotion_pending = True
                            promotion_piece_index = selection
                            promotion_color = 'white'
                    
                    elif white_pieces[selection] == 'rook':
                        if old_location == (7, 0):
                            white_rook_moved[1] = True
                        elif old_location == (0, 0):
                            white_rook_moved[0] = True
                        
                        if click_coord in black_location:
                            black_piece = black_location.index(click_coord)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = "White"
                                running = False
                            black_pieces.pop(black_piece)
                            black_location.pop(black_piece)
                    
                    elif white_pieces[selection] == 'king':
                        white_king_moved = True
                        # Check if castling
                        if click_coord == (6, 0) or click_coord == (2, 0):
                            handle_castling(old_location, click_coord, 'white')
                        elif click_coord in black_location:
                            black_piece = black_location.index(click_coord)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = "White"
                                running = False
                            black_pieces.pop(black_piece)
                            black_location.pop(black_piece)
                    
                    else:
                        if click_coord in black_location:
                            black_piece = black_location.index(click_coord)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = "White"
                                running = False
                            black_pieces.pop(black_piece)
                            black_location.pop(black_piece)
                    
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            
            elif turn_step == 2:
                if click_coord in black_location:
                    selection = black_location.index(click_coord)
                    turn_step = 3
            
            elif turn_step == 3:
                if click_coord in valid_moves and selection != 100:
                    old_location = black_location[selection]
                    black_location[selection] = click_coord
                    
                    if black_pieces[selection] == 'pawn':
                        if click_coord[0] != old_location[0] and click_coord not in white_location:
                            handle_en_passant(old_location, click_coord, 'black')
                        else:
                            if click_coord in white_location:
                                white_piece = white_location.index(click_coord)
                                captured_pieces_black.append(white_pieces[white_piece])
                                if white_pieces[white_piece] == 'king':
                                    winner = "Black"
                                    running = False
                                white_pieces.pop(white_piece)
                                white_location.pop(white_piece)
                            last_pawn_move = (old_location, click_coord, 'black')
                        
                        if click_coord[1] == 0:
                            promotion_pending = True
                            promotion_piece_index = selection
                            promotion_color = 'black'
                    
                    elif black_pieces[selection] == 'rook':
                        if old_location == (7, 7):
                            black_rook_moved[1] = True
                        elif old_location == (0, 7):
                            black_rook_moved[0] = True
                        
                        if click_coord in white_location:
                            white_piece = white_location.index(click_coord)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = "Black"
                                running = False
                            white_pieces.pop(white_piece)
                            white_location.pop(white_piece)
                    
                    elif black_pieces[selection] == 'king':
                        black_king_moved = True
                        if click_coord == (6, 7) or click_coord == (2, 7):
                            handle_castling(old_location, click_coord, 'black')
                        elif click_coord in white_location:
                            white_piece = white_location.index(click_coord)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = "Black"
                                running = False
                            white_pieces.pop(white_piece)
                            white_location.pop(white_piece)
                    
                    else:
                        if click_coord in white_location:
                            white_piece = white_location.index(click_coord)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = "Black"
                                running = False
                            white_pieces.pop(white_piece)
                            white_location.pop(white_piece)
                    
                    turn_step = 0
                    selection = 100
                    valid_moves = []
    
    pygame.display.flip()

pygame.quit()
