# I acknowledge the use of ChatGPT (GPT-5.1 Thinking, OpenAI, https://chatgpt.com/)
# to create, refine, and assist with the code in this file.

import tkinter as tk
import random

GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 100  # smaller = faster movement
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#000000"


class Snake:
    """Represents the player's snake in the game."""
    def __init__(self, canvas: tk.Canvas):
        self.body_size = BODY_PARTS
        self.coordinates: list[list[int]] = []
        self.squares: list[int] = []
        self.canvas = canvas

        # Start with all body parts at (0, 0)
        for _ in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tag="snake"
            )
            self.squares.append(square)


class Food:
    """Represents a single food item."""
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food"
        )


def next_turn(window: tk.Tk, canvas: tk.Canvas, snake: Snake,
              food: Food, label: tk.Label, state: dict) -> None:

    x, y = snake.coordinates[0]

    if state["direction"] == "up":
        y -= SPACE_SIZE
    elif state["direction"] == "down":
        y += SPACE_SIZE
    elif state["direction"] == "left":
        x -= SPACE_SIZE
    elif state["direction"] == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Check if snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        state["score"] += 1
        label.config(text=f"Score: {state['score']}")
        canvas.delete("food")
        food = Food(canvas)
    else:
        # Remove last body segment
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over(canvas)
    else:
        window.after(SPEED, next_turn, window, canvas, snake, food, label, state)


def change_direction(state: dict, new_direction: str) -> None:
    """Prevent reversing direction immediately."""
    current = state["direction"]

    if new_direction == "left" and current != "right":
        state["direction"] = "left"
    elif new_direction == "right" and current != "left":
        state["direction"] = "right"
    elif new_direction == "up" and current != "down":
        state["direction"] = "up"
    elif new_direction == "down" and current != "up":
        state["direction"] = "down"


def check_collisions(snake: Snake) -> bool:
    """Return True if snake collides with wall or itself."""
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True

    return False


def game_over(canvas: tk.Canvas) -> None:
    """Display Game Over text."""
    canvas.delete("all")
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        text="GAME OVER - Thanks for playing!",
        font=("Arial", 30, "bold"),
        fill="red"
    )


def main() -> None:
    """Run the Snake game GUI."""
    window = tk.Tk()
    window.title("Shivam's Snake Game - CSC-44102 Assessment 2 (v1)")

    window.resizable(False, False)

    state = {
        "score": 0,
        "direction": "down"
    }

    label = tk.Label(window, text=f"Score: {state['score']}", font=("Arial", 16))
    label.pack()

    canvas = tk.Canvas(window, bg=BG_COLOR,
                       width=GAME_WIDTH, height=GAME_HEIGHT)
    canvas.pack()

    window.update()

    snake = Snake(canvas)
    food = Food(canvas)

    window.bind("<Left>", lambda _: change_direction(state, "left"))
    window.bind("<Right>", lambda _: change_direction(state, "right"))
    window.bind("<Up>", lambda _: change_direction(state, "up"))
    window.bind("<Down>", lambda _: change_direction(state, "down"))

    next_turn(window, canvas, snake, food, label, state)
    window.mainloop()


if __name__ == "__main__":
    main()
