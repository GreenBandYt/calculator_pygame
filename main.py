import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 480, 660
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (173, 216, 230)
BUTTON_COLOR = (100, 100, 100)
SHADOW_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (150, 150, 150)
FONT = pygame.font.Font(None, 60)
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 80
EQUALS_BUTTON_WIDTH = 380
ENTRY_FIELD_HEIGHT = 80
ENTRY_FIELD_Y = 50

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")


class Button:
    def __init__(self, label, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BUTTON_COLOR
        self.shadow_offset = 5  # Смещение тени

    def draw(self, screen, font):
        # Рисуем тень
        pygame.draw.rect(screen, SHADOW_COLOR,
                         (self.x + self.shadow_offset, self.y + self.shadow_offset, self.width, self.height))

        # Рисуем кнопку
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Определяем цвет текста
        text_color = RED if self.label == 'C' else WHITE

        # Рисуем текст
        text = font.render(self.label, True, text_color)
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def set_hover(self, is_hovered):
        self.color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR


class Calculator:
    def __init__(self):
        self.entry_text = ''
        self.buttons = [
            Button('7', 50, 150), Button('8', 150, 150), Button('9', 250, 150), Button('/', 350, 150),
            Button('4', 50, 250), Button('5', 150, 250), Button('6', 250, 250), Button('*', 350, 250),
            Button('1', 50, 350), Button('2', 150, 350), Button('3', 250, 350), Button('-', 350, 350),
            Button('0', 50, 450), Button('.', 150, 450), Button('C', 250, 450), Button('+', 350, 450),
            Button('=', 50, 550, EQUALS_BUTTON_WIDTH)
        ]

    def draw_entry(self):
        pygame.draw.rect(screen, BLACK, (50, ENTRY_FIELD_Y, EQUALS_BUTTON_WIDTH, ENTRY_FIELD_HEIGHT))
        text = FONT.render(self.entry_text, True, WHITE)
        screen.blit(text, (60, 60))

    def calculate_expression(self, expression):
        try:
            result = eval(expression)
            return str(result)
        except Exception:
            return "Error"

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_clicked(pos):
                if button.label == '=':
                    self.entry_text = self.calculate_expression(self.entry_text)
                elif button.label == 'C':
                    self.entry_text = ''
                else:
                    self.entry_text += button.label

    def update_button_states(self, mouse_pos):
        for button in self.buttons:
            button.set_hover(button.is_clicked(mouse_pos))

    def draw(self):
        self.draw_entry()
        for button in self.buttons:
            button.draw(screen, FONT)


def main():
    calculator = Calculator()
    running = True

    while running:
        screen.fill(GRAY)
        mouse_pos = pygame.mouse.get_pos()
        calculator.update_button_states(mouse_pos)
        calculator.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                calculator.handle_click(event.pos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()