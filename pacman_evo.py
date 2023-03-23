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
        
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = 1
         
    def __repr__(self):
        return(f"x:{self.x} y:{self.y} size:{self.size} speed:{self.speed_x}, {self.speed_y}")        
        
    def move(self):
        
        """
        dx = random.randint(-self.speed_x, self.speed_x)
        dy = random.randint(-self.speed_y, self.speed_y)
        self.x = (self.x + dx) % SCREEN_WIDTH
        self.y = (self.y + dy) % SCREEN_HEIGHT
        """
        # Changing the direction and x,y coordinate
        # of the object if the coordinate of left
        # side is less than equal to 20 or right side coordinate
        # is greater than equal to 580
        if self.x <= self.size + 20 or self.x >= self.size + 780:
            self.direction *= -1
            self.speed_x = self.speed_x * self.direction
            self.speed_y = self.speed_y * self.direction
    
        # Changing the direction and x,y coordinate
        # of the object if the coordinate of top
        # side is less than equal to 20 or bottom side coordinate
        # is greater than equal to 580
        if self.y <= self.size + 20 or self.y >= self.size + 580:
            self.direction *= -1
            self.speed_x = self.speed_x * self.direction
            self.speed_y = self.speed_y * self.direction
    
        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y

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


class Pacman(Monster):
    def __init__(self, x, y, size, speed_x, speed_y, color = (255, 255, 0), dad = 0, mom = 0):
        super().__init__(x, y, size, speed_x, speed_y)
        self.dad = dad
        self.mom = mom
        self.color = (255, 255, 0)
        Monster.id += 1
        self.id = Monster.id
        self.age = 0

    def __repr__(self):
        return(f"x:{self.x} y:{self.y} size:{self.size} speed:{self.speed_x}, {self.speed_y} dad:{self.dad} mom:{self.mom}")

    def reproduce(self, other_pacman):
        size = random.choice([self.size, other_pacman.size, (self.size+other_pacman.size)//2]) + int(random.choice([self.size, other_pacman.size]) * random.uniform(-MUTATION_RATE_SIZE, MUTATION_RATE_SIZE))
        speed_x = random.choice([self.speed_x, other_pacman.speed_x, (self.speed_x+other_pacman.speed_x)//2]) + int(random.choice([self.speed_x, other_pacman.speed_x]) * random.uniform(-MUTATION_RATE_SPEED, MUTATION_RATE_SPEED))
        speed_y = random.choice([self.speed_y, other_pacman.speed_y, (self.speed_y+other_pacman.speed_y)//2]) + int(random.choice([self.speed_y, other_pacman.speed_y]) * random.uniform(-MUTATION_RATE_SPEED, MUTATION_RATE_SPEED))
        #print(f"new pacman is born! dad:{self.id} mom:{other_pacman.id}")      
        return Pacman(self.x, self.y, size, speed_x, speed_y, self.id, other_pacman.id)

class Ghost(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, size = 10, speed_x = 6, speed_y = 6)
        self.color = (255, 0, 0)
        self.lifetime = 4000
        
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
pacmans = [Pacman(random.randint(0, SCREEN_WIDTH)
           , random.randint(0, SCREEN_HEIGHT)
           , random.randint(3, 7)
           , random.randint(4, 6)
           , random.randint(4, 6)) for _ in range(NUM_PACMANS)]

ghosts = [Ghost(random.randint(0, SCREEN_WIDTH)
          , random.randint(0, SCREEN_HEIGHT)) for _ in range(NUM_GHOSTS)]
      

#pygame settings
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
    text = font.render(f"pacmans: {len(pacmans)}"
                       f"ghosts:{len(ghosts)}" 
                       f"max_speed: {(max(pacmans, key=lambda y: y.speed_x)).speed_x}"
                       f"max_size: {(max(pacmans, key=lambda y: y.size)).size}",
                        True, (255, 255, 255)
                        )
    screen.blit(text, (0, 0))
    
    if len(pacmans) == 0:
        print("all pacmans are dead")
        break
    elif len(ghosts) == 0:
        ghosts.append(Ghost(random.randint(0, SCREEN_WIDTH)
                      , random.randint(0, SCREEN_HEIGHT))
                      )
    
    # Draw Pacmans and Ghosts
    for pacman in pacmans:
        pacman.draw(screen)

    for ghost in ghosts:
        ghost.draw(screen)
        
    pacmans_to_delete = []    
        
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
                pacman.move()
           
            if math.hypot(pacman.x - ghost.x, pacman.y - ghost.y) \
               <= (pacman.size + ghost.size)//2:
                try:
                    pacmans.remove(pacman)
                    pacmans_to_delete.append(pacman)
                    ghost.size += pacman.size
                    ghost.lifetime = 4000
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
                    if len(ghosts) > 1:
                        ghosts_to_remove.append(ghost)
                    else:
                        ghost.lifetime = 4000
                           
        for ghost in ghosts_to_remove:
            ghosts.remove(ghost)
            del ghost
            print("ghost dead")
            
        #add new ghosts that were born after their ancestor was popped   
        ghosts.extend(ghosts_to_append)
        
        #pacman reproduction cycle            
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
                pacmans_to_delete.append(other_pacman)
                try:
                    pacmans.remove(pacman)
                    pacmans_to_delete.append(pacman)
                except ValueError:
                    pass  
                break
            
    for pacman in pacmans_to_delete:
        del pacman
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

