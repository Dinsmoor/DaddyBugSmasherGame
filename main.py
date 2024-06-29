import pygame
import random
import math

WIDTH = 640
HEIGHT = 480

FPS = 45

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Daddy Bug Smasher")
clock = pygame.time.Clock()

def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image.set_colorkey(colorkey)
    return image.convert_alpha()

def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

def play_music(music_file):
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.6)

def taunt_player():
    tauntings = ['1','2','3','4']
    play_sound(f"dialog/taunt{random.choice(tauntings)}.wav")

# Define classes here
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.going_right = load_image("sprites/daddy2.png")
        self.going_left = pygame.transform.flip(self.going_right, True, False)
        self.image = self.going_right
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.x_vel = 0
        self.y_vel = 0
        self.is_jumping = False
        self.facing = 'left'
        self.hammer = Hammer()
        self.swinging_weapon = False
        self.weapon_offset = (40, 5)


    def update(self):
        self.x_vel = 0
        self.swinging_weapon = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x_vel = 5
            self.facing = 'right'
        if keys[pygame.K_a]:
            self.x_vel = -5 
            self.facing = 'left'
        if keys[pygame.K_SPACE]:
            self.swinging_weapon = True
            self.hammer.update()
        
        if self.facing == 'left':
            self.image = self.going_left
        else:
            self.image = self.going_right


        if keys[pygame.K_w] and not self.is_jumping:
            self.y_vel = -10
            self.is_jumping = True
            jump_sounds = ['sfx/jump1.wav', 'sfx/jump2.wav']
            play_sound(random.choice(jump_sounds))

        self.y_vel += 0.5
        if self.y_vel > 10:
            self.y_vel = 10

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Check for collisions with walls (replace with actual collision logic)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
            self.is_jumping = False
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        self.hammer.rect.center = (self.rect.centerx + self.weapon_offset[0],
                                    self.rect.centery + self.weapon_offset[1])

class BugMaster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_list = ['sprites/master1.png', 'sprites/master2.png']
        self.image = load_image(self.image_list[0])
        self.rect = self.image.get_rect()

    def update(self):
        pass

class Hammer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("sprites/hammer.png")
        self.rect = self.image.get_rect()
        self.center = (WIDTH // 2, 0)  # Center of rotation

    def update(self):
        pass

class Bug(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bug_sprites = ['bug11','bug21', 'bug31','bug41','bug51','bug61']
        flying_bugs = ['bug31', 'bug41']
        this_bug_sprite = random.choice(bug_sprites)
        self.image = load_image(f"sprites/{this_bug_sprite}.png")  # Replace with your enemy image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 100)  # Spawn off screen
        self.rect.y = HEIGHT - self.rect.height  # Spawn between ground and up high
        if this_bug_sprite in flying_bugs:
            self.rect.y = random.randrange(280,320)
        self.x_vel = random.uniform(-0.2, -3)  # Move left
        self.pointvalue = 0
        global score


    def update(self):
        global score
        self.rect.x += self.x_vel + random.uniform(-0.1, -1) # vary the travel rate

        # Check if enemy went off screen
        if self.rect.right < 0:
            score += -1
            if random.randrange(0, 2) == 0:
                taunt_player()
            self.kill()

        if pygame.sprite.collide_rect(self, player.hammer) and player.swinging_weapon:
            score += 1
            death_sounds = ['sfx/death1.wav', 'sfx/death2.wav', 'sfx/death3.wav']
            play_sound(random.choice(death_sounds))
            self.kill()

class CloudSprite(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed  # Speed of movement (pixels per frame)
        self.screen_width = pygame.display.get_surface().get_width()  # Get screen width

    def update(self):
        # Move the cloud from right to left
        self.rect.x -= self.speed

        # If the cloud goes off screen, reset its position on the right side
        if self.rect.right < 0:
            self.rect.left = self.screen_width

def get_current_game_seconds(frame):
    return int(frame/FPS)


player = Player()
enemies = pygame.sprite.Group()
bugmaster = BugMaster()

font = pygame.font.Font(None, 32)

intro_image = load_image("background.png")
intro_sound = pygame.mixer.Sound("dialog/bugmaster_intro.wav")
win_sound = pygame.mixer.Sound("dialog/bugmaster_win.wav")
lose_sound = pygame.mixer.Sound("dialog/bugmaster_lose.wav")
intro_playing = True

# Main loop
running = True
frame = 0
music_playing = False
last_second = 0

# global (ew)
score = 0

skip = False
restart = False

if skip: frame = 400

while running:
    clock.tick(FPS)
    frame += 1
    game_seconds = get_current_game_seconds(frame)
    if game_seconds != last_second:
        last_second = game_seconds
        print(f'time: {game_seconds}')

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if frame < 2:
        intro_sound.play()
    if 2<= frame <= 10*FPS:
        screen.blit(intro_image, (0, 0))
        screen.blit(bugmaster.image, (450, 25))
        pygame.display.flip()
    if game_seconds < 10:
        continue
    if (game_seconds == 11) and (not music_playing):
        play_music('music/combat.wav')

    # Main game logic (after intro)
    else:
        # Update player
        player.update()

        # Spawn enemies (replace with logic for spawning)
        if random.randrange(0, 200) < 2:
            enemies.add(Bug())

        # Update enemies
        enemies.update()
        bugmaster.update()

        # Draw sprites
        screen.blit(intro_image, (0, 0))
        screen.blit(player.image, player.rect)
        screen.blit(bugmaster.image, (450, 25))
        enemies.draw(screen)

        if player.swinging_weapon:
            screen.blit(player.hammer.image, player.hammer.rect)
        else:
            player.hammer.kill()

        text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect = (20, 50)
        screen.blit(text_surface, text_rect)

        win_surface = font.render("Defeat the Bugmaster. 10 points to win, -5 points to loose", True, (0, 0, 0))
        win_rect = win_surface.get_rect()
        win_rect = (20, 10)
        screen.blit(win_surface, win_rect)

        # Update the display
        pygame.display.flip()

        if score >= 10:
            print("win")
            win_sound.play()
            pygame.mixer.music.stop()
            play_music("music/win.wav")
            pygame.time.wait(15000)
            pygame.mixer.music.stop()
            restart = True
            
        if score <= -5:
            print("lose")
            lose_sound.play()
            pygame.mixer.music.stop()
            play_music("music/lose.wav")
            pygame.time.wait(15000)
            pygame.mixer.music.stop()
            restart = True
        
        if restart:
            enemies.empty()
            score = 0
            frame = 0
            restart = False
    

pygame.quit()
