import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game constants
# Get the screen info for fullscreen
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (218, 165, 32)
TURQUOISE = (64, 224, 208)
SANDSTONE = (194, 178, 128)
RED = (220, 20, 60)

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = GOLD
PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = -15  # Increased jump strength

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.health = 100
        self.attacking = False
        self.attack_cooldown = 0

    def move(self, dx, dy):
        # Update facing direction
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

        # Move the player
        self.rect.x += dx

        # Keep player within screen bounds - extended for wider level
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH * 3:  # Extended world boundary
            self.rect.right = SCREEN_WIDTH * 3

        # Apply vertical movement
        self.rect.y += dy

        # Simple ground collision
        if self.rect.bottom >= SCREEN_HEIGHT - 50:  # Ground level
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            # Add a small vertical movement to ensure we leave the ground
            self.rect.y -= 2

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_cooldown = 30  # Half a second at 60 FPS

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        # Cap falling speed to prevent getting stuck
        if self.velocity_y > 15:
            self.velocity_y = 15
        self.move(0, self.velocity_y)

        # Update attack state
        if self.attacking:
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                self.attacking = False
        elif self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, screen, camera_offset=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset

        # Draw player body
        pygame.draw.rect(screen, PLAYER_COLOR, adjusted_rect)

        # Draw eyes to indicate facing direction
        eye_size = 5
        if self.facing_right:
            pygame.draw.circle(screen, BLACK, (adjusted_rect.right - 10, adjusted_rect.top + 15), eye_size)
        else:
            pygame.draw.circle(screen, BLACK, (adjusted_rect.left + 10, adjusted_rect.top + 15), eye_size)

        # Draw attack animation if attacking
        if self.attacking:
            attack_width = 30
            attack_height = 10
            if self.facing_right:
                attack_rect = pygame.Rect(adjusted_rect.right, adjusted_rect.centery - attack_height//2,
                                         attack_width, attack_height)
            else:
                attack_rect = pygame.Rect(adjusted_rect.left - attack_width, adjusted_rect.centery - attack_height//2,
                                         attack_width, attack_height)
            pygame.draw.rect(screen, TURQUOISE, attack_rect)

        # Draw health bar
        health_bar_width = 40
        health_bar_height = 5
        health_rect = pygame.Rect(adjusted_rect.centerx - health_bar_width//2,
                                 adjusted_rect.top - 10,
                                 health_bar_width * (self.health/100),
                                 health_bar_height)
        pygame.draw.rect(screen, (255, 0, 0), health_rect)

