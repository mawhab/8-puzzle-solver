import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, screen, position, text, size, colors):
        super().__init__()
        self.screen = screen
        self.colors = colors
        self.fg, self.bg, self.hoverc, self.blockedc = self.colors
        self.font = pygame.font.SysFont("Arial", size)
        self.text_render = self.font.render(text, True, self.fg)
        self.image = self.text_render
        self.x, self.y, self.w, self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.position = position
        self.ishovered = False
        self.isblocked = False
        self.func = None
        self.update()
        
    def update(self):
        self.fg, self.bg, self.hoverc, self.blockedc = self.colors
        if self.isblocked:
            bg = self.blockedc
        elif self.ishovered:
            bg = self.hoverc
        else:
            bg = self.bg
        pygame.draw.line(self.screen, (150, 150, 150), (self.x, self.y), (self.x + self.w , self.y), 5)
        pygame.draw.line(self.screen, (150, 150, 150), (self.x, self.y - 2), (self.x, self.y + self.h), 5)
        pygame.draw.line(self.screen, (50, 50, 50), (self.x, self.y + self.h), (self.x + self.w , self.y + self.h), 5)
        pygame.draw.line(self.screen, (50, 50, 50), (self.x + self.w , self.y + self.h), [self.x + self.w , self.y], 5)
        pygame.draw.rect(self.screen, bg, (self.x, self.y, self.w , self.h))

    def hover(self):
        self.ishovered=True

    def not_hover(self):
        self.ishovered = False

    def block(self):
        self.isblocked = True

    def unblock(self):
        self.isblocked = False

    def cb(self):
        if self.func:
            self.func()

    def set_cb(self, func):
        self.func = func
        return self

    