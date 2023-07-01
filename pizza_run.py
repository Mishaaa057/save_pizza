# THE IDEA:
# Simple running game
# Player controlls pizza and running from pineapples.
# DON'T LET PINEAPPLE GET INTO PIZZA!...

import pygame
from sys import exit
from random import randint

# VARIABLES
SCREEN_W = 800
SCREEN_H = 400
FPS = 60


class Pizza(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("graphics/empty_pizza.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (SCREEN_W//2, 300))
        self.pizza_speed = 5
        self.gravity = 0
        self.maks = pygame.mask.from_surface(self.image)
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.1)
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0
        

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.pizza_speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.pizza_speed
        
        if keys[pygame.K_SPACE]:
            if self.rect.bottom >= 300:
                self.gravity -= 20
                self.jump_sound.play()

    def update(self):
        self.apply_gravity()
        self.movement()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, direction = "left", spawn_y = 300):
        super().__init__()
        self.pineapple_speed = 7
        self.direction = direction
        if self.direction == "left":
            spawn_x = randint(900, 1100)
            
        else:
            spawn_x = randint(-400, -100)
            self.pineapple_speed *= -1
            

        self.image = pygame.image.load("graphics/pineapple.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom = (spawn_x, spawn_y))
        
    def update(self):
        self.rect.x -= self.pineapple_speed
        if self.direction == 'left':
            if self.rect.x < -100:
                self.kill()
        else:
            if self.rect.x > SCREEN_W + 100:
                self.kill()


def display_score(screen, font, start_time):
    current_time = pygame.time.get_ticks() - start_time
    current_time = current_time // 1000

    # Display using text surface
    score_surf = font.render(f"Score: {current_time}", False, "Black")
    score_rect = score_surf.get_rect(midbottom = (SCREEN_W//2, 40))
    screen.blit(score_surf, score_rect)
    
    return current_time


def collision(pizza, pineapple):
    if pygame.sprite.spritecollide(pizza.sprite, pineapple, False, collided=pygame.sprite.collide_mask):
        return True
    return False


def main():
    pygame.init()
    GAME_ACTIVE = False
    score = 0

    start_time = pygame.time.get_ticks()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    pygame.display.set_caption("SAVE PIZZA")
    clock = pygame.time.Clock()

    # Text
    font = pygame.font.Font("font/Pixeltype.ttf", 50)
    text = """GAME OVER: Pineapple got into pizza..."""
    end_surf = font.render(text, False, "White")
    end_rect = end_surf.get_rect(midbottom = (SCREEN_W//2, 40))
    start_surf = font.render("DON'T LET PINEAPPLE TO GET INTO PIZZA", False, "White")
    start_rect = start_surf.get_rect(midbottom = (SCREEN_W//2, 40))
    
    # Music 
    music = pygame.mixer.Sound("audio/music.wav")
    music.set_volume(0.2)
    music.play(loops=-1)    

    # Import images
    sky_surf = pygame.image.load('graphics/sky.png').convert()
    ground_surf = pygame.image.load('graphics/ground.png').convert()

    # Groups
    pizza = pygame.sprite.GroupSingle()
    pizza.add(Pizza())

    pineapple = pygame.sprite.Group()

    # Timers
    pineapple_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pineapple_timer, 700)


    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if GAME_ACTIVE:
                if event.type == pineapple_timer:
                    y = 300
                    dir = 'left'
                    if randint(0, 1):
                        dir = 'right'
                    if randint(0, 3) == 3:
                        y = 220
                    pineapple.add(Obstacle(direction=dir, spawn_y=y))
                    
                    

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        GAME_ACTIVE = True
                        start_time = pygame.time.get_ticks()


        if GAME_ACTIVE:

            # Place sky and ground
            screen.blit(sky_surf, (0, 0))
            screen.blit(ground_surf, (0, 300))

            # DRAW
            pizza.update()
            pizza.draw(screen)
            pineapple.draw(screen)
            pineapple.update()
            

            # Check for Endgame
            if collision(pizza, pineapple):
                GAME_ACTIVE = False
                pineapple.empty()

            # Display score
            score = display_score(screen, font, start_time)

        else: # ENDGAME
            screen.fill((145, 148, 106))
            
            if score: # not first game
                screen.blit(end_surf, end_rect)
                score_surf = font.render(f"Score: {score}", False, "Black")
                score_rect = score_surf.get_rect(midbottom = (SCREEN_W // 2, 250))
                screen.blit(score_surf, score_rect)
                
            else:
                screen.blit(start_surf, start_rect)
                
        pygame.display.update()


if __name__=="__main__":
    main()
