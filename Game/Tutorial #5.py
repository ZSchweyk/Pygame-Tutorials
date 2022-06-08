import random

import pygame
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()


class Player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 13
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
                


class Projectile(object):
    bullets = []
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = -13
        self.bullets.append(self)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)



class Ball:
    max_balls = 4
    balls = []

    def __init__(self, x, radius, color):
        self.x = random.choice([0, 480-2*radius])
        self.y = 0
        self.radius = radius
        self.color = color
        self.vel_x = 3 if self.x == 0 else -3
        self.vel_y = 0
        self.accel = -9.8
        self.balls.append(self)

    def draw(self, win):

        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)



def redrawGameWindow():
    win.blit(bg, (0,0))

    man.draw(win)

    for bullet in Projectile.bullets:
        bullet.draw(win)

    for ball in Ball.balls:
        ball.draw(win)

    
    pygame.display.update()


#mainloop
man = Player(200, 410, 64, 64)
run = True
while run:
    clock.tick(27)
    if len(Ball.balls) < Ball.max_balls:
        Ball.balls.append(Ball(0, 18, (255, 0, 0)))

    for ball in Ball.balls:
        ball.y += ball.accel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    for bullet in Projectile.bullets:
        if bullet.y > 0:
            bullet.y += bullet.vel
        else:
            Projectile.bullets.pop(Projectile.bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        Projectile.bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + 3), 6, (0, 0, 0)))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()


