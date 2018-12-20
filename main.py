import pymunk
import pygame
from settings import *
from objects import *
from copy import deepcopy


# Initializes the pygame game loop and sets up the pymunk physics space.
def evaluate(car, gen, it):
    # Initialize blank pygame window.
    pygame.init()
    pygame.display.set_caption("{}: iteration={}, generation={}".format(WINDOW_NAME, it, gen))
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Initialize pymunk physics engine.
    space = pymunk.Space()
    space.gravity = (0, -GRAVITY)

    # Add ground and car objects to the space.
    ground = Ground()
    ground.add_to_space(space)
    car.add_to_space(space)
    
    # Start game loop.
    for step in range(TIMESTEPS):
        # Draw objects on screen.
        window.fill(BLACK)
        car.blit(window)
        ground.blit(window)

        car.wheel_friction()

        # Update game state.
        space.step(0.02)
        pygame.display.flip()
        clock.tick(FPS)

    # Exit game.
    pygame.display.quit()
    pygame.quit()

    return car.score()

    

# Performs the evolutionary cycle
def main():
    population = [[Car(), 0, 0] for _ in range(POPULATION_SIZE)]
    
    for gen in range(NUM_GENERATIONS):
        
        # evaluate each car in the population
        for j, ind in enumerate(population):
            car, score, gen = ind
            if not score:
                score = evaluate(car, gen, j)
                population[j][1] = score

        # Perform selection
        cars = sorted(population, key=lambda x: -x[1])[:NUM_SURVIVORS]
        print("Best car = {}".format(cars[0]))

        # let cars have kids.
        population = []
        for car, score, gen in cars:
            car2 = car.offspring()
            population += [[car, score, gen], [car2, 0, gen+1]]
    

if __name__ == "__main__":
    main()
