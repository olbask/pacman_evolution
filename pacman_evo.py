import math
import random

import pygame

# Settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (0, 0, 0)
NUM_PACMANS = 100
NUM_GHOSTS = 4
MUTATION_RATE_SIZE = 0.3
MUTATION_RATE_SPEED = 0.3
GHOST_LIFETIME = 300

class Monster:

    id = 0

    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = random.choice([1, -1])

    def __repr__(self):
        return f"x:{self.x} y:{self.y} size:{self.size} speed:{self.speed_x}, {self.speed_y}"

    def move(self):
        self.x = (self.x + self.speed_x * self.direction) % SCREEN_WIDTH
        self.y = (self.y + self.speed_y * self.direction) % SCREEN_HEIGHT

    def move_towards(self, other_monster):
        dist = distance(self, other_monster)
        if dist > 0:
            dx = (other_monster.x - self.x) // dist
            dy = (other_monster.y - self.y) // dist
            self.x += dx * self.speed_x
            self.y += dy * self.speed_y

    def move_away(self, other_monster):
        dist = distance(self, other_monster)
        if dist > 0:
            dx = (self.x - other_monster.x) // dist
            dy = (self.y - other_monster.y) // dist
            self.x += dx * self.speed_x
            self.y += dy * self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def find_closest_monster(self, min_dist, monsters):
        closest_monster = None
        for monster in monsters:
            dist = distance(self, monster)
            if min_dist > dist > 0 and self != closest_monster:
                min_dist = dist
                closest_monster = monster
        return closest_monster


