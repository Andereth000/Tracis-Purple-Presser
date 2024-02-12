import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

pygame.mixer.init()
pop_sound = pygame.mixer.Sound("Audio/Pop sound effect.mp3")  # Replace with the actual path to your sound file

# Set up display
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
width, height = infoObject.current_w, infoObject.current_h
pygame.display.set_caption("Traci's Purple Presser")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
purple = (128, 0, 128)

# Game variables
title = "Traci's Purple Presser"
score = 0
clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)
mouse_pressed = False

buttons = []  # List to store information about each button


def display_title(title):
    title_text = font.render(title, True, purple)
    screen.blit(title_text, (175, 10))


def display_score(score):
    score_text = font.render(f"{score}", True, black)
    screen.blit(score_text, (500, 100))


def create_button():
    button_size = random.randint(300, 500)
    margin = 120
    button_x = random.randint(margin, width - button_size - margin)
    button_y = random.randint(margin, height - button_size - margin)

    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
    buttons.append(button_rect)


confetti = []  # List to store information about each confetti


def create_confetti(x, y):
    num_confetti = random.randint(10, 20)  # Adjust the range for the number of confetti pieces

    for _ in range(num_confetti):
        confetti_size = 20
        confetti_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        angle = math.radians(random.uniform(0, 360))  # Random angle in radians
        speed = random.uniform(2, 5)  # Adjust the speed range

        confetti_rect = pygame.Rect(x, y, confetti_size, confetti_size)
        confetti.append((confetti_rect, confetti_color, angle, speed))


def main():
    global score
    global confetti
    global mouse_pressed

    while True:
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                for button in buttons:
                    if button.collidepoint(event.pos):
                        buttons.remove(button)
                        score += 1

                        pop_sound.play()

                        create_confetti(button.x + button.width // 2, button.y + button.height // 2)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False

            if event.type == pygame.MOUSEMOTION and mouse_pressed:
                for button in buttons:
                    if button.collidepoint(event.pos):
                        buttons.remove(button)
                        score += 1

                        pop_sound.play()

                        create_confetti(button.x + button.width // 2, button.y + button.height // 2)

        display_score(score)
        display_title(title)

        if not buttons:  # If no button on the screen, create one
            create_button()

        new_confetti = []

        for confetti_piece in confetti:
            confetti_rect, confetti_color, angle, speed = confetti_piece
            pygame.draw.rect(screen, confetti_color, confetti_rect)
            confetti_rect.x += speed * math.cos(angle)
            confetti_rect.y += speed * math.sin(angle)

            new_confetti.append((confetti_rect, confetti_color, angle, speed))

        confetti = new_confetti

        # Remove confetti that is out of the screen
        confetti = [(rect, color, angle, speed) for rect, color, angle, speed in confetti if rect.y < height]

        # Draw all existing buttons
        for button in buttons:
            pygame.draw.ellipse(screen, purple, button)

        pygame.display.flip()
        clock.tick(30)  # Adjust frame rate as needed


if __name__ == "__main__":
    main()

