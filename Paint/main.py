import pygame

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

clock = pygame.time.Clock()

#  STATE 
tool = "brush"
color = (0, 0, 255)
radius = 6

drawing = False
start_pos = (0, 0)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((0, 0, 0))

#  BUTTONS 
buttons = {
    "brush": pygame.Rect(10, 10, 70, 30),
    "rect": pygame.Rect(90, 10, 70, 30),
    "circle": pygame.Rect(170, 10, 70, 30),
    "eraser": pygame.Rect(250, 10, 70, 30),
}

colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

color_buttons = {
    "red": pygame.Rect(360, 10, 30, 30),
    "green": pygame.Rect(400, 10, 30, 30),
    "blue": pygame.Rect(440, 10, 30, 30),
}

# DRAWING BUTTONS
def draw_button(rect, text, active=False):
    pygame.draw.rect(screen, (150, 150, 150) if active else (70, 70, 70), rect)
    font = pygame.font.SysFont(None, 20)
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (rect.x + 5, rect.y + 7))

def draw_color(rect, col, active=False):
    pygame.draw.rect(screen, col, rect)
    if active:
        pygame.draw.rect(screen, (255, 255, 255), rect, 3)

# MAIN LOOP 
running = True

while running:
    screen.fill((30, 30, 30))
    screen.blit(canvas, (0, 0))

    # Buttons
    for name, rect in buttons.items():
        draw_button(rect, name, tool == name)

    for name, rect in color_buttons.items():
        draw_color(rect, colors[name], color == colors[name])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #  click 
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # tools
            for name, rect in buttons.items():
                if rect.collidepoint(mx, my):
                    tool = name

            # colors
            for name, rect in color_buttons.items():
                if rect.collidepoint(mx, my):
                    color = colors[name]

            if my > 60:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos

                # rectangle 
                if tool == "rect":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(start_pos[0] - end_pos[0])
                    h = abs(start_pos[1] - end_pos[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h))

                # circle
                if tool == "circle":
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    r = int((dx**2 + dy**2) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, r)

            drawing = False

        # brush
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "brush":
                    pygame.draw.circle(canvas, color, event.pos, radius)

                if tool == "eraser":
                    pygame.draw.circle(canvas, (0, 0, 0), event.pos, radius * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()