from CommonFuncs import *
from Map import Map
from Scripts.Entity.Entity import Entity
import random


class Ghost(Entity):
    def __init__(self, name: str, file: str, spriteGroup: pygame.sprite.Group, startPosition: Tuple[int, int], map: Map, pathColor):
        Entity.__init__(self, spriteGroup, startPosition, file)
        self.name = name
        self.speed = 1
        self.map = map
        self.startDirection = UP
        self.currentDirection = self.startDirection
        self.pathColor = pathColor

    def move(self):
        cell = worldToGridT(self.rect.center)
        if self.map.colorMap[cell[0]][cell[1]] == MAP_CROSSROAD:
            directions = raycast(self.rect.center, self.map)
            if len(directions) > 0:
                self.currentDirection = random.choice(directions)
        self.moveByDirection(self.currentDirection)


    def moveByDirection(self, direction: int):
        if direction == UP:
            self.rect.y -= self.speed
        elif direction == DOWN:
            self.rect.y += self.speed
        elif direction == RIGHT:
            self.rect.x += self.speed
        elif direction == LEFT:
            self.rect.x -= self.speed

    def collidePlayer(self):
        print(self.name)

    # def bfs(self, startNode: Node, targetNode: Node, color, screen, map):
    #     queue = [(startNode, [startNode])]
    #
    #     timer = Timer()
    #     timer.start()
    #     while queue:
    #         (node, path) = queue.pop(0)
    #         # print(path)
    #         # print("finish")
    #         node.isVisited = True
    #         if node == targetNode:
    #             DrawPath(path, color, screen)
    #             # pygame.draw.circle(pygame.display.get_surface(), MAP_PACMAN_START_POSITION, gridToWorldT(node.gridPosition), 5)
    #             # print(node.gridPosition)
    #             # print(len(path))
    #             # print("bfs")
    #             # print(timer.stop())
    #             return path
    #
    #         if node.topN != None and node.topN.isVisited == False:
    #             newPath = path.copy()
    #             newPath.append(node.topN)
    #             queue.append((node.topN, newPath))
    #         if node.rightN != None and node.rightN.isVisited == False:
    #             newPath = path.copy()
    #             newPath.append(node.rightN)
    #             queue.append((node.rightN, newPath))
    #         if node.bottomN != None and node.bottomN.isVisited == False:
    #             newPath = path.copy()
    #             newPath.append(node.bottomN)
    #             queue.append((node.bottomN, newPath))
    #         if node.leftN != None and node.leftN.isVisited == False:
    #             newPath = path.copy()
    #             newPath.append(node.leftN)
    #             queue.append((node.leftN, newPath))
    #
    #     self.map.resetVisited()