import pygame
import sys

def visual(riwayat):
    pygame.init()
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualisasi Jalur Labirin")
    font = pygame.font.SysFont(None, 30)
    clock = pygame.time.Clock()

    posisi_node = {
        'IN': (400, 50),
        'B1': (400, 150),
        'S1': (300, 150),
        'S2': (300, 250),
        'L1': (500, 150),
        'L2': (500, 250),
        'L3': (500, 350),
        'OUT': (400, 250)
    }

    jalur = [
        ('IN', 'B1'), ('IN', 'S1'),
        ('B1', 'OUT'),
        ('S1', 'S2'), ('S1', 'L1'),
        ('S2', 'OUT'), ('S2', 'L1'),
        ('L1', 'L2'), ('L2', 'L3'), ('L3', 'OUT'),
        ('L1', 'L1'), ('L2', 'L1'), ('L3', 'L2')  
    ]

    running = True
    while running:
        screen.fill((30, 30, 30))

        for i in range(len(riwayat) - 1):
            a, b = riwayat[i], riwayat[i + 1]
            if a in posisi_node and b in posisi_node:
                pygame.draw.line(screen, (200, 200, 200), posisi_node[a], posisi_node[b], 3)

        for i, node in enumerate(riwayat):
            if node in posisi_node:
                x, y = posisi_node[node]
                color = (0, 255, 0) if i == len(riwayat) - 1 else (100, 100, 255)
                pygame.draw.circle(screen, color, (x, y), 30)
                text = font.render(node, True, (255, 255, 255))
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False

    pygame.quit()
