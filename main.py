import pygame
import os
import math
import random

pygame.init()
WIDTH = 1900
HEIGHT = 1000
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FPS = 144
pygame.display.set_caption("Orbital Diagram")
clock = pygame.time.Clock()
G = 6.674 * (10 ** (-11))


class Celestial_Body:
    def __init__(self, name, mass, radius, colour, x, y, v_x, v_y, orbital_lines):
        self.name = name
        self.mass = mass
        self.colour = colour
        self.radius = radius
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.orbital_lines = orbital_lines


class orbital_line:
    def __init__(self, decay, x, y, width, height):
        self.decay = decay
        self.x = x
        self.y = y
        self.width = width
        self.height = height


sun = Celestial_Body("sun", 10 ** 16, 10, WHITE, WIDTH / 2, HEIGHT / 2, 0, 0, [])
sun_2 = Celestial_Body("sun_2", 10 ** 16, 10, WHITE, WIDTH / 3, HEIGHT / 3, 0, 30, [])
Planet_1 = Celestial_Body("planet 1", 10, 2, BLUE, sun.x + 100, HEIGHT / 2, 0, (G * sun.mass / 100) ** (1 / 2), [])
Planet_2 = Celestial_Body("planet 2", 200, 4, RED, sun.x - 200, HEIGHT / 2, 0, -(G * sun.mass / 200) ** (1 / 2), [])
print((G * sun.mass / 100) ** (1 / 2))


# draws out data onto window
def draw(bodies):
    screen.fill(BLACK)
    for body in bodies:
        for line in body.orbital_lines:
            pygame.draw.rect(screen, body.colour, (line.x, line.y, 1, 1))
        pygame.draw.circle(screen, body.colour, (body.x, body.y), body.radius)
    pygame.display.update()


# helper function for removing celestial body from list
def exclude_body(body1, bodies):
    exclude_body1_list = []
    for body2 in bodies:
        if body1.name != body2.name:
            exclude_body1_list.append(body2)
    return exclude_body1_list


# helper function to remove lines after certain period
def remove_line(line1, orbital_lines):
    orbital_lines_without_line = []
    for line2 in orbital_lines:
        if line1.x != line2.x:
            orbital_lines_without_line.append(line2)
    return orbital_lines_without_line


# Updates values
def tick(bodies):
    for body1 in bodies:
        F_x = 0
        F_y = 0
        for body2 in exclude_body(body1, bodies):
            x_dif = body1.x - body2.x
            y_dif = body1.y - body2.y
            F_x += -(G * body1.mass * body2.mass * (x_dif / ((x_dif ** 2 + y_dif ** 2) ** (1 / 2))) / (
                    x_dif ** 2 + y_dif ** 2))
            F_y += -(G * body1.mass * body2.mass * (y_dif / ((x_dif ** 2 + y_dif ** 2) ** (1 / 2))) / (
                    x_dif ** 2 + y_dif ** 2))
        body1.v_x += F_x / (body1.mass * FPS)
        body1.v_y += F_y / (body1.mass * FPS)
        body1.x += body1.v_x / FPS
        body1.y += body1.v_y / FPS
        body1.orbital_lines.append(orbital_line(0, body1.x, body1.y, body1.v_x / FPS, body1.v_y / FPS))
        for line in body1.orbital_lines:
            line.decay += 1 / FPS
            if line.decay >= 1:
                body1.orbital_lines = remove_line(line, body1.orbital_lines)


def shift_lines(shift_x, shift_y, lines):
    for line in lines:
        line.x += shift_x
        line.y += shift_y


def shift_bodies(shift_x, shift_y, bodies):
    for body in bodies:
        shift_lines(shift_x, shift_y, body.orbital_lines)
        body.x += shift_x
        body.y += shift_y


# Initalizes the simulation
def main():
    #bodies = [sun_2, sun]
    bodies = [sun,Planet_1,Planet_2]
    bodies = [sun,sun_2, Planet_1, Planet_2]
    running = True

    while running:
        clock.tick(FPS)
        shift_bodies(CENTER_X - bodies[0].x, CENTER_Y - bodies[0].y, bodies)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bodies.append(
                    Celestial_Body(("Planet" + str(len(bodies))), random.randint(10, 1000), random.randint(1, 5),
                                   ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))), pos[0],
                                   pos[1], random.randint(1, 100), random.randint(1, 100), []))
        tick(bodies)
        draw(bodies)


main()
