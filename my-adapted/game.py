import tkinter as tk
from typing import Protocol, Optional


class GameObject(Protocol):
    def update(self):
        """Update the game object."""

    def paint(self, canvas: tk.Canvas):
        """Paints the game object."""


class Game():  # the main class that we call "Game"
    # setting up the window for the game here
    def __init__(self, title: str, width: int, height: int, timestep: int = 50):
        self.root = tk.Tk()  # saying this window will use tkinter
        self.root.title(title)
        # self.root.title("Tower Defense Ultra Mode")
        self.running = False  # creating a variable RUN. does nothing yet.hu
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timestep = timestep
        self.timer_id = None

        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)

        # actually creates a window and puts our frame on it
        self.canvas = tk.Canvas(master=self.frame, width=width,
                                height=height, bg="white", highlightthickness=0)
        # makes the window called "canvas" complete
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

        self.objects: list[GameObject] = []

    def add_object(self, object: GameObject):
        self.objects.append(object)

    def remove_object(self, object: GameObject):
        self.objects.remove(object)

    def run(self):
        self.running = True
        self._run()
        self.root.mainloop()

    def _run(self):
        self.update()
        self.paint()

        if not self.running:
            return

        # does a run of the function every 50/1000 = 1/20 of a second
        self.timer_id = self.root.after(self.timestep, self._run)

    def end(self):
        self.running = False
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()  # closes the game window and ends the program

    def update(self):
        """Updates the game."""
        for obj in self.objects:
            obj.update()

    def paint(self):
        """Paints the game."""
        self.canvas.delete(tk.ALL)  # clear the screen
        for obj in self.objects:
            obj.paint()
