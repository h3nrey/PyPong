import pygame
import math
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
        self.senseX = 1;
        self.senseY = -1;
        self.speed = 4;
    
    def move(self):
        x = self.rect.x;
        y = self.rect.y;
        speed = self.speed;
        sense = self.senseX;

        if(x >= 775):
            self.senseX = -1;
        elif(x < 0):
            self.senseX = 1;
        if(y > 475 or y < 0):
            self.senseY *= -1;
        self.rect.x += speed * sense;
        self.rect.y += speed * self.senseY;
    
    def update(self):
        self.move();

ball = pygame.sprite.GroupSingle();
ball.add(Ball());

while True:
    events = pygame.event.get();
    screen.fill("black");

    for event in events:
        if(event.type == pygame.QUIT):
            pygame.quit();
            exit();
    
    ball.update();
    ball.draw(screen);

    pygame.display.update();
    clock.tick(FPS);