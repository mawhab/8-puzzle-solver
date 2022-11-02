from Button import *
import pygame

pygame.init()

screen = pygame.display.set_mode((600,400))

colors = [(255,255,255),
          (0,0,0),
          (128,128,128)]
b0 = Button(screen, (10,10), "alloo", 55, colors)
b1 = Button(screen, (100,100), "alloo111", 55, colors)

buttons = pygame.sprite.Group()

buttons.add(b0)
buttons.add(b1)
buttons.update()
buttons.draw(screen)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            for btn in buttons:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    btn.hover()
                else:
                    btn.not_hover()

    buttons.update()
    buttons.draw(screen)
    pygame.display.update()