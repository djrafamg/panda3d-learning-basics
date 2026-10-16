from panda3d.core import loadPrcFileData, TransparencyAttrib
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec2, ClockObject
import random, math

configs = """
win-size 1280 720
window-title Game Panda3D
show-frame-rate-meter true
"""

loadPrcFileData("", configs)

global_clock = ClockObject.getGlobalClock()

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.setBackgroundColor(0.2, 0.4, 0.8)

        #Camera
        self.disableMouse()
        self.camera.setPos(0, 0, 0)
        self.camera.setHpr(0, 0, 0)

        #Some cam data to learn and understand
        print(self.camera.getPos())
        print(self.camera.getHpr())
        print(self.cam.getTransform())
        print(self.camLens.getFilmSize())
        print(self.camLens.getFov())

        #Dictionary for keys
        self.keys = {"up": False, "down": False, "left": False, "right": False}

        #Key events
        self.accept("arrow_up", self.set_key, ["up", True])
        self.accept("arrow_up-up", self.set_key, ["up", False])
        self.accept("arrow_down", self.set_key, ["down", True])
        self.accept("arrow_down-up", self.set_key, ["down", False])
        self.accept("arrow_left", self.set_key, ["left", True])
        self.accept("arrow_left-up", self.set_key, ["left", False])
        self.accept("arrow_right", self.set_key, ["right", True])
        self.accept("arrow_right-up", self.set_key, ["right", False])

        #Player speed
        self.player_speed = 4

        #Player
        self.player = self.loader.load_model('models/box')
        self.player.setPos(-0.5, 10, -0.5)
        self.player.setColor(1, 0.3, 1, 1)
        self.player.reparentTo(self.render)

        #Target
        self.target = self.loader.load_model('models/box')
        self.target.setScale(0.5)
        self.set_random_target_pos(2)
        self.target.setColor(1, 1, 0, 1)
        self.target.setTransparency(TransparencyAttrib.MAlpha)
        self.target.reparentTo(self.render)
        #Pulse alpha target task
        self.taskMgr.add(self.pulse_alpha_target_task, "PulseAlphaTargetTask")

        #Update task
        self.taskMgr.add(self.update, "UpdateTask")

    def set_key(self, key, value):
        self.keys[key] = value

    def update(self, task):
        dt = global_clock.getDt()

        x, z = 0, 0
        if self.keys["up"]:
            z += 1
        if self.keys["down"]:
            z -= 1
        if self.keys["left"]:
            x -= 1
        if self.keys["right"]:
            x += 1

        direction = Vec2(x, z)

        if direction.length() > 0:
            direction.normalize()
            dx = direction.x * self.player_speed * dt
            dz = direction.y * self.player_speed * dt
        else:
            dx = dz = 0

        pos = self.player.getPos()

        new_x = pos.x + dx
        new_z = pos.z + dz

        new_x = max(-5, min(4, new_x))
        new_z = max(-3, min(2, new_z))

        self.player.setPos(new_x, pos.y, new_z)

        distance = self.get_distance_to_target()

        if distance < 0.8:
            self.set_random_target_pos(2)

        return Task.cont

    def get_distance_to_target(self):
        center_player_x = self.player.getX() + 0.5
        center_player_z = self.player.getZ() + 0.5

        center_target_x = self.target.getX() + 0.25
        center_target_z = self.target.getZ() + 0.25

        distance = ((center_player_x - center_target_x) ** 2 + (center_player_z - center_target_z) ** 2) ** 0.5
        return distance

    def set_random_target_pos(self, min_distance_from_player):
        while True:
            pos_x = random.uniform(-4.5, 4)
            pos_z = random.uniform(-2.5, 2)
            self.target.setPos(pos_x, 10.25, pos_z)

            distance = self.get_distance_to_target()
            if distance >= min_distance_from_player:
                break

    def pulse_alpha_target_task(self, task):
        #Alpha: [0.4, 1]
        alpha = 0.7 + 0.3 * math.sin(task.time * 3)
        print(alpha)
        self.target.setColor(1, 1, 0, alpha)
        return task.cont

game = MyGame()
game.run()

