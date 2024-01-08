import pygame
import time

class Point:
    def __init__(self, x: int, y: int, name: str, font: pygame.font.Font):
        self.x = x
        self.y = y
        self.name = name
        self.nameText = font.render(name, True, 'blue') 
        self.radius = 10
        self.checked = False

    def getNeighbor(self, links) -> list:
        neighbor = []
        for link in links:
            point1, point2, weight = link.get()
            if self == point1: 
                neighbor.append((point2, weight))
            if self == point2:
                neighbor.append((point1, weight))

        return neighbor

    def setChecked(self, value: bool):
        self.checked = value

    def display(self, screen):
        pygame.draw.circle(screen, 'blue', (self.x, self.y), self.radius)
        screen.blit(self.nameText, (self.x - 1.5 * self.radius, self.y + 1.5 * self.radius)) 



class Link:
    def __init__(self, point1: Point, point2: Point, weight: int, font: pygame.font.Font):
        self.point1 = point1
        self.point2 = point2
        self.weight = weight
        self.weightText = font.render(str(weight), True, 'green') 

    def get(self) -> (Point, Point, int):
        return self.point1, self.point2, self.weight

    def display(self, screen):
        pygame.draw.line(screen, 'green', (self.point1.x, self.point1.y), (self.point2.x, self.point2.y), 2)
        screen.blit(self.weightText, ((self.point1.x + self.point2.x) / 2 - 40, (self.point1.y + self.point2.y) / 2 - 40))


class Salersman:
    def __init__(self, startPoint: Point):
        self.startPoint = startPoint
        self.onPoint = startPoint
        self.radius = 5
        self.nbPointChecked = 0
        self.oldPoint = None
        self.nextPoint = None

    def getMinWeight(self, points: list) -> Point:
        minWeight = 999
        minPoint = None

        for point in points:
            if point[1] < minWeight:
                minWeight = point[1]
                minPoint = point

        return minPoint


    def choseNextPoint(self, links: list):
        neighbor = self.onPoint.getNeighbor(links)
        noneCheckedPoint = []
        # point[0]: Point, point[1]: weight
        for point in neighbor:

            if point[0].checked == False:
                noneCheckedPoint.append(point)

        if len(noneCheckedPoint) == 0:
            self.nextPoint = self.getMinWeight(neighbor)
        else:
            self.nextPoint = self.getMinWeight(noneCheckedPoint)
      
        # Handle the End
        for i in neighbor:
            if self.nbPointChecked > nbPoint and i[0].name == 'A':
                self.nextPoint = i
        
        self.onPoint.setChecked(True)
        self.nbPointChecked += 1
        self.oldPoint = self.onPoint
        self.onPoint = self.nextPoint[0]

    def display(self, screen: pygame.display.set_mode):
        pygame.draw.circle(screen, 'red', (self.onPoint.x, self.onPoint.y), self.radius)

        if self.oldPoint != None and self.nextPoint != None:
            pygame.draw.line(screen, 'red', (self.oldPoint.x, self.oldPoint.y), (self.onPoint.x, self.onPoint.y), 2)


# Initialize pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
font = pygame.font.Font(size=32)

# Initialize points
nbPoint = 5
pointA = Point(100, 300, 'A', font)
pointB = Point(300, 200, 'B', font)
pointC = Point(300, 400, 'C', font)
pointD = Point(500, 100, 'D', font)
pointE = Point(700, 500, 'E', font)
points = [pointA, pointB, pointC, pointD, pointE]

# Initialize links
linkAB = Link(pointA, pointB, 3, font)
linkAC = Link(pointA, pointC, 2, font)
linkBC = Link(pointB, pointC, 1, font)
linkBD = Link(pointB, pointD, 5, font)
linkBE = Link(pointB, pointE, 4, font)
linkCE = Link(pointC, pointE, 3, font)
links = [linkAB, linkAC, linkBC, linkBD, linkBE, linkCE]

# Initialize Salersman
s = Salersman(pointA)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill('white')

    # Display linnks
    for link in links:
        link.display(screen)

    # Display points
    for point in points:
        point.display(screen)

    s.display(screen)
    
    pygame.display.flip()


    time.sleep(1)
    s.choseNextPoint(links)

    clock.tick(60)

pygame.quit()














