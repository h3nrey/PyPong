import pygame
from sys import exit;

W = 800;
H = 500;
screen = pygame.display.set_mode((W, H));
screen.fill("black");

clock = pygame.time.Clock();
FPS = 60;

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__();
        self.w = 25
        self.image = pygame.Surface((self.w, self.w));
        self.image.fill("white");
        self.rect = self.image.get_rect(center = (W / 2, H/2));

ball = pygame.sprite.GroupSingle();
ball.add(Ball());

while True:
    events = pygame.event.get();

    for event in events:
        if(event.type == pygame.QUIT):
            pygame.quit();
            exit();
    
    ball.draw(screen);
    pygame.display.update();
    clock.tick(FPS);