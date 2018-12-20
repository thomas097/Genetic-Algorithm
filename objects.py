import pymunk
import pygame
from settings import *
import numpy as np
from copy import deepcopy


class Ground():
    def __init__(self, height=80):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Poly(self.body, [(0, GROUND_HEIGHT), (0, 0),
                                             (WINDOW_WIDTH, 0), (WINDOW_WIDTH, GROUND_HEIGHT)])
        self.shape.friction = GROUND_FRICTION

    def add_to_space(self, space):
        space.add(self.shape)

    def blit(self, window):
        pygame.draw.line(window, GREY, (0, WINDOW_HEIGHT - GROUND_HEIGHT),
                         (WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_HEIGHT), LINE_WIDTH)
    

class Car():
    def __init__(self):
        self.bodies = []
        self.shapes = []
        self.constraints = []
        self.spds = [0, 0]

        # Create body of the car.
        self.num_body_parts = np.random.randint(MIN_BODY_PARTS, MAX_BODY_PARTS)
        for i in range(self.num_body_parts):
            # Create body part.
            body = pymunk.Body(CAR_MASS, CAR_MOMENTUM)

            # Position body part.
            dx, dy = np.random.randint(-CAR_INIT_D, CAR_INIT_D, 2)
            body.position = (CAR_INIT_X + dx, CAR_INIT_Y + dy) 

            # Assign box to body part
            radius = np.random.randint(MIN_BODY_RADIUS, MAX_BODY_RADIUS)
            shape = pymunk.Circle(body, radius)

            # Store part for reference.
            self.bodies.append(body)
            self.shapes.append(shape)

        # Make first (and optionally the last) part(s) wheels.
        if len(self.bodies) > 1:
            self.spds[0] = np.random.randint(MIN_WHEEL_ANGULAR_VELOCITY, MAX_WHEEL_ANGULAR_VELOCITY)
            self.bodies[-1].angular_velocity = self.spds[0]
            self.bodies[-1].friction = WHEEL_FRICTION
        self.spds[1] = np.random.randint(MIN_WHEEL_ANGULAR_VELOCITY, MAX_WHEEL_ANGULAR_VELOCITY)
        self.bodies[0].angular_velocity = self.spds[1]
        self.bodies[0].friction = WHEEL_FRICTION
        

        # Link pairs of bodies together using joints (if more than one joint).
        if len(self.bodies) > 1:
            for i, body1 in enumerate(self.bodies[:-1]):
                body2 = self.bodies[i+1]
                constr = pymunk.constraint.PinJoint(body1, body2)
                constr.distance = self.shapes[i].radius + self.shapes[i+1].radius + 1
                self.constraints.append(constr)


    def add_to_space(self, space):
        # Add bodies to space.
        for body, shape in zip(self.bodies, self.shapes):
            space.add(body, shape)
        # Add body constrains.
        for constr in self.constraints:
            space.add(constr)


    def wheel_friction(self):
        # Determine distance from wheel(s) to ground.
        dy1 = abs(self.bodies[-1].position[1] - self.shapes[-1].radius- GROUND_HEIGHT)
        dy2 = abs(self.bodies[0].position[1] - self.shapes[0].radius- GROUND_HEIGHT)
        
        if len(self.bodies) > 1 and dy1 < WHEEL_COLLISION_THRES:
            self.bodies[-1].force = self.spds[0] * self.shapes[-1].radius, 0
            
        if dy2 < WHEEL_COLLISION_THRES:
            self.bodies[0].force = self.spds[1] * self.shapes[0].radius, 0


    def score(self):
        return min([b.position[0] for b in self.bodies])


    def offspring(self):
        self2 = deepcopy(self)
        self2.spds[0] += np.clip(np.random.randint(-3, 3), MIN_WHEEL_ANGULAR_VELOCITY,
                                MAX_WHEEL_ANGULAR_VELOCITY)
        self2.spds[1] += np.clip(np.random.randint(-3, 3), MIN_WHEEL_ANGULAR_VELOCITY,
                                MAX_WHEEL_ANGULAR_VELOCITY)
        return self2
            

    def blit(self, window):       
        # Draw bodiesone by one.
        for body, shape in zip(self.bodies, self.shapes):
            radius, angle = shape.radius, body.angle
            
            x = body.position[0]
            y = WINDOW_HEIGHT - body.position[1]
            dx = radius * np.cos(angle)
            dy = radius * np.sin(angle)
            
            pygame.draw.circle(window, BLUE, (int(x), int(y)), int(radius))
            pygame.draw.line(window, GREY, (int(x), int(y)), (int(x + dx), int(dy + y)), LINE_WIDTH)

            
