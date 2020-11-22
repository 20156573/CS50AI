import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    # Tạo một frontier rỗng
    def __init__(self):
        self.frontier = []

    # Thêm một node vào frontier
    def add(self, node):
        self.frontier.append(node)

    # Kiểm tra xem biên giới có chứa một trạng thái cụ thể nào không
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    # Kiểm tra xem biên giới có rỗng không
    def empty(self):
        return len(self.frontier) == 0

    # Xóa một nốt khỏi biên giớ
    def remove(self):
        if self.empty():
            raise Exception('Empty frontier')
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception('Empty frontier')
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    
    def __init__(self, filename):

        # Doc file va cai chieu cao va chieu dai cua me cung
        with open(filename) as f:
            contents = f.read()
        
        # Xac thuc diem khoi dau va diem dich cua me cung
        if contents.count("A") != 1:
            raise Exception('Maze must have exactly one start point')
        if contents.count("B") != 1:
            raise Exception('Maze must have exactly one goal')

        # Xac dinh chieu cao va chieu rong cua me cung
        contents = contents.splitlines()
        print('Day la contents', contents)
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Tao ra mo hinh me cung
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
    
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state): 
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):

        # Theo doi so luong state da duoc kham pha
        self.num_explored = 0

        # Khoi tao frontier den vi tri bat dau
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Khoi tao mot set explored trong
        self.explored = set()

        # Lap lai cho den khi tim ra giai phap
        while True:

            # Neu khong con gi trong frontier, thi khong co con duong nào
            if frontier.empty():
                raise Exception('No solution')
            
            # Chon mot node tu frontier
            node = frontier.remove()
            self.num_explored += 1

            # Neu node la muc tieu, sau do chung ta co giai phap
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # danh dau node la da duoc kham pha
            self.explored.add(node.state)

            # them neighbors vao frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Tao mot canvas trong
        img = Image.new(
            'RGBA',
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
            
                # walls
                if col:
                    fill = (40, 40, 40)
                
                # start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)
                
                # Da duoc kham pha
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                
                # empty cell
                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
        img.save(filename)

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print
("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)