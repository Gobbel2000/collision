class Rectangle:

    def __init__(self, x, y, max_x, max_y):
        if max_x < x:
            x, max_x = max_x, x
        if max_y < y:
            y, max_y = max_y, y
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y

        self.width = max_x - x
        self.height = max_y - y
        self.area = self.width * self.height

    def __bool__(self):
        """Consider a rectangle as true if and only if its area is nonzero"""
        return bool(self.area)

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.max_x == other.max_x and
                self.max_y == other.max_y)

    def intersection(self, other):
        """Return the intersection between two rectangles.
        This is always a rectangle, but may have no area if both rectangles are disjoint.
        """
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        max_x = min(self.max_x, other.max_x)
        max_y = min(self.max_y, other.max_y)
        return Rectangle(x, y, max(max_x, x), max(max_y, y))

    def collides_with(self, other):
        """Return, whether this rectangle collides with another rectangle"""
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        max_x = min(self.max_x, other.max_x)
        max_y = min(self.max_y, other.max_y)
        return max_x > x and max_y > y

    def with_border(self, other):
        """Return a new Rectangle by adding a border based on the
        dimensions of other. """
        pass


class Cuboid:

    def __init__(self, x, y, z, max_x, max_y, max_z):
        if max_x < x:
            x, max_x = max_x, x
        if max_y < y:
            y, max_y = max_y, y
        if max_z < z:
            z, max_z = max_z, z
        self.x = x
        self.y = y
        self.z = z
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z

        self.width = max_x - x
        self.depth = max_y - y
        self.height = max_z - z
        self.volume = self.width * self.depth * self.height

    def __bool__(self):
        return bool(self.volume)

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z and
                self.max_x == other.max_x and
                self.max_y == other.max_y and
                self.max_z == other.max_z)

    def intersection(self, other):
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        z = max(self.z, other.z)
        max_x = min(self.max_x, other.max_x)
        max_y = min(self.max_y, other.max_y)
        max_z = min(self.max_z, other.max_z)
        return Cuboid(x, y, z, max(max_x, x), max(max_y, y), max(max_z, z))

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
            return Rectangle(self.y, self.z, self.max_y, self.max_z)
        elif axis == 1:  # Remove Y-axis
            return Rectangle(self.x, self.z, self.max_x, self.max_z)
        elif axis == 2:  # Remove Z-axis
            return Rectangle(self.x, self.y, self.max_x, self.max_y)
