
import pygame
pygame.init()  
WIDTH, HEIGHT = 1000, 900
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
timer = pygame.time.Clock()

#game pieces and their locations
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

turn_step = 0
selection = 100
valid_moves = []

#load in game piece images
#black pieces
black_rook = pygame.image.load("pieces/black rook.png")
black_rook = pygame.transform.scale(black_rook, (75, 75))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_queen = pygame.image.load("pieces/black queen.png")
black_queen = pygame.transform.scale(black_queen, (75, 75))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load("pieces/black king.png")
black_king = pygame.transform.scale(black_king, (75, 75))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_bishop = pygame.image.load("pieces/black bishop.png")
black_bishop = pygame.transform.scale(black_bishop, (75, 75))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load("pieces/black knight.png")
black_knight = pygame.transform.scale(black_knight, (75, 75))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load("pieces/black pawn.png")
black_pawn = pygame.transform.scale(black_pawn, (75, 75))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))


black_images = [black_rook, black_knight, black_bishop, black_queen, black_king, black_pawn]
black_images_small = [black_rook_small, black_knight_small, black_bishop_small, black_queen_small, black_king_small, black_pawn_small]

#white pieces
white_rook = pygame.image.load("pieces/white rook.png")
white_rook = pygame.transform.scale(white_rook, (75, 75))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_queen = pygame.image.load("pieces/white queen.png")
white_queen = pygame.transform.scale(white_queen, (75, 75))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load("pieces/white king.png")
white_king = pygame.transform.scale(white_king, (75, 75))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_bishop = pygame.image.load("pieces/white bishop.png")
white_bishop = pygame.transform.scale(white_bishop, (75, 75))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load("pieces/white knight.png")
white_knight = pygame.transform.scale(white_knight, (75, 75))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load("pieces/white pawn.png")
white_pawn = pygame.transform.scale(white_pawn, (75, 75))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_rook, white_knight, white_bishop, white_queen, white_king, white_pawn]
white_images_small = [white_rook_small, white_knight_small, white_bishop_small, white_queen_small, white_king_small, white_pawn_small]

piece_list = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']  

#check variables / Flashing counter
counter = 0
winner = ""


#draw the chess board
def draw_board():
    square_size = 100
    
    # Draw the 8x8 board
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = (240, 240, 240)  # light gray
            else:
                color = (100, 100, 100)  # dark gray
            
            pygame.draw.rect(
                screen,
                color,
                (col * square_size, row * square_size, square_size, square_size)
            )
    
    # Draw status bar
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
    status_text = ["White: Select a piece to move", "White: Select a square", "Black: Select a piece to move", "Black: Select a square"]
    status_surface = font.render(status_text[turn_step], True, 'black')
    screen.blit(status_surface, (20, 820))

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (white_location[i][0] * 100 + 12, white_location[i][1] * 100 + 12))
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', (white_location[i][0] * 100 + 1, white_location[i][1] * 100 + 1, 100, 100), 2)
    
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (black_location[i][0] * 100 + 12, black_location[i][1] * 100 + 12))
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'red', (black_location[i][0] * 100 + 1, black_location[i][1] * 100 + 1, 100, 100), 2)

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
        if (position[0], position[1] + 1) not in white_location and \
            (position[0], position[1] + 1) not in black_location and position[1] + 1 < 8:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_location and \
            (position[0], position[1] + 2) not in black_location and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_location:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_location:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_location and \
            (position[0], position[1] - 1) not in black_location and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_location and \
            (position[0], position[1] - 2) not in black_location and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_location:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_location:
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
    for i in range(4): #up, down, left, right
        path = True
        chain = 1
        if i == 0: #up
            x = 0
            y = 1
        elif i == 1: #down
            x = 0
            y = -1
        elif i == 2: #left
            x = -1
            y = 0
        else: #right
            x = 1
            y = 0
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
        enemies_list = black_location
        friends_list = white_location
    else:
        enemies_list = white_location
        friends_list = black_location
    moves_list = []
    for i in range(8):
        if i == 0:
            x = 1
            y = 2
        elif i == 1:
            x = 1
            y = -2
        elif i == 2:
            x = -1
            y = 2
        elif i == 3:
            x = -1
            y = -2
        elif i == 4:
            x = 2
            y = 1
        elif i == 5:
            x = 2
            y = -1
        elif i == 6:
            x = -2
            y = 1
        else:
            x = -2
            y = -1
        
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
    for i in range(4): #up right, up left, down right, down left
        path = True
        chain = 1
        if i == 0: #up right
            x = 1
            y = 1
        elif i == 1: #up left
            x = -1
            y = 1
        elif i == 2: #down right
            x = 1
            y = -1
        else: #down left
            x = -1
            y = -1
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
    # Combine rook and bishop moves
    moves_list.extend(check_rook(position, color_str))
    moves_list.extend(check_bishop(position, color_str))
    return moves_list

def check_king(position, color_str):
    moves_list = []
    # Combine rook and bishop moves but only 1 square away
    for move in check_rook(position, color_str):
        if abs(move[0] - position[0]) <= 1 and abs(move[1] - position[1]) <= 1:
            moves_list.append(move)
    for move in check_bishop(position, color_str):
        if abs(move[0] - position[0]) <= 1 and abs(move[1] - position[1]) <= 1:
            moves_list.append(move)
    return moves_list

def check_valid_moves():
    if turn_step < 2:
        valid_options = check_options(white_pieces, white_location, 'white')[selection]
    else:
        valid_options = check_options(black_pieces, black_location, 'black')[selection]
    return valid_options

def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(black_images_small[index], (825, 5 + i * 50))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(white_images_small[index], (825, 5 + i * 50))

def draw_check():
    if turn_step < 2:
        king_location = white_location[white_pieces.index('king')]
        for i in range(len(black_pieces)):
            moves = check_options(black_pieces, black_location, 'black')[i]
            if king_location in moves:
                if counter < 15:
                    pygame.draw.rect(screen, 'dark red', (king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100), 5)
    else:
        king_location = black_location[black_pieces.index('king')]
        for i in range(len(white_pieces)):
            moves = check_options(white_pieces, white_location, 'white')[i]
            if king_location in moves:
                if counter < 15:
                    pygame.draw.rect(screen, 'dark blue', (king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100), 5)

#main game loop
running = True
while running:
    timer.tick(FPS)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill((255, 255, 255))
    draw_board()
    draw_pieces()
    draw_captured()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    #for event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            col = mouse_pos[0] // 100
            row = mouse_pos[1] // 100
            click_coord = (col, row)

            if turn_step == 0:
                if click_coord in white_location:
                    selection = white_location.index(click_coord)
                    turn_step = 1
            if turn_step == 1:
                if click_coord in valid_moves and selection != 100:
                    white_location[selection] = click_coord
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
            if turn_step == 2:
                if click_coord in black_location:
                    selection = black_location.index(click_coord)
                    turn_step = 3
            if turn_step == 3:
                if click_coord in valid_moves and selection != 100:
                    black_location[selection] = click_coord
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