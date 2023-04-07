import pygame
import math
from sys import exit;
from random import choice
pygame.init();

# SETUP
W = 800;
H = 500;
screen = pygame.display.set_mode((W, H));
screen.fill("black");

clock = pygame.time.Clock();
FPS = 60;
matchFinished = False;
whoWon = "";

def DrawWireframe():
    pygame.draw.line(screen, "white", (W / 2, 0), (W / 2, H), 10)
    for i in range(30):
        pygame.draw.line(screen, "black", (0, i * 10 * 2), (W, i * 10 * 2), 10);

def RestartRally(madePoint):
    # if(madePoint == 1):
    #     paddle.sprites()[1].score += 1;
    # else: paddle.sprites()[0].score += 1;
    paddle.sprites()[madePoint].score += 1;
    print(f"pos: {paddle.sprites()[madePoint].rect.x} - score: {paddle.sprites()[madePoint].score}")
    
    for p in paddle.sprites():
        p.rect.y = (500 / 2) - 50;

def OnWin():
    global matchFinished;
    matchFinished = True;
    print(f"{whoWon} won")

def RestartGame():
    global matchFinished, whoWon;

    matchFinished = False;
    whoWon = "";
    for p in paddle.sprites():
        p.rect.y = (500 / 2) - 50;
        p.score = 0;

def MatchEnd():
    textSurf = text.render(f"{whoWon} won", False, "white");
    textRect = textSurf.get_rect(center = (W / 2, H / 2))
    pygame.draw.rect(screen, "black", (textRect.x - 10, textRect.y, textRect.width + 20, 50));
    screen.blit(textSurf, textRect);

    RestartSurf = Restarttext.render(f"press R to restart", False, "white");
    restartRect = RestartSurf.get_rect(center = (400, 350))
    pygame.draw.rect(screen, "black", (restartRect.x - 10, restartRect.y - 20, restartRect.width + 20, 50));
    screen.blit(RestartSurf, restartRect);


# SPRITES
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__();
        self.w = 25
        self.image = pygame.Surface((self.w, self.w));
        self.image.fill("white");
        self.rect = self.image.get_rect(center = (W / 2, H/2));
        self.senseX = choice([1,-1]);
        self.senseY = -1;
        self.speed = (4,4)
    
    def move(self):
        # x = self.rect.x;
        y = self.rect.y;
        speed = self.speed;
        sense = self.senseX;

        if(y > 475 or y < 0):
            self.senseY *= -1;
        self.rect.x += speed[0] * sense;
        self.rect.y += speed[1] * self.senseY;
    
    def CheckCollision(self, paddle):
        if(pygame.sprite.spritecollide(self,paddle, False)):
            if(self.senseX == 1):
                self.senseX = -1;
            elif(self.senseX == -1):
                self.senseX = 1;
            self.speed = (self.speed[0] + 0.2, self.speed[1])

    def CheckEnd(self , callback):
        x = self.rect.x;
        madePoint = None
        
        if(x >= 775 or x < 0):
            if(x >= 775):
                madePoint = 1
            elif(x < 0):
                madePoint = 0;
            self.RestartPos();
            callback(madePoint);
    
    def RestartPos(self):
        self.rect.x = W / 2;
        self.rect.y = H / 2;
        self.senseX = choice([1,-1]);
        self.speed = (4,4);
    
    def update(self, paddle, rallycallback):
        self.move();
        self.CheckCollision(paddle);
        self.CheckEnd(rallycallback);

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, type):
        super().__init__();
        self.surface = pygame.Surface((25,100));
        self.surface.fill("white");
        self.image = self.surface ;
        self.rect = self.image.get_rect(center = (x,H /2))
        self.sense = 0;
        self.speed = 4;
        self.score = 0;
        self.type = type;
        # print(f"pos: {self.rect.x} - type: {self.type}")

    def move(self, ballPos):
        if(self.rect.y > 400): self.rect.y = H - self.rect.height;
        if(self.rect.y < 0): self.rect.y = 0;

        if(self.type == "player"):
            self.rect.y += self.speed * self.sense;
        else:
            ballSense = 0;
            if(ballPos == self.rect.y):
                ballSense = 0;
            else:
                if(self.rect.y > ballPos): ballSense = 1;
                elif(self.rect.y < ballPos): ballSense = -1;
            self.rect.y += self.speed * ballSense

    def CheckInput(self, events):
        for event in events:
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_DOWN):
                    self.sense = 1;
                if(event.key == pygame.K_UP):
                    self.sense = -1;
            if(event.type == pygame.KEYUP):
                self.sense = 0;
   
    def CheckScore(self, callback):
        global whoWon;
        # print(f"score: {self.score} - type: {self.type}");
        if(self.score >= 7):
            whoWon = self.type;
            callback();
    def update(self, events, ballPos, callback):
        self.CheckInput(events);
        self.move(ballPos);
        self.CheckScore(callback)

class ScoreText(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__();
        self.text = "0";
        self.font = pygame.font.Font("Assets/pixel.ttf", 120);
        self.image = self.font.render(self.text, False, "#ffffff");
        self.rect = self.image.get_rect(center = (x,120))
    def update(self, score):
        self.text = str(score);
        self.image = self.font.render(str(score), False, "#ffffff");


# OBJECTS
ball = pygame.sprite.GroupSingle();
ball.add(Ball());

paddle = pygame.sprite.Group();
paddle.add(Paddle(750, "bot"));
paddle.add(Paddle(50, "player"));

scoreText = pygame.sprite.Group();
scoreText.add(ScoreText(200));
scoreText.add(ScoreText(600));

text = pygame.font.Font("Assets/pixel.ttf", 90);
Restarttext = pygame.font.Font("Assets/pixel.ttf", 40);


# GAME LOOP
while True:
    events = pygame.event.get();
    screen.fill("black");

    for event in events:
        if(event.type == pygame.QUIT):
            pygame.quit();
            exit();
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_r):
                RestartGame();
    
    DrawWireframe();
    scoreText.draw(screen);
    scoreText.sprites()[0].update(paddle.sprites()[1].score);
    scoreText.sprites()[1].update(paddle.sprites()[0].score);

    if(matchFinished == False):
        ball.update(paddle, RestartRally);
        ball.draw(screen);

    if(matchFinished == False):
        paddle.update(events, ball.sprites()[0].rect.y, OnWin);
    paddle.draw(screen);
    
    if(matchFinished == True):     
        MatchEnd();

    pygame.display.update();
    clock.tick(FPS);