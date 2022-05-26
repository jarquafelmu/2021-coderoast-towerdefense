import tkinter as tk


class Game():  # the main class that we call "Game"
    # setting up the window for the game here
    def __init__(self, title: str, width: int, height: int, timestep: int = 50):
        self.root = tk.Tk()  # saying this window will use tkinter
        self.root.title(title)
        # self.root.title("Tower Defense Ultra Mode")
        self.running = False  # creating a variable RUN. does nothing yet.hu
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timestep = timestep

        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)

        # actually creates a window and puts our frame on it
        self.canvas = tk.Canvas(master=self.frame, width=width,
                                height=height, bg="white", highlightthickness=0)
        # makes the window called "canvas" complete
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

    def run(self):
        # handle special cases first
        if not self.running:
            return

        self.update()  # calls the function 'def update(self):'
        self.paint()  # calls the function 'def paint(self):'

        # does a run of the function every 50/1000 = 1/20 of a second
        self.root.after(self.timestep, self.run)

    def end(self):
        self.root.destroy()  # closes the game window and ends the program

    def update(self):
        self.mouse.update()
        self.wavegenerator.update()
        self.displayboard.update()
        # done so that a projectile removing itself wont break this loop
        for projectile in projectiles:
            projectile.update()
        for y in range(gridSize):
            for x in range(gridSize):
                # updates each block one by one by going to its 'def update():' command
                blockGrid[x][y].update()
        for monster in monsters:
            monster.update()
        global monstersByHealth
        global monstersByHealthReversed
        global monstersByDistance
        global monstersByDistanceReversed
        global monstersListList
        monstersByHealth = sorted(
            monsters, key=lambda x: x.health, reverse=True)
        monstersByDistance = sorted(
            monsters, key=lambda x: x.distanceTravelled, reverse=True)
        monstersByHealthReversed = sorted(
            monsters, key=lambda x: x.health, reverse=False)
        monstersByDistanceReversed = sorted(
            monsters, key=lambda x: x.distanceTravelled, reverse=False)
        monstersListList = [monstersByHealth, monstersByHealthReversed,
                            monstersByDistance, monstersByDistanceReversed]

        for y in range(gridSize):
            for x in range(gridSize):
                if towerGrid[x][y]:
                    # updates each tower one by one by going to its 'def update():' command
                    towerGrid[x][y].update()

    def paint(self):
        self.canvas.delete(ALL)  # clear the screen
        self.gameMap.paint(self.canvas)
        # draw the mouse dot by going to its 'def paint(canvas):' command
        self.mouse.paint(self.canvas)
        for y in range(gridSize):
            for x in range(gridSize):
                if towerGrid[x][y]:
                    towerGrid[x][y].paint(self.canvas)
        for i in range(len(monstersByDistanceReversed)):
            monstersByDistanceReversed[i].paint(self.canvas)
        for i in range(len(projectiles)):
            projectiles[i].paint(self.canvas)
        if displayTower:
            displayTower.paintSelect(self.canvas)
        self.displayboard.paint()
