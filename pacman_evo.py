import math
import pygame
import random


# Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
NUM_PACMANS = 100
NUM_GHOSTS = 2
MUTATION_RATE_SIZE = 0.2
MUTATION_RATE_SPEED = 0.2

class Monster:
    
    id = 0
        
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
         
    def __repr__(self):
        return(f"x:{self.x} y:{self.y} size:{self.size} speed:{self.speed}")        
        
    def move(self):
        dx = random.randint(-self.speed, self.speed)
        dy = random.randint(-self.speed, self.speed)
        self.x = (self.x + dx) % SCREEN_WIDTH
        self.y = (self.y + dy) % SCREEN_HEIGHT
        
    def move_towards(self, other_monster):
        dist = distance(self, other_monster)
        if dist > 0:
            dx = (other_monster.x - self.x) // dist
            dy = (other_monster.y - self.y) // dist
            self.x += dx * self.speed
            self.y += dy * self.speed
    
    def move_away(self, other_monster):
        dist = distance(self, other_monster)
        if dist > 0:
            dx = (self.x - other_monster.x) // dist
            dy = (self.y - other_monster.y) // dist
            self.x += dx * self.speed
            self.y += dy * self.speed
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)


class Pacman(Monster):
    def __init__(self, x, y, size, speed, color = (255, 255, 0), dad = 0, mom = 0):
        super().__init__(x, y, size, speed)
        self.dad = dad
        self.mom = mom
        self.color = (255, 255, 0)
        Monster.id += 1
        self.id = Monster.id
        self.age = 0

    def __repr__(self):
        return(f"x:{self.x} y:{self.y} size:{self.size} speed:{self.speed} dad:{self.dad} mom:{self.mom}")

    def reproduce(self, other_pacman):
        size = random.choice([self.size, other_pacman.size, (self.size+other_pacman.size)//2]) + int(random.choice([self.size, other_pacman.size]) * random.uniform(-MUTATION_RATE_SIZE, MUTATION_RATE_SIZE))
        speed = random.choice([self.speed, other_pacman.speed, (self.speed+other_pacman.speed)//2]) + int(random.choice([self.speed, other_pacman.speed]) * random.uniform(-MUTATION_RATE_SPEED, MUTATION_RATE_SPEED))
        print(f"new pacman is born! dad:{self.id} mom:{other_pacman.id}")      
        return Pacman(self.x, self.y, size, speed, self.id, other_pacman.id)

class Ghost(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, size = 10, speed = 6)
        self.color = (255, 0, 0)
        self.lifetime = 2000
        
    def __repr__(self):
        return(f"size:{self.size} lifetime:{self.lifetime}")



# Define the function to calculate the distance between two objects
def distance(obj1, obj2):
    return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5
 
# Define the function to check if Pacmans can reproduce
def can_reproduce(pacman1, pacman2):
    if pacman1.age >= 100 and pacman2.age >= 100:
        if (pacman1.dad and pacman1.mom) != pacman2.id and (pacman2.dad and pacman2.mom) != pacman1.id \
            and pacman1.dad != pacman2.dad and pacman1.mom != pacman2.mom:
            return True
        elif (pacman1.dad and pacman1.mom) == 0 and (pacman2.dad and pacman2.mom) == 0:
            return True

# Define the function to check if Pacman is close enough to reproduce
def range_to_reproduce(pacman1, pacman2):
    return distance(pacman1, pacman2) < (pacman1.size + pacman2.size) / 2


# Create Pacmans and Ghosts
pacmans = [Pacman(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                  random.randint(3, 7), random.randint(4, 6)) for _ in range(NUM_PACMANS)]
print(pacmans)
ghosts = [Ghost(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(NUM_GHOSTS)]
print(ghosts)        

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")


    if len(pacmans) == 0:
        print("all pacmans are dead")
        break
    elif len(ghosts) == 0:
        ghosts.append(Ghost(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
    
    # Draw Pacmans and Ghosts
    for pacman in pacmans:
        pacman.draw(screen)

    for ghost in ghosts:
        ghost.draw(screen)
        
    # Simulate life of Pacmans and Ghosts
    for pacman in pacmans:
        pacman.age += 1
        ghosts_to_remove = []
        ghosts_to_append = []
        for ghost in ghosts:
            
            if distance(pacman, ghost) <= 30:
                pacman.move_away(ghost)
                ghost.move_towards(pacman)
            else:
                ghost.move()
           
            if math.hypot(pacman.x - ghost.x, pacman.y - ghost.y) <= (pacman.size + ghost.size)//2:
                try:
                    pacmans.remove(pacman)
                    ghost.size += pacman.size
                    if ghost.size >= 20:
                        ghosts_to_remove.append(ghost)
                        print("ghost popped")
                        ghosts_to_append.append(Ghost(ghost.x - 10, ghost.y - 10))
                        ghosts_to_append.append(Ghost(ghost.x + 10, ghost.y + 10))
                    print("pacman is eaten")
                except ValueError:
                    ghost.lifetime -= 1
                    if ghost.lifetime <= 0:
                        ghosts_to_remove.append(ghost)
            else:
                ghost.lifetime -= 1
                if ghost.lifetime <= 0:
                    ghosts_to_remove.append(ghost)
                           
        for ghost in ghosts_to_remove:
            ghosts.remove(ghost)
            del ghost
            print("ghost dead")
            
        
        ghosts.extend(ghosts_to_append)
                    
        for other_pacman in pacmans:
            
            if distance(pacman, other_pacman) <= 40 and can_reproduce(pacman, other_pacman):
                pacman.move_towards(other_pacman)
                other_pacman.move_towards(pacman)
            
            if other_pacman != pacman \
               and can_reproduce(pacman, other_pacman) \
               and range_to_reproduce(pacman, other_pacman):
                for i in range(random.randint(2, 3)):
                    new_pacman = pacman.reproduce(other_pacman)
                    pacmans.append(new_pacman)
                pacmans.remove(other_pacman)
                try:
                    pacmans.remove(pacman)
                except ValueError:
                    pass  
                break
    
    pygame.display.flip()

    clock.tick(25)  # limits FPS to 60

pygame.quit()

