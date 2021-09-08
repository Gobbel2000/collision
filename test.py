#!/usr/bin/env python3

import configparser
import unittest

import site
site.addsitedir("/home/gabriel/3dp/klipperui/klippy/")  #TODO: correct relative path

import configfile

import geometry
import collision_check


# Needed to create ConfigWrapper
class _DummyPrinter:
    reactor = None

CONFIG_FILE = "test_config.cfg"




class GeometryTest(unittest.TestCase):

    def test_rectangle(self):
        rectangle = geometry.Rectangle(10, 15, 14, 20)
        self.assertEqual(rectangle.x, 10)
        self.assertEqual(rectangle.y, 15)
        self.assertEqual(rectangle.width, 4)
        self.assertEqual(rectangle.height, 5)
        self.assertEqual(rectangle.max_x, 14)
        self.assertEqual(rectangle.max_y, 20)
        self.assertEqual(rectangle.area, 20)

    def test_rectangle_negative(self):
        rectangle = geometry.Rectangle(5, 10, -15, -20)
        self.assertEqual(rectangle.x, -15)
        self.assertEqual(rectangle.y, -20)
        self.assertEqual(rectangle.width, 20)
        self.assertEqual(rectangle.height, 30)
        self.assertEqual(rectangle.max_x, 5)
        self.assertEqual(rectangle.max_y, 10)
        self.assertEqual(rectangle.area, 600)
    
    def test_rectangle_bool(self):
        # Rectangle with positive area
        r1 = geometry.Rectangle(2, 3, 3, 4)
        # Rectangle with area 0
        r2 = geometry.Rectangle(2, 3, 2, 3)
        self.assertTrue(r1)
        self.assertFalse(r2)

    def test_rectangle_eq(self):
        r1 = geometry.Rectangle(4, 6, 8, 8)
        r2 = geometry.Rectangle(8, 8, 4, 6)
        self.assertEqual(r1, r2)

        r3 = geometry.Rectangle(4, 6, 8, 7)
        self.assertNotEqual(r1, r3)

    def test_rectangle_intersection(self):
        r1 = geometry.Rectangle(0, 0, 8, 4)
        r2 = geometry.Rectangle(2, 2, 6, 10)
        r3 = geometry.Rectangle(0, 8, 5, 10)  # bordering, but disjoint to r1
        r4 = geometry.Rectangle(50, 50, 60, 60)  # fully disjoint to r1
        r5 = geometry.Rectangle(1, 1, 7, 3)  # fully surrounded by r1

        # Intersection
        expected = geometry.Rectangle(2, 2, 6, 4)
        self.assertEqual(r1.intersection(r2), expected)
        self.assertEqual(r2.intersection(r1), expected)
        self.assertEqual(r1.intersection(r3).area, 0)
        self.assertEqual(r1.intersection(r4).area, 0)
        self.assertEqual(r1.intersection(r5), r5)
        self.assertEqual(r5.intersection(r1), r5)
        self.assertEqual(r1.intersection(r1), r1)

        # Collision
        self.assertTrue(r1.collides_with(r2))
        self.assertTrue(r2.collides_with(r1))
        self.assertFalse(r1.collides_with(r3))
        self.assertFalse(r1.collides_with(r4))
        self.assertTrue(r1.collides_with(r5))
        self.assertTrue(r5.collides_with(r1))
        self.assertTrue(r1.collides_with(r1))


    def test_cuboid(self):
        cuboid = geometry.Cuboid(10, 15, 20, 30, 40, 30)
        self.assertEqual(cuboid.x, 10)
        self.assertEqual(cuboid.y, 15)
        self.assertEqual(cuboid.z, 20)
        self.assertEqual(cuboid.width, 20)
        self.assertEqual(cuboid.depth, 25)
        self.assertEqual(cuboid.height, 10)

        self.assertEqual(cuboid.max_x, 30)
        self.assertEqual(cuboid.max_y, 40)
        self.assertEqual(cuboid.max_z, 30)
        self.assertEqual(cuboid.volume, 5000)

    def test_cuboid_negative(self):
        cuboid = geometry.Cuboid(5, 20, 5, -5, 15, -15)
        self.assertEqual(cuboid.x, -5)
        self.assertEqual(cuboid.y, 15)
        self.assertEqual(cuboid.z, -15)
        self.assertEqual(cuboid.width, 10)
        self.assertEqual(cuboid.depth, 5)
        self.assertEqual(cuboid.height, 20)

        self.assertEqual(cuboid.max_x, 5)
        self.assertEqual(cuboid.max_y, 20)
        self.assertEqual(cuboid.max_z, 5)
        self.assertEqual(cuboid.volume, 1000)

    def test_cuboid_bool(self):
        c1 = geometry.Cuboid(2, 2, 2, 7, 5, 3)
        self.assertTrue(c1)
        c2 = geometry.Cuboid(2, 2, 2, 7, 2, 3)
        self.assertFalse(c2)

    def test_cuboid_eq(self):
        c1 = geometry.Cuboid(1, 2, 3, 4, 5, 6)
        c2 = geometry.Cuboid(1, 5, 3, 4, 2, 6)
        c3 = geometry.Cuboid(1, 1, 3, 4, 5, 6)
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

    def test_cuboid_intersection(self):
        c1 = geometry.Cuboid(0, 0, 0, 20, 15, 10)
        c2 = geometry.Cuboid(5, 5, 5, 15, 25, 35)  # Intersecting c1
        c3 = geometry.Cuboid(0, 15, 5, 20, 45, 45)  # bordering, but disjoint to c1
        c4 = geometry.Cuboid(50, 50, 50, 60, 60, 60)  # fully disjoint to c1
        c5 = geometry.Cuboid(2, 2, 2, 14, 10, 8)  # fully surrounded by c1

        # Intersection
        expected = geometry.Cuboid(5, 5, 5, 15, 15, 10)
        self.assertEqual(c1.intersection(c2), expected)
        self.assertEqual(c2.intersection(c1), expected)
        self.assertEqual(c1.intersection(c3).volume, 0)
        self.assertEqual(c1.intersection(c4).volume, 0)
        self.assertEqual(c1.intersection(c5), c5)
        self.assertEqual(c5.intersection(c1), c5)
        self.assertEqual(c1.intersection(c1), c1)

        # Collision
        self.assertTrue(c1.collides_with(c2))
        self.assertTrue(c2.collides_with(c1))
        self.assertFalse(c1.collides_with(c3))
        self.assertFalse(c1.collides_with(c4))
        self.assertTrue(c1.collides_with(c5))
        self.assertTrue(c5.collides_with(c1))
        self.assertTrue(c1.collides_with(c1))


class CollisionTest(unittest.TestCase):

    def setUp(self):
        fileconfig = configparser.RawConfigParser(strict=False)
        with open(CONFIG_FILE, "r") as fp:
            fileconfig.read_file(fp)
        config = configfile.ConfigWrapper(
            _DummyPrinter(), fileconfig, {}, "collision")
        self.collision = collision_check.load_config(config)

    def test_attributes(self):
        c = self.collision
        self.assertIsInstance(c.printbed, geometry.Cuboid)
        self.assertIsInstance(c.printhead, geometry.Rectangle)
        self.assertIsInstance(c.gantry, geometry.Rectangle)
        self.assertIsInstance(c.gantry_x_oriented, bool)
        self.assertIsInstance(c.gantry_height, float)
        self.assertGreater(c.gantry_height, 0)
        self.assertEqual(c.current_objects, [])

    def test_(self):
        print("2nd test")


if __name__ == '__main__':
    unittest.main()
