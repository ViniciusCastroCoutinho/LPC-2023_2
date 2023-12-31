# Jucimar Jr
# 2022

import pygame
import random

pygame.init()

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

SCORE_MAX = 3

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MyPong - PyGame Edition - 2021.01.30")

# score text
score_font = pygame.font.Font('assets/PressStart2P.ttf', 44)
score_text = score_font.render('00 x 00', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect = score_text.get_rect()
score_text_rect.center = (680, 50)

# victory text
victory_font = pygame.font.Font('assets/PressStart2P.ttf', 100)
victory_text = victory_font .render('VICTORY', True, COLOR_WHITE, COLOR_BLACK)
victory_text_rect = score_text.get_rect()
victory_text_rect.center = (450, 350)

# defeat text
defeat_font = pygame.font.Font('assets/PressStart2P.ttf', 100)
defeat_text = defeat_font .render('DEFEAT', True, COLOR_WHITE, COLOR_BLACK)
defeat_text_rect = score_text.get_rect()
defeat_text_rect.center = (506, 350)

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')

# player 1
player_1 = pygame.image.load("assets/player.png")
player_1_y = 300
player_1_move_up = False
player_1_move_down = False

# paddle height and parts
paddle_height = 150
paddle_part_height = paddle_height / 15

# player 2 - robot
player_2 = pygame.image.load("assets/player.png")
player_2_y = 300
player_2_moving = False
ai_reaction = False

# ball
ball = pygame.image.load("assets/ball.png")
ball_x = 640
ball_y = random.randint(1, 360)
ball_dx = 5
ball_dy = 5
speed_max = 25


def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = 640
    ball_y = random.randint(1, 360)
    ball_dx = random.choice([-1, 1]) * 5
    ball_dy = random.choice([-1, 1]) * 5
    ball_dy *= -1
    ball_dx *= -1
    scoring_sound_effect.play()


def speed_ball(ball_d):
    global speed_max
    if abs(ball_d) < speed_max:
        ball_d *= -1.11
    else:
        if ball_d > 0:
            ball_d = -speed_max
        else:
            ball_d = speed_max
    return ball_d


def ball_collision_x(player_y):
    global paddle_part_height, ball_y, ball_dy, ball_dx
    for i in range(15):
        if player_y + i * paddle_part_height < ball_y + 20 < player_y + (i + 1) * paddle_part_height:
            if i == 7:
                ball_dy = 0
            else:
                ball_dy = i - 7
            ball_dx = speed_ball(ball_dx)
            bounce_sound_effect.play()
            break


# score
score_1 = 0
score_2 = 0

# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        #  keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1_move_up = True
            if event.key == pygame.K_DOWN:
                player_1_move_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_1_move_up = False
            if event.key == pygame.K_DOWN:
                player_1_move_down = False

    # checking the victory condition
    if score_1 < SCORE_MAX and score_2 < SCORE_MAX:

        # clear screen
        screen.fill(COLOR_BLACK)

        # ball collision with the wall
        if ball_y > 700:
            ball_dy *= -1
            bounce_sound_effect.play()
        elif ball_y <= 0:
            ball_dy *= -1
            bounce_sound_effect.play()

        # ball collision with the player 1 's paddle
        # x-axis
        if 80 - abs(speed_ball(ball_dx)) < ball_x < 100:
            ball_collision_x(player_1_y)

        # y-axis
        if 30 < ball_x < 80 - abs(speed_ball(ball_dx)):
            if player_1_move_up and player_1_y < ball_y <= player_1_y + 20 + speed_ball(ball_dy):
                ball_y -= (ball_dy + 15)
                ball_dy = speed_ball(ball_dy)
                bounce_sound_effect.play()
            elif player_1_move_down and player_1_y + 150 >= ball_y + 20 >= player_1_y + 130 - speed_ball(ball_dy):
                ball_y += (ball_dy + 15)
                ball_dy = speed_ball(ball_dy)
                bounce_sound_effect.play()
        elif 20 < ball_x < 100:
            if player_1_y + 30 == ball_y + 25 or player_1_y + 155 == ball_y:
                ball_dy = speed_ball(ball_dy)
                bounce_sound_effect.play()

        # ball collision with the player 2 's paddle
        # y-axis
        if 1180 + speed_ball(ball_dx) < ball_x < 1230:
            if player_2_y < ball_y <= player_2_y + 20 + speed_ball(ball_dy):
                ball_y -= (ball_dy + 15)
                ball_dy = speed_ball(ball_dy)
                bounce_sound_effect.play()
            elif player_2_y + 150 >= ball_y + 20 >= player_2_y + 130 - speed_ball(ball_dy):
                ball_y += (ball_dy + 15)
                ball_dy = speed_ball(ball_dy)
                bounce_sound_effect.play()
        elif 1160 + speed_ball(ball_dx) < ball_x < 1230:
            if player_2_y + 30 == ball_y + 25 or player_2_y + 155 == ball_y:
                ball_dy = speed_ball(ball_dy)
                bounce_sound_effect.play()
        # x-axis
        if 1160 < ball_x < 1190 + abs(speed_ball(ball_dx)):
            ball_collision_x(player_2_y)

        # scoring points
        if ball_x < -50:
            reset_ball()
            score_2 += 1
        elif ball_x > 1320:
            reset_ball()
            score_1 += 1

        # ball movement
        ball_x = ball_x + ball_dx
        ball_y = ball_y + ball_dy

        # player 1 up movement
        if player_1_move_up:
            player_1_y -= 5
        else:
            player_1_y += 0

        # player 1 down movement
        if player_1_move_down:
            player_1_y += 5
        else:
            player_1_y += 0

        # player 1 collides with upper wall
        if player_1_y <= 0:
            player_1_y = 0

        # player 1 collides with lower wall
        elif player_1_y >= 570:
            player_1_y = 570

        # player 2 "Artificial Intelligence"
        if ball_dx < 0:
            ai_reaction = False
            if not player_2_moving:
                if random.randint(0, 99) < 5:
                    player_2_moving = True
            else:
                if player_2_y < 300:
                    player_2_y += 5
                elif player_2_y > 300:
                    player_2_y -= 5
        else:
            if not ai_reaction:
                if random.randint(0, 99) < 5:
                    ai_reaction = True
            else:
                if player_2_y + 80 > ball_y > player_2_y + 70:
                    pass
                elif ball_y > player_2_y + 75:
                    player_2_y += 5
                elif ball_y < player_2_y + 75:
                    player_2_y -= 5
        if player_2_y <= 0:
            player_2_y = 0
        elif player_2_y >= 570:
            player_2_y = 570

        # update score hud
        score_text = score_font.render(str(score_1) + ' x ' + str(score_2), True, COLOR_WHITE, COLOR_BLACK)

        # drawing objects
        screen.blit(ball, (ball_x, ball_y))
        screen.blit(player_1, (50, player_1_y))
        screen.blit(player_2, (1180, player_2_y))
        screen.blit(score_text, score_text_rect)
    elif score_1 == SCORE_MAX:
        # drawing victory
        screen.fill(COLOR_BLACK)
        screen.blit(score_text, score_text_rect)
        screen.blit(victory_text, victory_text_rect)
    elif score_2 == SCORE_MAX:
        # drawing defeat
        screen.fill(COLOR_BLACK)
        screen.blit(score_text, score_text_rect)
        screen.blit(defeat_text, defeat_text_rect)

    # update screen
    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()
