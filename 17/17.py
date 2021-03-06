import sys
import re
import math

FILE = 'input17.txt'


def factor(n):
    for d in range(2, int(math.sqrt(n))+1):
        if d * (d + 1) == n:
            return d

class Probe:

    def __init__(self):
        self.x, self.y = 0, 0       # position
        self.dx, self.dy = 0, 0     # vitesse
        self.trajectoire = [(0, 0)]

    def initialise(self, dx, dy):
        self.x, self.y = 0, 0
        self.trajectoire = [(0, 0)]
        self.dx, self.dy = dx, dy

    # Règles de déplacement du probe

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def drag(self):
        self.dx = max(self.dx - 1, 0)
    
    def gravity(self):
        self.dy -= 1

    def step(self):
        self.move()
        self.drag()
        self.gravity()
        self.trajectoire.append((self.x, self.y))


    def steps(self, n):
        for _ in range(n):
            self.step()


class Mission:


    def __init__(self, filename):
        self.filename = filename
        self.area = (0, 0), (0, 0) # x intervalle, y intervalle
        self.probe = Probe()
        self.nb_steps = -1
        self.alt_max = 0     # pour la partie 1
        self.velocities = [] # pour la partie 2


    def load(self):
        regex = r"target area: x=(?P<x0>(-)?\d+)\.\.(?P<x1>(-)?\d+), y=(?P<y0>-?\d+)\.\.(?P<y1>-?\d+)\n"
        with open(self.filename, 'r') as datas:
            search = re.search(regex, datas.readline())
            self.area = (int(search.group('x0')), int(search.group('x1'))), (int(search.group('y0')), int(search.group('y1')))

    # -- Modélisation

    def __str__(self):
        s = ''
        debut_y = max(self.max_y(), *tuple(y for _, y in self.probe.trajectoire)) + 2
        fin_y = min(self.min_y(), *tuple(y for _, y in self.probe.trajectoire)) - 3
        fin_x = max(self.max_x(), *tuple(x for x, _ in self.probe.trajectoire)) + 3
        for y in range(debut_y, fin_y, -1):
            s += f'{y:3} '
            for x in range(fin_x):
                if (x, y) == (0, 0):
                    s += 'S'
                elif (x, y) in self.probe.trajectoire:
                    s += '#'
                elif self.inside(x, y):
                    s += 'T'
                else:
                    s += '.'
            s += '\n'
        return s


    def inside(self, x, y):
        return self.min_x() <= x <=self.max_x() and self.min_y() <= y <=self.max_y()

    def too_far(self, x, y):
        return x > self.max_x() or y < self.min_y()

    def min_x(self):
        return self.area[0][0]

    def max_x(self):
        return self.area[0][1]

    def min_y(self):
        return self.area[1][0]

    def max_y(self):
        return self.area[1][1]

    def end(self):
        x, y = self.probe.x, self.probe.y
        return self.inside(x, y) or self.too_far(x, y)

    def simulate(self, dx, dy):
        """Simule le mouvement du projectile jusqu'à ce qu'il entre dans la zone
        (return True) où qu'il la dépasse (return False)"""
        self.probe.initialise(dx, dy)
        while not self.end():
            self.probe.step()
            self.nb_steps += 1
        return self.inside(self.probe.x, self.probe.y)


    # -- Résolution

    def set_intervals_velocity(self):
        dx_min = int((1 + 3 * math.sqrt(self.min_x())) / 2) - 1
        dx_max = self.max_x()
        y_min = self.min_y()
        y_max = self.max_y()

        if y_min > 0:
            dy_min = int((1 + 3 * math.sqrt(y_min)) / 2) - 1
            dy_max = y_max
        else:
            dy_min = y_min
            dy_max = abs(y_min) - 1

        return dx_min, dx_max, dy_min, dy_max

    def solve(self):
        _, _, _, dy_max = self.set_intervals_velocity()
        self.alt_max = dy_max * (dy_max + 1) // 2

    def solve_two(self):
        dx_min, dx_max, dy_min, dy_max = self.set_intervals_velocity()
        self.velocities = [(dx, dy) for dx in range(dx_min, dx_max+1)
                                        for dy in range(dy_min, dy_max+1)
                                            if self.simulate(dx, dy)]


def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    mission = Mission(fichier)
    mission.load()
    if version == '1':
        mission.solve()
        print(mission.alt_max)
    else:
        mission.solve_two()
        print(len(mission.velocities))

if __name__ == '__main__':
    main() 


