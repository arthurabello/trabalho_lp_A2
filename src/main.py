import pygame

pygame.init()
m = 10
n = 21
initial_width = n * 40
initial_height = m * 40
color_light_green = (144, 238, 144)
color_dark_green = (0, 100, 0)
color_red = (255, 0, 0)

screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
pygame.display.set_caption("The Art of Violence")

def get_square_from_click(mouse_pos):
    x, y = mouse_pos
    width, height = screen.get_size()
    square_width = width // n
    square_height = height // m
    column = x // square_width
    row = y // square_height
    return row, column

def draw_board(selected_square=None):
    width, height = screen.get_size()
    square_width = width // n
    square_height = height // m
    
    for row in range(m):
        for column in range(n):
            if (row + column) % 2 == 0:
                color = color_light_green
            else:
                color = color_dark_green
            
            if selected_square and (row, column) == selected_square:
                color = color_red
            
            pygame.draw.rect(screen, color, 
                           (column * square_width, row * square_height, square_width, square_height))

running = True
selected_square = None
fullscreen = False
current_size = [initial_width, initial_height]
resizing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                selected_square = get_square_from_click(mouse_position)
                print(f"Selected square: row {selected_square[0]}, column {selected_square[1]}")
                
        elif event.type == pygame.VIDEORESIZE:
            resizing = True
            current_size = [event.w, event.h]
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    current_size = screen.get_size()  
                else:
                    screen = pygame.display.set_mode(current_size, pygame.RESIZABLE)
    
    if resizing:
        screen = pygame.display.set_mode(current_size, pygame.RESIZABLE)
        resizing = False
    
    screen.fill((0, 0, 0))
    draw_board(selected_square)
    pygame.display.flip()

pygame.quit()
