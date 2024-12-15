import pygame
import catch_up
from random import randint
pygame.font.init()
window = pygame.display.set_mode((800, 500))
fps = pygame.time.Clock()
fon = pygame.image.load("fon.jpg")
fon = pygame.transform.scale(fon,(800, 500))

button_rect = pygame.Rect(300, 200, 200, 50)
button_exit = pygame.Rect(300, 270, 200, 50)
font = pygame.font.Font(None, 35)
bed = pygame.font.Font(None, 35).render('Начать игру', True, (255,255,255))
exit_b = pygame.font.Font(None, 35).render('Выход', True, (255,255,255))

instruction_font = pygame.font.Font(None, 25)  # Меньший шрифт
instruction1 = instruction_font.render('A D - ходьба', True, (255, 255, 255))
instruction2 = instruction_font.render('Space - прыжок', True, (255, 255, 255))
instruction3 = instruction_font.render('R - выстрел', True, (255, 255, 255))

run = True
while run:
    window.blit(fon,(0, 0))
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    catch_up.main()
           
                    pygame.quit()
                elif button_exit.collidepoint(event.pos):
                    running = False
                    pygame.quit()
    
    pygame.draw.rect(window, (22, 66, 168),button_rect)
    pygame.draw.rect(window, (22, 66, 168),button_exit)
    window.blit(bed,(325, 210))
    window.blit(exit_b,(350, 280))
    window.blit(instruction1, (10, 420))
    window.blit(instruction2, (10, 450))
    window.blit(instruction3, (10, 580))

    
    pygame.display.update()
    fps.tick(60)