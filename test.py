#!/usr/bin/env python3

import configparser
import copy
import os
import unittest

import site
_extras_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
site.addsitedir(_extras_dir)  # For collision module
site.addsitedir(os.path.dirname(_extras_dir))  # For configfile module

import configfile

from collision import geometry
import collision


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
        r6 = geometry.Rectangle(8.9, 0, 12, 4)  # Less than 1 padding to r1
        r7 = geometry.Rectangle(0, 5.1, 8, 8)  # More than 1 padding to r1

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

        # Collision with padding
        self.assertFalse(r1.collides_with(r6))
        self.assertTrue(r1.collides_with(r6, 1))
        self.assertTrue(r6.collides_with(r1, 1))
        self.assertFalse(r1.collides_with(r7, 1))


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
        c6 = geometry.Cuboid(24.9, 19.9, 14.9, 40, 35, 30)  # Less than 5 padding to c1
        c7 = geometry.Cuboid(25.1, 0, 0, 40, 15, 10)  # More than 5 padding to c1

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

        # Collision with padding
        self.assertFalse(c1.collides_with(c6))
        self.assertTrue(c1.collides_with(c6, 5))
        self.assertTrue(c6.collides_with(c1, 5))
        self.assertFalse(c1.collides_with(c7, 5))


class CollisionTest(unittest.TestCase):

    def setUp(self):
        fileconfig = configparser.RawConfigParser(strict=False)
        with open(CONFIG_FILE, "r") as fp:
            fileconfig.read_file(fp)
        config = configfile.ConfigWrapper(
            _DummyPrinter(), fileconfig, {}, "collision")
        self.collision = collision.load_config(config)

        # Make another collision object but with an x-oriented gantry
        fc_x = copy.deepcopy(fileconfig)
        fc_x.set("collision", "gantry_orientation", "x")
        config_x = configfile.ConfigWrapper(
            _DummyPrinter(), fc_x, {}, "collision")
        self.collision_x = collision.load_config(config_x)

    def test_attributes(self):
        c = self.collision
        self.assertIsInstance(c.printbed, geometry.Cuboid)
        self.assertIsInstance(c.printhead, geometry.Rectangle)
        self.assertIsInstance(c.gantry, geometry.Rectangle)
        self.assertIsInstance(c.gantry_x_oriented, bool)
        self.assertIsInstance(c.gantry_height, float)
        self.assertGreaterEqual(c.gantry_height, 0)
        self.assertEqual(c.current_objects, [])

        self.assertFalse(c.gantry_x_oriented)
        self.assertTrue(self.collision_x.gantry_x_oriented)

    def test_moving_parts(self):
        cy = self.collision
        cx = self.collision_x
        new_object = geometry.Cuboid(70, 100, 0, 150, 180, 60)
        self.assertEqual(cy.moving_parts(new_object),
                         (geometry.Rectangle(-10, 50.1, 176, 252),
                          geometry.Cuboid(41.5, 0, 84, 182, 1000, float('inf'))))
        self.assertEqual(cx.moving_parts(new_object),
                         (geometry.Rectangle(-10, 50.1, 176, 252),
                          geometry.Cuboid(0, 71.5, 84, 500, 212, float('inf'))))

    def test_collision(self):
        cy = self.collision
        cx = self.collision_x
        # Objects well distributed on X-Axis, only fits with cy
        objects0 = [geometry.Cuboid(10, 10, 0, 150, 100, 120),
                    geometry.Cuboid(250, 10, 0, 400, 200, 150)]
        # Like previous, but first object is small enough to fit under gantry
        objects1 = [geometry.Cuboid(10, 10, 0, 150, 100, 75),
                    geometry.Cuboid(250, 10, 0, 400, 200, 150)]
        # Gantry fits, printhead doesn't
        objects2 = [geometry.Cuboid(50, 50, 0, 150, 150, 75),
                    geometry.Cuboid(170, 50, 0, 300, 150, 75)]
        # Completely colliding objects
        objects3 = [geometry.Cuboid(10, 10, 0, 400, 400, 200),
                    geometry.Cuboid(50, 50, 0, 200, 200, 75)]
        # Diagonal setup: both gantry orientations fit
        objects4 = [geometry.Cuboid(10, 10, 0, 100, 100, 200),
                    geometry.Cuboid(200, 200, 0, 400, 400, 200)]
        # Would fit except the padding is lower than 5
        objects5 = [geometry.Cuboid(10, 10, 0, 100, 100, 80),
                    geometry.Cuboid(184, 10, 0, 300, 100, 80)]

        # Too large for printer
        o_large = geometry.Cuboid(10, 20, 0, 1500, 2000, 899)
        self.assertFalse(cy.printjob_collision(o_large))

        cy.add_printed_object(objects0[0])
        cx.add_printed_object(objects0[0])
        self.assertTrue(cy.printjob_collision(objects0[1]))
        # Gantry collides
        self.assertFalse(cx.printjob_collision(objects0[1]))
        cy.clear_objects()
        cx.clear_objects()

        cy.add_printed_object(objects1[0])
        cx.add_printed_object(objects1[0])
        self.assertTrue(cy.printjob_collision(objects1[1]))
        # Gantry passes over
        self.assertTrue(cx.printjob_collision(objects1[1]))
        cy.clear_objects()
        cx.clear_objects()

        cy.add_printed_object(objects2[0])
        cx.add_printed_object(objects2[0])
        # Printhead collides
        self.assertFalse(cy.printjob_collision(objects2[1]))
        self.assertFalse(cx.printjob_collision(objects2[1]))
        cy.clear_objects()
        cx.clear_objects()

        cy.add_printed_object(objects3[0])
        cx.add_printed_object(objects3[0])
        # Everything collides
        self.assertFalse(cy.printjob_collision(objects3[1]))
        self.assertFalse(cx.printjob_collision(objects3[1]))
        cy.clear_objects()
        cx.clear_objects()

        cy.add_printed_object(objects4[0])
        cx.add_printed_object(objects4[0])
        # Nothing collides
        self.assertTrue(cy.printjob_collision(objects4[1]))
        self.assertTrue(cx.printjob_collision(objects4[1]))
        cy.clear_objects()
        cx.clear_objects()

        cy.add_printed_object(objects5[0])
        cx.add_printed_object(objects5[0])
        # The padding isn't kept
        self.assertFalse(cy.printjob_collision(objects5[1]))
        self.assertFalse(cx.printjob_collision(objects5[1]))
        # Test that it would work with padding set from 5 to 3
        cy_no_pad = copy.copy(cy)
        cx_no_pad = copy.copy(cx)
        cy_no_pad.padding = 3
        cx_no_pad.padding = 3
        self.assertTrue(cy_no_pad.printjob_collision(objects5[1]))
        self.assertTrue(cx_no_pad.printjob_collision(objects5[1]))
        cy.clear_objects()
        cx.clear_objects()


if __name__ == '__main__':
    unittest.main()
