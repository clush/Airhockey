import math


def length(v):
    """
    Returns the length of a vector.
    :param v:
    :return:
    """
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def normalize(v):
    """
    Normalizes a vector.
    :param v:
    :return:
    """
    l = length(v)
    if l == 0.0:
        return 0, 0
    return v[0] / l, v[1] / l


def from_to(p1, p2):
    """
    Returns the vector from point 1 to point 2.
    :param p1:
    :param p2:
    :return:
    """
    return p2[0] - p1[0], p2[1] - p1[1]


def add(v1, v2):
    """
    Adds two vectors.
    :param v1:
    :param v2:
    :return:
    """
    return v1[0] + v2[0], v1[1] + v2[1]


def scale(v, x, y):
    """
    Scales a vector by x in x direction and by y in y direction.
    :param v:
    :param x:
    :param y:
    :return:
    """
    return v[0] * x, v[1] * y


def mul_by(v, x):
    """
    Multiplies a vector by a scalar value.
    :param v:
    :param x:
    :return:
    """
    return scale(v, x, x)


def round(v):
    """
    Rounds the components of a vector.
    :param v:
    :return:
    """
    return int(v[0]), int(v[1])


def dot(v1, v2):
    """
    Computes the dot product of two vectors.
    :param v1:
    :param v2:
    :return:
    """
    return v1[0] * v2[0] + v1[1] * v2[1]


def image_to_coord_space(v, boundaries):
    """
    Converts a vector from image space ((0, 0) to (w, h)) to coordinate space ((0, 0) to (1, 1)) inside the boundaries
    :param v:
    :param boundaries:
    :return:
    """
    offset = (v[0] - boundaries[0][0], v[1] - boundaries[0][1])
    return scale(offset, 1.0 / (boundaries[1][0] - boundaries[0][0]), 1.0 / (boundaries[1][1] - boundaries[0][1]))


def coord_to_image_space(v, boundaries):
    """
    Converts a vector from coordinate space ((0, 0) to (1, 1)) inside the boundaries to image space ((0, 0) to (w, h))
    :param v:
    :param boundaries:
    :return:
    """
    scaled = scale(v, boundaries[1][0] - boundaries[0][0], boundaries[1][1] - boundaries[0][1])
    return round((scaled[0] + boundaries[0][0], scaled[1] + boundaries[0][1]))