class Enemy:
    def __init__(self, x, y, width=30, height=50, patrol_distance=100, enemy_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.enemy_type = enemy_type

        # Different enemy types with different colors and behaviors
        if enemy_type == "normal":
            self.color = RED
            self.speed = 2
            self.health = 50
        elif enemy_type == "fast":
            self.color = (255, 165, 0)  # Orange
            self.speed = 4
            self.health = 30
        elif enemy_type == "strong":
            self.color = (128, 0, 128)  # Purple
            self.speed = 1.5
            self.health = 100
        else:
            self.color = RED
            self.speed = 2
            self.health = 50

        self.direction = 1  # 1 for right, -1 for left
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.velocity_y = 0
        self.on_ground = False

    def update(self, platforms):
        # Move horizontally based on direction
        self.rect.x += self.speed * self.direction

        # Check patrol boundaries
        if self.rect.x > self.start_x + self.patrol_distance:
            self.direction = -1  # Change direction to left
        elif self.rect.x < self.start_x - self.patrol_distance:
            self.direction = 1   # Change direction to right

        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check platform collisions
        for platform in platforms:
            if (self.rect.bottom >= platform.rect.top and
                self.rect.bottom <= platform.rect.top + 10 and
                self.rect.right > platform.rect.left and
                self.rect.left < platform.rect.right and
                self.velocity_y > 0):
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.velocity_y = 0
                break
        else:
            self.on_ground = False

    def draw(self, screen, camera_offset):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset
        pygame.draw.rect(screen, self.color, adjusted_rect)

        # Draw eyes to indicate direction
        eye_size = 4
        if self.direction > 0:  # Facing right
            pygame.draw.circle(screen, BLACK, (adjusted_rect.right - 8, adjusted_rect.top + 12), eye_size)
        else:  # Facing left
            pygame.draw.circle(screen, BLACK, (adjusted_rect.left + 8, adjusted_rect.top + 12), eye_size)

        # Draw health bar
        health_bar_width = 30
        health_bar_height = 4
        health_rect = pygame.Rect(adjusted_rect.centerx - health_bar_width//2,
                                 adjusted_rect.top - 8,
                                 health_bar_width * (self.health/50),
                                 health_bar_height)
        pygame.draw.rect(screen, (255, 0, 0), health_rect)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = SANDSTONE

    def draw(self, screen, camera_offset=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset
        pygame.draw.rect(screen, self.color, adjusted_rect)

class Game:
    def __init__(self):
        # Set up fullscreen mode
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("King of Persia")
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_offset = 0
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

        # Create player
        self.player = Player(100, SCREEN_HEIGHT - 150)

        # Create platforms - adjusted for fullscreen with more platforms
        ground_height = 50
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH * 3, ground_height),  # Extended ground
            Platform(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 150, SCREEN_WIDTH * 0.15, 20),  # Platform 1
            Platform(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 200, SCREEN_WIDTH * 0.15, 20),   # Platform 2
            Platform(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 250, SCREEN_WIDTH * 0.15, 20),  # Platform 3
            Platform(SCREEN_WIDTH * 1.0, SCREEN_HEIGHT - 200, SCREEN_WIDTH * 0.2, 20),    # Platform 4
            Platform(SCREEN_WIDTH * 1.25, SCREEN_HEIGHT - 150, SCREEN_WIDTH * 0.15, 20),  # Platform 5
            Platform(SCREEN_WIDTH * 1.5, SCREEN_HEIGHT - 200, SCREEN_WIDTH * 0.18, 20),   # Platform 6
            # Additional platforms
            Platform(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT - 300, SCREEN_WIDTH * 0.1, 20),    # Platform 7
            Platform(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT - 350, SCREEN_WIDTH * 0.12, 20),   # Platform 8
            Platform(SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - 400, SCREEN_WIDTH * 0.1, 20),    # Platform 9
            Platform(SCREEN_WIDTH * 1.2, SCREEN_HEIGHT - 350, SCREEN_WIDTH * 0.12, 20),   # Platform 10
            Platform(SCREEN_WIDTH * 1.5, SCREEN_HEIGHT - 300, SCREEN_WIDTH * 0.1, 20),    # Platform 11
            Platform(SCREEN_WIDTH * 1.8, SCREEN_HEIGHT - 250, SCREEN_WIDTH * 0.15, 20),   # Platform 12
        ]

        # Create enemies - adjusted for fullscreen with more enemies and different types
        self.enemies = [
            # Normal enemies
            Enemy(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT - 200, patrol_distance=SCREEN_WIDTH * 0.1, enemy_type="normal"),
            Enemy(SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - 300, patrol_distance=SCREEN_WIDTH * 0.12, enemy_type="normal"),
            Enemy(SCREEN_WIDTH * 1.4, SCREEN_HEIGHT - 250, patrol_distance=SCREEN_WIDTH * 0.15, enemy_type="normal"),

            # Fast enemies
            Enemy(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT - 150, patrol_distance=SCREEN_WIDTH * 0.08, enemy_type="fast"),
            Enemy(SCREEN_WIDTH * 1.1, SCREEN_HEIGHT - 200, patrol_distance=SCREEN_WIDTH * 0.1, enemy_type="fast"),
            Enemy(SCREEN_WIDTH * 1.7, SCREEN_HEIGHT - 250, patrol_distance=SCREEN_WIDTH * 0.12, enemy_type="fast"),

            # Strong enemies
            Enemy(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT - 300, patrol_distance=SCREEN_WIDTH * 0.09, enemy_type="strong"),
            Enemy(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT - 150, patrol_distance=SCREEN_WIDTH * 0.11, enemy_type="strong"),
            Enemy(SCREEN_WIDTH * 1.2, SCREEN_HEIGHT - 300, patrol_distance=SCREEN_WIDTH * 0.13, enemy_type="strong"),

            # Additional enemies
            Enemy(SCREEN_WIDTH * 1.6, SCREEN_HEIGHT - 350, patrol_distance=SCREEN_WIDTH * 0.14, enemy_type="normal"),
            Enemy(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT - 400, patrol_distance=SCREEN_WIDTH * 0.1, enemy_type="fast"),
            Enemy(SCREEN_WIDTH * 1.9, SCREEN_HEIGHT - 150, patrol_distance=SCREEN_WIDTH * 0.15, enemy_type="strong")
        ]

        # Load background image (placeholder)
        self.bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg.fill((135, 206, 235))  # Sky blue background

        # Create decorative elements for Persian theme - adjusted for fullscreen
        self.decorations = []
        for i in range(20):  # More decorations for wider screen
            # Simple arch shapes
            x = i * (SCREEN_WIDTH * 0.1)
            self.decorations.append(pygame.Rect(x, SCREEN_HEIGHT - 300, SCREEN_WIDTH * 0.08, 80))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Changed to F key for jumping
                    self.player.jump()
                if event.key == pygame.K_SPACE:
                    self.player.attack()
                if event.key == pygame.K_ESCAPE:  # Add escape key to exit fullscreen
                    self.running = False

    def check_collisions(self):
        # Check for player-enemy collisions
        for enemy in self.enemies[:]:  # Use a copy to safely remove during iteration
            # Check if player is attacking and hitting enemy
            if self.player.attacking:
                attack_rect = pygame.Rect(0, 0, 0, 0)
                if self.player.facing_right:
                    attack_rect = pygame.Rect(self.player.rect.right,
                                             self.player.rect.centery - 5,
                                             30, 10)
                else:
                    attack_rect = pygame.Rect(self.player.rect.left - 30,
                                             self.player.rect.centery - 5,
                                             30, 10)

                if attack_rect.colliderect(enemy.rect):
                    # Different damage based on enemy type
                    if enemy.enemy_type == "normal":
                        enemy.health -= 25
                    elif enemy.enemy_type == "fast":
                        enemy.health -= 30  # Fast enemies are weaker
                    elif enemy.enemy_type == "strong":
                        enemy.health -= 15  # Strong enemies take less damage

                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        # Different score based on enemy type
                        if enemy.enemy_type == "normal":
                            self.score += 100
                        elif enemy.enemy_type == "fast":
                            self.score += 150
                        elif enemy.enemy_type == "strong":
                            self.score += 200

            # Check if enemy is hitting player
            elif self.player.rect.colliderect(enemy.rect):
                # Different damage based on enemy type
                if enemy.enemy_type == "normal":
                    self.player.health -= 1
                elif enemy.enemy_type == "fast":
                    self.player.health -= 2
                elif enemy.enemy_type == "strong":
                    self.player.health -= 3

                # Push player away from enemy
                if self.player.rect.centerx < enemy.rect.centerx:
                    self.player.rect.x -= 5
                else:
                    self.player.rect.x += 5

    def update(self):
        # Get keyboard state
        keys = pygame.key.get_pressed()

        # Handle horizontal movement
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED

        # Continuous jumping with F key
        if keys[pygame.K_f] and self.player.on_ground:
            self.player.jump()

        # Move player
        self.player.move(dx, 0)
        self.player.update()

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.platforms)

        # Check for collisions
        self.check_collisions()

        # Update camera offset to follow player
        target_offset = max(0, self.player.rect.x - SCREEN_WIDTH // 3)
        self.camera_offset = target_offset

        # Check platform collisions for player
        self.player.on_ground = False  # Reset ground state
        for platform in self.platforms:
            if (self.player.rect.bottom >= platform.rect.top and
                self.player.rect.bottom <= platform.rect.top + 15 and  # Increased collision tolerance
                self.player.rect.right > platform.rect.left and
                self.player.rect.left < platform.rect.right and
                self.player.velocity_y > 0):
                self.player.rect.bottom = platform.rect.top
                self.player.on_ground = True
                self.player.velocity_y = 0

        # Check game over condition
        if self.player.health <= 0:
            self.running = False
            print("Game Over! Your score:", self.score)

    def draw(self):
        # Draw background
        self.screen.blit(self.bg, (0, 0))

        # Draw decorative elements
        for decoration in self.decorations:
            adjusted_rect = decoration.copy()
            adjusted_rect.x -= self.camera_offset
            if 0 <= adjusted_rect.x <= SCREEN_WIDTH:
                pygame.draw.arc(self.screen, TURQUOISE, adjusted_rect, 0, 3.14, 3)

        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_offset)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_offset)

        # Draw player
        self.player.draw(self.screen, self.camera_offset)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

        # Draw health
        health_text = self.font.render(f"Health: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (20, 60))

        # Update display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
