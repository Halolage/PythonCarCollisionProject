class Car:
    DIRECTIONS = [
        "N",
        "E",
        "S",
        "W",
    ]  # Clockwise so that turn_left turn_right functions can move via index direction to get new direction

    def __init__(self, name, x, y, direction, commands) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = commands
        self.active = True  # Car will be active till it collides
        self.collision_info = None  # Stores collision details and info

    def turn_left(self):
        idx = (Car.DIRECTIONS.index(self.direction) - 1) % 4 # turn_anticlockwise
        self.direction = Car.DIRECTIONS[idx]

    def turn_right(self):
        idx = (Car.DIRECTIONS.index(self.direction) + 1) % 4 # turn_clockwise
        self.direction = Car.DIRECTIONS[idx]

    def move_forward(self, bounding_width, bounding_height):
        new_x, new_y = self.x, self.y
        if self.direction == 'N':
            new_y += 1
        elif self.direction == 'S':
            new_y -= 1
        elif self.direction == 'E':
            new_x += 1
        elif self.direction == 'W':
            new_x -= 1
        
        if 0 <= new_x < bounding_width and 0 <= new_y < bounding_height: # validate if after movement still within boundaries
            return new_x, new_y
        else:
            return self.x, self.y # movement ignored with beyond boundaries
        
    def execute_command(self, command, bounding_width, bounding_height):
        if command == 'L':
            self.turn_left()
        elif command == 'R':
            self.turn_right()
        elif command == 'F':
            self.x, self.y = self.move_forward(bounding_width, bounding_height)


class Simulation:
    def __init__(self) -> None:
        self.bounding_width = 0
        self.bounding_height = 0
        self.cars = []

    def boundary_field(self):
        """Sets up the boundary field"""
        while True:
            try:
                width_str, height_str = map(
                    int,
                    input(
                        "Please enter the width and height of the simulation field in x y format: "
                    ).split(),
                )
                self.bounding_width = int(width_str)
                self.bounding_height = int(height_str)
                if self.bounding_width < 0 or self.bounding_height < 0:
                    print("Width and height must be positive integers.")
                    continue
                print(f"You have created a field of {self.bounding_width} x {self.bounding_height}.\n")
                break

            except ValueError as e:
                print(f"Invalid input. Please enter two integers separated by a space.")

    def add_car(self):
        """Adds a car"""
        name = input("Please enter the name of the car: \n").strip()
        while any(car.name==name for car in self.cars):     # Rejects duplicate car names
            print(f"Car named {name} already exists. Please choose a different name.")

        while True:
            try:
                pos_input = input(
                    f"Please enter initial position of car {name} in x y Direction format:\n"
                ).strip()

                x_str, y_str, direction = pos_input.split()
                x, y = int(x_str), int(y_str)
                if not 0 <= x < self.bounding_width and 0 <= y < self.bounding_height:
                    print(f"Position out of bounds, x should be between 0 and {self.bounding_width-1} and y should be between 0 and {self.bounding_height-1}")
                    continue
                if direction not in Car.DIRECTIONS:
                    print("Invalid direction. Only N,S,E,W values are allowed.")
                    continue

                break
            except ValueError:
                print(
                    "Invalid input. Make sure to enter two numbers with a space between (x y) followed by a direction (e.g., '10 5 N')."
                )
        
        while True:
            commands = input(f"Please enter the commands for the car {name}:\n").strip().upper()
            if not commands or not all(c in 'LRF' for c in commands):
                print("Invalid commands, only L, R, F allowed.")
            else:   
                break
        
        new_car = Car(name, int(x), int(y), direction, commands)
        self.cars.append(new_car)
        self.display_cars()

    def display_cars(self):
        print("\nYour current list of cars are:")
        for car in self.cars:
            print(f"- {car.name}, ({car.x, car.y}) {car.direction}, {car.commands}")

    def run(self):
        """Start simulation"""
        print("Welcome to Auto Driving Car Simulation!\n")
        self.boundary_field()

        while True:
            print("\nPlease choose from the following options:")
            print("[1] Add a car to field")
            print("[2] Run simulation")
            choice = input().strip()

            if choice == "1":
                self.add_car()

            elif choice == "2":
                if not self.cars:
                    print("No cars to simulate. Please add at least one car.")
                else:
                    self.display_cars()
                    self.run_simulation()
                    self.post_simulation_options()
                    break
            
            else: 
                print("Invalid option. Please choose 1 or 2.")
    
    def run_simulation(self):
        """Run the simulation"""
        max_steps = max(len(car.commands) for car in self.cars)
        positions = {(car.x, car.y): car.name for car in self.cars}

        for step in range(max_steps):
            intended_moves = {}
            for car in self.cars:
                if not car.active or step >= len(car.commands):
                    continue

                command = car.commands[step]
                prev_x, prev_y = car.x, car.y
                prev_direction = car.direction

                car.execute_command(command, self.bounding_width, self.bounding_height)
                intended_position = (car.x, car.y)

                # dict to pre-store intended moves
                intended_moves[car.name] = {
                    'car': car,
                    'from': (prev_x, prev_y),
                    'to': intended_position,
                    'direction': car.direction,
                    'command': command
                }

                # Example structure of intended_moves:
                # [
                #     {'car': <Car object at 0x7f9f>, 'from': (10, 5), 'to': (10, 6), 'direction': 'N', 'command': 'F'},
                #     {'car': <Car object at 0x7fa0>, 'from': (0, 0), 'to': (1, 0), 'direction': 'E', 'command': 'R'}
                # ]

        
            # Collision Detection
            move_conflicts = {}
            for move in intended_moves.values():
                pos = move['to']
                move_conflicts.setdefault(pos, []).append(move['car']) # groups all cars that intend to move to same position
            
            # Example structure of move_conflicts:
            # move_conflicts = {
            #     (10, 6): [<Car object 1>, <Car object 2>],
            #     (1, 0): [<Car object 3>]
            # }

            for pos, cars_at_pos in move_conflicts.items():
                if len(cars_at_pos) > 1:
                    for car in cars_at_pos:
                        if not car.collision_info: # stores the car collision info if present in dict
                            car.collision_info = {
                                'position' : pos,
                                'step' : step + 1,
                                'with' : [c.name for c in cars_at_pos if c!= car]   # stores the car it had collision at this position with
                            }
                            car.active = False
                            car.x, car.y = pos # update the collided cars to latest collision positon
                        
                else: 
                    car = cars_at_pos[0] # update the non-collided cars to latest collition position
                    positions[(car.x, car.y)] = car.name

        print("\nAfter simulation, the result is: ")
        for car in self.cars:
            if car.collision_info:
                collision_with = ' and '.join(car.collision_info['with'])
                x, y = car.collision_info['position']
                step = car.collision_info['step']
                print(f"- {car.name}, collides with {collision_with} at ({x}, {y}) at step {step}")
            else:
                print(f"- {car.name}, ({car.x}, {car.y}) {car.direction}")

    def post_simulation_options(self):
        while True:
            print("\nPlease choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")
            choice = input().strip()
            if choice == '1':
                self.__init__() # reset simulation
                self.run()
                break
            elif choice == '2':
                print("Thank you for running the simulation. Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
