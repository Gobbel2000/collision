class Rectangle:

    def __init__(self, x, y, width, height):
        if width < 0:
            x += width
            width *= -1
        if height < 0:
            y += height
            height *= -1
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.max_x = x + width
        self.max_y = y + height
        self.area = width * height

    def __bool__(self):
        """Consider a rectangle as true if and only if its area is nonzero"""
        return bool(self.area)

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.width == other.width and
                self.height == other.height)

    def intersection(self, other):
        """Return the intersection between two rectangles.
        This is always a rectangle, but may have no area if both rectangles are disjoint.
        """
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        width = min(self.max_x, other.max_x) - x
        height = min(self.max_y, other.max_y) - y
        return Rectangle(x, y, max(width, 0), max(height, 0))

    def collides_with(self, other):
        """Return, whether this rectangle collides with another rectangle"""
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        max_x = min(self.max_x, other.max_x)
        max_y = min(self.max_y, other.max_y)
        return max_x > x and max_y > y
        

    def resize(self, width=0, height=0):
        """Return a new Rectangle that is grown or shrunk from the center in
        both directions for each dimension"""
        return Rectangle(self.x-width, self.y-height,
                         self.width + 2*width, self.height + 2*height)


class Cuboid:

    def __init__(self, x, y, z, width, depth, height):
        if width < 0:
            x += width
            width *= -1
        if depth < 0:
            y += depth
            depth *= -1
        if height < 0:
            z += height
            height *= -1
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.height = height

        self.max_x = x + width
        self.max_y = y + depth
        self.max_z = z + height
        self.volume = width * depth * height

    def __bool__(self):
        return bool(self.volume)

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z and
                self.width == other.width and
                self.depth == other.depth and
                self.height == other.height)

    def intersection(self, other):
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        z = max(self.z, other.z)
        width = min(self.max_x, other.max_x) - x
        depth = min(self.max_y, other.max_y) - y
        height = min(self.max_z, other.max_z) - z
        return Cuboid(x, y, z, max(width, 0), max(depth, 0), max(height, 0))

    def collides_with(self, other):
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        z = max(self.z, other.z)
        max_x = min(self.max_x, other.max_x)
        max_y = min(self.max_y, other.max_y)
        max_z = min(self.max_z, other.max_z)
        return max_x > x and max_y > y and max_z > z

    def projection(self, axis=2):
        """Project the cuboid to a paraxial rectangle"""
        if axis == 0:  # Remove X-axis
            return Rectangle(self.y, self.z, self.depth, self.height)
        elif axis == 1:  # Remove Y-axis
            return Rectangle(self.x, self.z, self.width, self.height)
        elif axis == 2:  # Remove Z-axis
            return Rectangle(self.x, self.y, self.width, self.depth)

    def resize(self, width=0, depth=0, height=0):
        """Return a new Rectangle that is grown or shrunk from the center in
        both directions for each dimension"""
        return Cuboid(self.x-width, self.y-depth, self.z-height,
                      self.width + 2*width, self.depth + 2*depth,
                      self.height + 2*height)
