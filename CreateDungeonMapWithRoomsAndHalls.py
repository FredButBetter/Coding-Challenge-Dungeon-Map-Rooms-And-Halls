import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

MAP_WIDTH = 60
MAP_HEIGHT = 60
MAX_LEAF_SIZE = 20
MIN_LEAF_SIZE = 6

def main():
    rootLeaf = leaf(0, 0, MAP_WIDTH, MAP_HEIGHT)    # Initialize the root leaf, which in the end will be the full map
    leafList = [rootLeaf]

    didSplit = True

    # create the room boundaries
    while didSplit:
        didSplit = False
        for loopleaf in leafList:
            if (loopleaf.leftChild is None) and (loopleaf.rightChild is None):
                if loopleaf.width > MAX_LEAF_SIZE or loopleaf.height > MAX_LEAF_SIZE:
                    loopleaf.split()
                    leafList.append(loopleaf.leftChild)
                    leafList.append(loopleaf.rightChild)
                    didSplit = True

    halls = []
    # create the rooms within those boundaries
    rootLeaf.createRooms()

    # plot to show final result
    fig, ax = plt.subplots()
    for loopleaf in leafList:
        if (loopleaf.leftChild is None) and (loopleaf.rightChild is None):
            room = loopleaf.room
            rect = patches.Rectangle((room.x, room.y), room.width, room.height, linewidth=1, edgecolor='none', facecolor='blue')
            ax.add_patch(rect)

        if len(loopleaf.halls) != 0:
            for hall in loopleaf.halls:
                rect = patches.Rectangle((hall.x, hall.y), hall.width, hall.height, linewidth=1, edgecolor='none', facecolor='red')
                ax.add_patch(rect)

    plt.xlim([-1, MAP_WIDTH+1])
    plt.ylim([-1, MAP_HEIGHT+1])
    plt.show()


class leaf:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.leftChild = None
        self.rightChild = None

        self.room = None
        self.halls = []

    # cut the leaf in half vertically or horizontally to make 2 new leaves
    def split(self):
        if self.width > self.height:  # if current leaf is wider than it is high, then split side-by-side
            splitMax = max(self.width - MIN_LEAF_SIZE, MIN_LEAF_SIZE)   #ensure that the maximum size doesn't go negative
            splitInt = random.randint(MIN_LEAF_SIZE, splitMax)
            self.leftChild = leaf(self.x, self.y, splitInt, self.height)
            self.rightChild = leaf(self.x + splitInt, self.y, self.width - splitInt, self.height);
        else:   # otherwise split top-to-bottom
            splitMax = max(self.height - MIN_LEAF_SIZE, MIN_LEAF_SIZE)  # ensure that the maximum size doesn't go negative
            splitInt = random.randint(MIN_LEAF_SIZE, splitMax)
            self.leftChild = leaf(self.x, self.y, self.width, splitInt)
            self.rightChild = leaf(self.x, self.y + splitInt, self.width, self.height - splitInt);


    # generate all rooms and hallways for this leaf and all children
    def createRooms(self):
        if self.leftChild is not None or self.rightChild is not None:   # this is a branch, go to children
            if self.leftChild is not None:
                self.leftChild.createRooms()
            if self.rightChild is not None:
                self.rightChild.createRooms()

            if self.leftChild is not None and self.rightChild is not None:
                self.createHall(self.leftChild.getRoom(), self.rightChild.getRoom())

        else:   # else make rooms in this leaf
            roomWidth = random.randint(3, self.width - 2)   # room size is at least 3 by 3, but leaves some room for hallways
            roomHeight = random.randint(3, self.height - 2)

            roomX = self.x + random.randint(1, self.width - roomWidth)
            roomY = self.y + random.randint(1, self.height - roomHeight)

            self.room = room(roomX, roomY, roomWidth, roomHeight)

    # get a room from within the leaf
    def getRoom(self):
        if self.room is not None:
            return self.room
        else:
            leftRoom, rightRoom = None, None
            if self.leftChild is not None:
                leftRoom = self.leftChild.getRoom()
            if self.rightChild is not None:
                rightRoom = self.rightChild.getRoom()

            if leftRoom is None and rightRoom is None:
                return None
            elif rightRoom is None:
                return leftRoom
            elif leftRoom is None:
                return rightRoom
            elif random.random() > .5:
                return leftRoom
            else:
                return rightRoom

    # create a hallway between two rooms
    def createHall(self, leftRoom, rightRoom):
        point1X = random.randint(leftRoom.x + 1, leftRoom.x + leftRoom.width - 1)
        point1Y = random.randint(leftRoom.y + 1, leftRoom.y + leftRoom.height - 1)
        point2X = random.randint(rightRoom.x + 1, rightRoom.x + rightRoom.width - 1)
        point2Y = random.randint(rightRoom.y + 1, rightRoom.y + rightRoom.height - 1)

        hallWidth = point2X - point1X
        hallHeight = point2Y - point1Y

        if hallWidth < 0:
            if hallHeight < 0:
                if random.random() > .5:
                    self.halls.append(room(point2X, point1Y, abs(hallWidth), 1))
                    self.halls.append(room(point2X, point2Y, 1, abs(hallHeight)))
                else:
                    self.halls.append(room(point2X, point2Y, abs(hallWidth), 1))
                    self.halls.append(room(point1X, point2Y, 1, abs(hallHeight)))
            elif hallHeight > 0:
                if random.random() > .5:
                    self.halls.append(room(point2X, point1Y, abs(hallWidth), 1))
                    self.halls.append(room(point2X, point1Y, 1, abs(hallHeight)))
                else:
                    self.halls.append(room(point2X, point2Y, abs(hallWidth), 1))
                    self.halls.append(room(point1X, point1Y, 1, abs(hallHeight)))
            else: # hallHeight is 0
                self.halls.append(room(point2X, point2Y, abs(hallWidth), 1))
        elif hallWidth > 0:
            if hallHeight < 0:
                if random.random() > .5:
                    self.halls.append(room(point1X, point2Y, abs(hallWidth), 1))
                    self.halls.append(room(point1X, point2Y, 1, abs(hallHeight)))
                else:
                    self.halls.append(room(point1X, point1Y, abs(hallWidth), 1))
                    self.halls.append(room(point2X, point2Y, 1, abs(hallHeight)))
            elif hallHeight > 0:
                if random.random() > .5:
                    self.halls.append(room(point1X, point1Y, abs(hallWidth), 1))
                    self.halls.append(room(point2X, point1Y, 1, abs(hallHeight)))
                else:
                    self.halls.append(room(point1X, point2Y, abs(hallWidth), 1))
                    self.halls.append(room(point1X, point1Y, 1, abs(hallHeight)))
            else: # hallHeight is 0
                self.halls.append(room(point1X, point1Y, abs(hallWidth), 1))
        else: # hallWidth is 0
            if hallHeight < 0:
                self.halls.append(room(point2X, point2Y, 1, abs(hallHeight)))
            elif hallHeight > 0:
                self.halls.append(room(point1X, point1Y, 1, abs(hallHeight)))


class room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


if __name__ == '__main__': main()