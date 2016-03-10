import math
import border
import const

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
  
def mirror_point_into_field(point):
    """
    Mirrors a Point at the border if it is out of the boundarys
    :param bag: the bag used in this program
    :param point: the to mirroring point
    :return: the mirrored point
    """
    bordervalue = check_for_out_of_field(point)
    while bordervalue > 0:
	  point = mirror_point_at_border(point, bordervalue)
	  bordervalue = check_for_out_of_field(point)
    return point
   
def mirror_point_at_border(point, bordervalue):
    yPosition = point[1]
    xPosition = point[0]
    #TODO Stosszahl einberechnen beim Bandenabprall
    if bordervalue == border.border.xBy0:
      xPosition = const.CONST.xBorderBy0 - (xPosition - const.CONST.xBorderBy0)
    if bordervalue == border.border.xBy1:
      xPosition = const.CONST.xBorderBy1 - (xPosition - const.CONST.xBorderBy1)
    if bordervalue == border.border.yBy0:
      yPosition = const.CONST.yBorderBy0 -(yPosition - const.CONST.yBorderBy0)
    if bordervalue == border.border.yBy1:
      yPosition = const.CONST.yBorderBy1 -(yPosition - const.CONST.yBorderBy1)
    return (xPosition, yPosition)
   
   
def check_for_out_of_field(point):
  if point[0] < const.CONST.xBorderBy0:
    return border.border.xBy0
  if point[0] > const.CONST.xBorderBy1:
    return border.border.xBy1
  if point[1] < const.CONST.yBorderBy0:
    return border.border.yBy0
  if point[1] > const.CONST.yBorderBy1:
    return border.border.yBy1
  return border.border.infield 
   
