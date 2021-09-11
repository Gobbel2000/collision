from geometry import Rectangle, Cuboid


class Collision:

    def __init__(self, config):
        self._config = config

        self.printbed = self._read_printbed()
        self.printhead = self._read_printhead()
        self.gantry, self.gantry_x_oriented = self._read_gantry()
        self.gantry_height = config.getfloat("gantry_z_min")
        self.padding = config.getfloat("padding", 5)

        self.current_objects = []

    def _read_printbed(self):
        stepper_configs = [self._config.getsection("stepper_" + axis)
                           for axis in "xyz"]
        min_ = [cfg.getfloat("position_min") for cfg in stepper_configs]
        max_ = [cfg.getfloat("position_max") for cfg in stepper_configs]
        return Cuboid(*min_, *max_)

    def _read_printhead(self):
        """Return a Rectangle representing the size of the print head
        as viewed from above. The printing nozzle would be at (0, 0).
        """
        config = self._config
        return Rectangle(
            -config.getfloat("printhead_x_min"),
            -config.getfloat("printhead_y_min"),
            config.getfloat("printhead_x_max"),
            config.getfloat("printhead_y_max"),
        )

    def _read_gantry(self):
        """Return a Rectangle representing the size of the gantry as viewed
        from above as well as if it is oriented parallel to the X-Axis or not.
        The printing nozzle would be at the 0-coordinate on the other axis.
        """
        config = self._config
        xy_min = config.getfloat("gantry_xy_min")
        xy_max = config.getfloat("gantry_xy_max")
        x_oriented = config.getchoice("gantry_orientation",
                                      {"x": True, "y": False})
        if x_oriented:
            gantry = Rectangle(self.printbed.x, -xy_min,
                               self.printbed.width, xy_max)
        else:
            gantry = Rectangle(-xy_min, self.printbed.y,
                               xy_max, self.printbed.depth)
        return gantry, x_oriented

    def moving_parts(self, print_object):
        """Return collision boxes for the moving parts (printhead and gantry)
        when printing this object. These areas will include all the space
        that these parts could move in when printing the given object.
        """
        moving_printhead = Rectangle(
            print_object.x + self.printhead.x,
            print_object.y + self.printhead.y,
            print_object.max_x + self.printhead.max_x,
            print_object.max_y + self.printhead.max_y,
        )
        if self.gantry_x_oriented:
            moving_gantry = Cuboid(
                self.gantry.x,
                print_object.y + self.gantry.y,
                self.gantry_height,
                self.gantry.max_x,
                print_object.max_y + self.gantry.max_y,
                float('inf'),  # Make the box extend ALL THE WAY to the top
            )
        else:
            moving_gantry = Cuboid(
                print_object.x + self.gantry.x,
                self.gantry.y,
                self.gantry_height,
                print_object.max_x + self.gantry.max_x,
                self.gantry.max_y,
                float('inf'),
            )
        return moving_printhead, moving_gantry

    def printjob_collision(self, new_object):
        if self.printbed.intersection(new_object) != new_object:
            # Doesn't fit in the printer at all!
            return False

        mv_printhead, mv_gantry = self.moving_parts(new_object)
        for obj in self.current_objects:
            if (new_object.collides_with(obj, self.padding) or
                mv_printhead.collides_with(obj.projection(), self.padding) or
                mv_gantry.collides_with(obj, self.padding)):
                return False
        return True
    
    def add_printed_object(self, new_object):
        """Add an object, like a finished print job, to be considered in the
        future.
        """
        self.current_objects.append(new_object)

    def clear_objects(self):
        """Empty the list of print objects to keep track of"""
        self.current_objects.clear()


def load_config(config):
    return Collision(config)
