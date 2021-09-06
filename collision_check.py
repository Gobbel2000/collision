from geometry import Rectangle, Cuboid

def config_to_cuboids(config):
    x = config["printbed_x_min"]
    y = config["printbed_y_min"]
    width = config["printbed_x_max"] - x
    depth = config["printbed_y_max"] - y
    height = config["printbed_height"]
    printbed = Cuboid(x, y, 0, width, depth, height)

    x = config["printhead_x_min"]
    y = config["printhead_y_min"]
    width = config["printhead_x_max"] - x
    depth = config["printhead_y_max"] - y
    height = config["gantry_z_min"]
    printhead = Cuboid(x, y, 0, width, depth, height)

    point = config["gantry_xy_min"]
    width = config["gantry_xy_max"] - point
    if config["gantry_orientation"] == "x":
        gantry = Rectangle(printbed.x, point, printbed.width, width)
    elif config["gantry_orientation"] == "y":
        gantry = Rectangle(point, printbed.y, width, printbed.depth)

    return printbed, printhead, gantry

def moving_parts(printhead, gantry, print_object):
    """Return collision boxes for the moving parts when printing this object"""
    return [printhead, gantry] #TODO

def printjob_collision(printbed, printhead, gantry, current_objects, new_object):
    if printbed.intersection(new_object) != new_object:
        # Doesn't fit in the printer at all!
        return False

    for obj in current_objects + moving_parts(printhead, gantry, new_object):
        if new_object.collides_with(obj):
            return False
    return True