class Pacman(Monster):
    def __init__(self, x, y, size, speed_x, speed_y, color=(255, 255, 0), dad=0, mom=0):
        super().__init__(x, y, size, speed_x, speed_y)
        self.dad = dad
        self.mom = mom
        self.color = (255, 255, 0)
        Monster.id += 1
        self.id = Monster.id
        self.age = 0

    def __repr__(self):
        return f"x:{self.x} y:{self.y} size:{self.size} speed:{self.speed_x}," \
               f" {self.speed_y} dad:{self.dad} mom:{self.mom}"

    def reproduce(self, other_pacman):
        size = random.choice([self.size, other_pacman.size, (self.size + other_pacman.size) // 2]) + int(
            random.choice([self.size, other_pacman.size]) * random.uniform(-MUTATION_RATE_SIZE, MUTATION_RATE_SIZE))
        speed_x = random.choice([self.speed_x, other_pacman.speed_x, (self.speed_x + other_pacman.speed_x) // 2]) + int(
            random.choice([self.speed_x, other_pacman.speed_x]) * random.uniform(-MUTATION_RATE_SPEED,
                                                                                 MUTATION_RATE_SPEED))
        speed_y = random.choice([self.speed_y, other_pacman.speed_y, (self.speed_y + other_pacman.speed_y) // 2]) + int(
            random.choice([self.speed_y, other_pacman.speed_y]) * random.uniform(-MUTATION_RATE_SPEED,
                                                                                 MUTATION_RATE_SPEED))
        # print(f"new pacman is born! dad:{self.id} mom:{other_pacman.id}")
        return Pacman(
            self.x + random.randint(-20, 20)
            , self.y + random.randint(-20, 20)
            , size
            , speed_x
            , speed_y
            , self.id
            , other_pacman.id
        )


class Ghost(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, size=10, speed_x=3, speed_y=3)
        self.color = (255, 0, 0)
        self.lifetime = GHOST_LIFETIME

    def __repr__(self):
        return f"size:{self.size} lifetime:{self.lifetime}"


# Define the function to calculate the distance between two objects
def distance(obj1, obj2):
    return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5


# Define the function to check if Pacmans can reproduce
def can_reproduce(pacman1, pacman2):
    if (pacman1.age and pacman2.age) >= 80:
        if (pacman1.dad and pacman1.mom) != pacman2.id \
                and (pacman2.dad and pacman2.mom) != pacman1.id \
                and pacman1.dad != pacman2.dad and pacman1.mom != pacman2.mom:
            return True
        elif (pacman1.dad and pacman1.mom) == 0 \
                and (pacman2.dad and pacman2.mom) == 0:
            return True


# Define the function to check if Pacman is close enough to reproduce
def range_to_reproduce(pacman1, pacman2):
    return distance(pacman1, pacman2) < (pacman1.size + pacman2.size) / 2


# Create initial populations of Pacmans and Ghosts
pacmans = [
    Pacman(
        random.randint(0, SCREEN_WIDTH)
        , random.randint(0, SCREEN_HEIGHT)
        , random.randint(3, 7)
        , random.randint(1, 2)
        , random.randint(1, 2)
    )
    for _ in range(NUM_PACMANS)
]

ghosts = [
    Ghost(
        random.randint(0, SCREEN_WIDTH)
        , random.randint(0, SCREEN_HEIGHT)
    )
    for _ in range(NUM_GHOSTS)
]

# pygame settings
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 14)
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)

    if len(pacmans) == 0:
        print("all pacmans are dead")
        break


    # Draw Pacmans and Ghosts
    for pacman in pacmans:
        if pacman.x > SCREEN_WIDTH: pacman.x -= SCREEN_WIDTH
        if pacman.y > SCREEN_HEIGHT: pacman.y -= SCREEN_HEIGHT
        if pacman.x < 0: pacman.x += SCREEN_WIDTH
        if pacman.y < 0: pacman.y += SCREEN_HEIGHT
        pacman.draw(screen)

    for ghost in ghosts:
        if ghost.x > SCREEN_WIDTH: ghost.x -= SCREEN_WIDTH
        if ghost.y > SCREEN_HEIGHT: ghost.y -= SCREEN_HEIGHT
        if ghost.x < 0: ghost.x += SCREEN_WIDTH
        if ghost.y < 0: ghost.y += SCREEN_HEIGHT
        ghost.draw(screen)

    ghosts_to_remove = []
    # Ghosts lifecycle
    for ghost in ghosts:
        ghosts_to_append = []
        pacmans_to_delete = []

        # ghost eating
        for pacman in pacmans:
            if math.hypot(pacman.x - ghost.x, pacman.y - ghost.y) \
                    <= (pacman.size + ghost.size) // 2:
                try:
                    pacmans.remove(pacman)
                    pacmans_to_delete.append(pacman)
                    ghost.size += pacman.size
                    if ghost.size >= 20:
                        ghosts_to_remove.append(ghost)
                        print("ghost popped")
                        ghosts_to_append.append(Ghost(ghost.x - 10, ghost.y - 10))
                        ghosts_to_append.append(Ghost(ghost.x + 10, ghost.y + 10))
                    print("pacman is eaten")
                    break
                except ValueError:
                    pass

        # ghost movement
        if ghost.find_closest_monster(100, pacmans):
            pacman = ghost.find_closest_monster(100, pacmans)
            ghost.move_towards(pacman)
        else:
            if ghost.x <= 0 + ghost.size:
                ghost.speed_x *= -1
            if ghost.y <= 0 + ghost.size:
                ghost.speed_y *= -1
            ghost.move()

        ghost.lifetime -= 1
        if ghost.lifetime <= 0:
            if len(ghosts) > 1:
                ghosts_to_remove.append(ghost)
            else:
                ghost.lifetime = GHOST_LIFETIME

        for pacman in pacmans_to_delete:
            try:
                pacmans.remove(pacman)
            except ValueError:
                del pacman
                pass

        # add newborn ghosts
        ghosts.extend(ghosts_to_append)

    # clear dead monsters
    for ghost in ghosts_to_remove:
        print(ghost)
        ghosts.remove(ghost)
        del ghost
        print("ghost is dead")

    pacmans_to_delete = []
    # Pacmans lifecycle
    for pacman in pacmans:

        pacman.age += 1

        if pacman.age == 1000:
            pacmans.remove(pacman)
            pacmans_to_delete.append(pacman)
            break

        # Pacman movement
        for other_pacman in pacmans:

            if distance(pacman, other_pacman) <= 100 and can_reproduce(pacman, other_pacman):
                pacman.move_towards(other_pacman)

            if other_pacman != pacman \
                    and can_reproduce(pacman, other_pacman) \
                    and range_to_reproduce(pacman, other_pacman):
                for i in range(random.randint(1, 4)):
                    new_pacman = pacman.reproduce(other_pacman)
                    if new_pacman.size >= (pacman.size and other_pacman.size) \
                            or new_pacman.speed_x >= (pacman.speed_x and other_pacman.speed_x) \
                            or new_pacman.speed_y >= (pacman.speed_y and other_pacman.speed_y):
                        pacmans.append(new_pacman)
                    else:
                        pacmans_to_delete.append(new_pacman)
                pacmans.remove(other_pacman)
                pacmans_to_delete.append(other_pacman)
                try:
                    pacmans.remove(pacman)
                    pacmans_to_delete.append(pacman)
                except ValueError:
                    pass
                break

        # Pacman movement
        if pacman.find_closest_monster(100, ghosts):
            pacman.move_away(pacman.find_closest_monster(100, ghosts))
        elif pacman.find_closest_monster(50, pacmans):
            pacman.move_towards(pacman.find_closest_monster(50, pacmans))
        else:
            if pacman.x <= 0 + pacman.size:
                pacman.speed_x *= -1
            if pacman.y <= 0 + pacman.size:
                pacman.speed_y *= -1
            pacman.move()

    for pacman in pacmans_to_delete:
        del pacman

    text = font.render(
        f"pacmans: {len(pacmans)}"
        f"ghosts:{len(ghosts)}"
        f"max_speed_x_pa: {(max(pacmans, key=lambda y: y.speed_x)).speed_x}"
        f"max_speed_y_pa: {(max(pacmans, key=lambda y: y.speed_y)).speed_y}"
        f"max_size_pa: {(max(pacmans, key=lambda y: y.size)).size}"
        #f"max_speed_x_gh: {(max(ghosts, key=lambda y: y.speed_x)).speed_x}"
        #f"max_speed_y_gh: {(max(ghosts, key=lambda y: y.speed_y)).speed_y}"
        , True
        , (255, 255, 255)
    )
    screen.blit(text, (0, 0))

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
