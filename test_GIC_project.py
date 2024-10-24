import unittest
from GIC_project import Car, Simulation

# Unit test on 7 functionalities:
# 1. car initialization and attributes
# 2. Turning left and right
# 3. Moving forward with boundary constraints
# 4. Moviing forward without boundary contraints
# 5. Collision detection
# 6. No Collision 
# 7. Multiple collision

class TestProject(unittest.TestCase):
    def setUp(self):
        # Initialize simulation env for each individual test
        self.simulation = Simulation()
        self.simulation.bounding_width = 10
        self.simulation.bounding_height = 10

    def test_car_initialization(self):
        # Test for car attributes
        car = Car('A', 1, 2, 'N', 'FFRFFFFRRL')
        self.assertEqual(car.name, 'A')
        self.assertEqual(car.x, 1)
        self.assertEqual(car.y, 2)
        self.assertEqual(car.direction, 'N')
        self.assertEqual(car.commands, 'FFRFFFFRRL')
        self.assertTrue(car.active, True)
        self.assertIsNone(car.collision_info)

    def test_car_turning(self):
        # Test for car turn
        car = Car('B', 0, 0, 'N', '')
        car.turn_left()
        self.assertEqual(car.direction, 'W')
        car.turn_right()
        self.assertEqual(car.direction, 'N')
        car.turn_right()
        car.turn_right()
        self.assertEqual(car.direction, 'S')
        car.turn_left()
        self.assertEqual(car.direction, 'E')

    def test_car_movement_within_boundary(self):
        # Test for car within boundary
        car = Car('C', 5, 5, 'N', '')
        new_x, new_y = car.move_forward(self.simulation.bounding_width, self.simulation.bounding_height)
        car.x, car.y = new_x, new_y 
        self.assertEqual((new_x, new_y), (5, 6))
        car.direction = 'E'
        new_x, new_y = car.move_forward(self.simulation.bounding_width, self.simulation.bounding_height)
        car.x, car.y = new_x, new_y 
        self.assertEqual((new_x, new_y), (6, 6))
        car.direction = 'S'
        new_x, new_y = car.move_forward(self.simulation.bounding_width, self.simulation.bounding_height)
        car.x, car.y = new_x, new_y 
        self.assertEqual((new_x, new_y), (6, 5))
        car.direction = 'W'
        new_x, new_y  = car.move_forward(self.simulation.bounding_width, self.simulation.bounding_height)
        car.x, car.y = new_x, new_y 
        self.assertEqual((new_x, new_y), (5, 5))

    def test_car_movement_beyond_boundary(self):
        car = Car('D', 0, 0, 'S', '')
        new_x, new_y = car.move_forward(self.simulation.bounding_width, self.simulation.bounding_height)
        car.x, car.y = new_x, new_y 
        self.assertEqual((car.x, car.y), (0, 0))  # Should not move
        car.direction = 'W'
        new_x, new_y = car.move_forward(self.simulation.bounding_width, self.simulation.bounding_height)
        car.x, car.y = new_x, new_y 
        self.assertEqual((car.x, car.y), (0, 0))  # Should not move

    def test_collision(self):
        car_e = Car('E', 1, 1, 'N', 'F')
        car_f = Car('F', 1, 3, 'S', 'F')
        self.simulation.cars = [car_e, car_f]
        self.simulation.run_simulation()
        self.assertFalse(car_e.active)
        self.assertFalse(car_f.active)
        self.assertIsNotNone(car_e.collision_info)
        self.assertIsNotNone(car_f.collision_info)
        self.assertEqual(car_e.collision_info['position'], (1, 2))
        self.assertEqual(car_f.collision_info['position'], (1, 2))

    def test_no_collision(self):
        car_g = Car('G', 0, 0, 'N', 'FF')
        car_h = Car('H', 5, 5, 'E', 'FF')
        self.simulation.cars = [car_g, car_h]
        self.simulation.run_simulation()
        self.assertTrue(car_g.active)
        self.assertTrue(car_h.active)
        self.assertIsNone(car_g.collision_info)
        self.assertIsNone(car_h.collision_info)
        self.assertEqual((car_g.x, car_g.y), (0, 2))
        self.assertEqual((car_h.x, car_h.y), (7, 5))

    def test_simulation_with_commands(self):
        car_i = Car('I', 1, 2, 'N', 'FFRFFFFRRL')
        self.simulation.cars = [car_i]
        self.simulation.run_simulation()
        self.assertTrue(car_i.active)
        self.assertIsNone(car_i.collision_info)
        self.assertEqual((car_i.x, car_i.y), (5, 4))
        self.assertEqual(car_i.direction, 'S')

    def test_multiple_collisions(self):
        car_j = Car('J', 2, 1, 'N', 'F')
        car_k = Car('K', 2, 3, 'S', 'F')
        car_l = Car('L', 1, 2, 'E', 'F')
        car_m = Car('M', 3, 2, 'W', 'F')
        self.simulation.cars = [car_j, car_k, car_l, car_m]
        self.simulation.run_simulation()
        # All cars should collide at (1,1)
        for car in self.simulation.cars:
            self.assertFalse(car.active)
            self.assertIsNotNone(car.collision_info)
            self.assertEqual(car.collision_info['position'], (2, 2))

if __name__ == '__main__':
    unittest.main()