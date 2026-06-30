# HCI Assignment 2 Beta Prototype
# API used: OpenGL with Pygame

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH, HEIGHT = 900, 600

current_screen = "home"


def draw_text(text, x, y, size=28):
    font = pygame.font.SysFont("Arial", size, True)
    text_surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    glWindowPos2d(x, y)
    glDrawPixels(
        text_surface.get_width(),
        text_surface.get_height(),
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        text_data
    )


def draw_rect(x, y, w, h, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


def is_hover(mx, my, x, y, w, h):
    my = HEIGHT - my
    return x <= mx <= x + w and y <= my <= y + h


def button(label, x, y, w, h, mx, my):
    hover = is_hover(mx, my, x, y, w, h)

    if hover:
        draw_rect(x, y, w, h, (0.2, 0.6, 1.0))
    else:
        draw_rect(x, y, w, h, (0.1, 0.35, 0.7))

    draw_text(label, x + 25, y + 25, 24)
    return hover


def setup_opengl():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_home(mx, my):
    draw_rect(0, 0, WIDTH, HEIGHT, (0.05, 0.08, 0.15))

    draw_text("Local Organisation Service Kiosk", 210, 520, 34)
    draw_text("Beta Version Prototype using OpenGL", 250, 480, 24)

    about_hover = button("About Us", 330, 350, 240, 70, mx, my)
    services_hover = button("Services", 330, 250, 240, 70, mx, my)
    contact_hover = button("Contact", 330, 150, 240, 70, mx, my)

    return about_hover, services_hover, contact_hover


def draw_about():
    draw_rect(0, 0, WIDTH, HEIGHT, (0.08, 0.12, 0.2))
    draw_text("About Us", 380, 510, 36)
    draw_text("This prototype is designed for a local organisation.", 160, 410, 26)
    draw_text("It helps users access information easily through", 160, 370, 26)
    draw_text("a simple visual and audio-based interface.", 160, 330, 26)
    draw_text("Press BACKSPACE to return.", 280, 160, 24)


def draw_services():
    draw_rect(0, 0, WIDTH, HEIGHT, (0.08, 0.16, 0.12))
    draw_text("Services", 390, 510, 36)
    draw_text("1. Community Support", 250, 410, 26)
    draw_text("2. Event Registration", 250, 360, 26)
    draw_text("3. Public Information", 250, 310, 26)
    draw_text("4. Feedback Collection", 250, 260, 26)
    draw_text("Press BACKSPACE to return.", 280, 160, 24)


def draw_contact():
    draw_rect(0, 0, WIDTH, HEIGHT, (0.16, 0.10, 0.12))
    draw_text("Contact", 400, 510, 36)
    draw_text("Email: info@localorganisation.com", 230, 400, 26)
    draw_text("Phone: +60 12-345 6789", 280, 350, 26)
    draw_text("Location: Subang Jaya, Malaysia", 240, 300, 26)
    draw_text("Press BACKSPACE to return.", 280, 160, 24)


def main():
    global current_screen

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("HCI Beta Prototype - OpenGL UI")

    setup_opengl()

    try:
        click_sound = pygame.mixer.Sound("click.wav")
    except:
        click_sound = None

    running = True

    while running:
        mx, my = pygame.mouse.get_pos()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if current_screen == "home":
            about_hover, services_hover, contact_hover = draw_home(mx, my)
        elif current_screen == "about":
            draw_about()
        elif current_screen == "services":
            draw_services()
        elif current_screen == "contact":
            draw_contact()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    current_screen = "home"

            if event.type == MOUSEBUTTONDOWN and current_screen == "home":
                if about_hover:
                    current_screen = "about"
                    if click_sound:
                        click_sound.play()

                elif services_hover:
                    current_screen = "services"
                    if click_sound:
                        click_sound.play()

                elif contact_hover:
                    current_screen = "contact"
                    if click_sound:
                        click_sound.play()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()