"""
This file contains the initial and end \
screen and the logic to conect with the game.
"""


import sys
import pygame
from game import game


def draw_text(text, font, color, surface, x, y):
    """
    This function is incharge of draw text in a surface.
    """
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def welcomeScreen():
    """
    It prints in screen the welcome page
    """
    window = pygame.display.set_mode((width, height))
    window_rect = window.get_rect()

    title_size = 50
    font_size = 18

    title_font = pygame.font.Font('freesansbold.ttf', title_size)
    font = pygame.font.Font('freesansbold.ttf', font_size)

    while True:
        window.fill(black)

        x = window_rect.top + width * 0.05
        y = window_rect.left + height * 0.05

        draw_text("Missionaries and Cannibals", title_font,
                  (255, 255, 255), window, x, y)

        y = y + title_size
        instructions = [
            "",
            "Rules:",
            "1.Move the cannibals and the missionaries to the"
            "other side of the river.",
            "2.To move the boat it needs at least one character.",
            "3.If there is on one side 2 or more cannibals and "
            "only one missionary you will lose.",
            "4.Click on the characters or the boat to play.",
            "",
            "¡¡Click to start!!",
            "",
            "",
            "By Victor Herguedas"
        ]

        for text in instructions:
            draw_text(text, font, white, window, x, y)
            y = y + font_size

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                godbyeScreen(game())


def godbyeScreen(status):
    """
    It prints in screen the welcome page
    """
    window = pygame.display.set_mode((width, height))
    window_rect = window.get_rect()

    title_size = 50
    font_size = 30

    title_font = pygame.font.Font('freesansbold.ttf', title_size)
    font = pygame.font.Font('freesansbold.ttf', font_size)

    while True:
        window.fill(black)

        x = window_rect.top + width * 0.05
        y = window_rect.left + height * 0.05

        draw_text("Missionaries and Cannibals", title_font,
                  (255, 255, 255), window, x, y)

        y = y + title_size
        instructions = [
            "",
            status,
            "",
            "",
            "Click to play again.",
            "",
            "",
            "By Victor Herguedas"
        ]

        for text in instructions:
            draw_text(text, font, white, window, x, y)
            y = y + font_size

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                godbyeScreen(game())


if __name__ == "__main__":
    pygame.init()

    width = 800
    height = 480
    white = (255, 255, 255)
    black = (0, 0, 0)

    welcomeScreen()
