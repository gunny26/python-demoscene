########################################################################
import operator
import math
 
class Vec3d(object):
    """3d vector class, supports vector and scalar operators,
    and also provides a bunch of high level functions.
    reproduced from the vec2d class on the pygame wiki site.
    """
    __slots__ = ['x', 'y', 'z']
 
    def __init__(self, x_or_triple, y = None, z = None):
        if y == None:
            self.x = x_or_triple[0]
            self.y = x_or_triple[1]
            self.z = x_or_triple[2]
        else:
            self.x = x_or_triple
            self.y = y
            self.z = z
 
    def __len__(self):
        return 3
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec3d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec3d")
 
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec3d(%s, %s, %s)' % (self.x, self.y, self.z)
    
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return self.x == other[0] and self.y == other[1] and self.z == other[2]
        else:
            return False
    
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return self.x != other[0] or self.y != other[1] or self.z != other[2]
        else:
            return True
 
    def __nonzero__(self):
        return self.x or self.y or self.z
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec3d"
        if isinstance(other, Vec3d):
            return Vec3d(f(self.x, other.x),
                         f(self.y, other.y),
                         f(self.z, other.z))
        elif (hasattr(other, "__getitem__")):
            return Vec3d(f(self.x, other[0]),
                         f(self.y, other[1]),
                         f(self.z, other[2]))
        else:
            return Vec3d(f(self.x, other),
                         f(self.y, other),
                         f(self.z, other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec3d"
        if (hasattr(other, "__getitem__")):
            return Vec3d(f(other[0], self.x),
                         f(other[1], self.y),
                         f(other[2], self.z))
        else:
            return Vec3d(f(other, self.x),
                         f(other, self.y),
                         f(other, self.z))
 
    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
            self.z = f(self.z, other[2])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
            self.z = f(self.z, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)
        elif hasattr(other, "__getitem__"):
            return Vec3d(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            return Vec3d(self.x + other, self.y + other, self.z + other)

    __radd__ = __add__
    
    def __iadd__(self, other):
        if isinstance(other, Vec3d):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        else:
            self.x += other
            self.y += other
            self.z += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)
        elif (hasattr(other, "__getitem__")):
            return Vec3d(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            return Vec3d(self.x - other, self.y - other, self.z - other)
    def __rsub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(other.x - self.x, other.y - self.y, other.z - self.z)
        if (hasattr(other, "__getitem__")):
            return Vec3d(other[0] - self.x, other[1] - self.y, other[2] - self.z)
        else:
            return Vec3d(other - self.x, other - self.y, other - self.z)
    def __isub__(self, other):
        if isinstance(other, Vec3d):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
        else:
            self.x -= other
            self.y -= other
            self.z -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x*other.x, self.y*other.y, self.z*other.z)
        if (hasattr(other, "__getitem__")):
            return Vec3d(self.x*other[0], self.y*other[1], self.z*other[2])
        else:
            return Vec3d(self.x*other, self.y*other, self.z*other)

    __rmul__ = __mul__
    
    def __imul__(self, other):
        if isinstance(other, Vec3d):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
            self.z *= other[2]
        else:
            self.x *= other
            self.y *= other
            self.z *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return Vec3d(operator.neg(self.x), operator.neg(self.y), operator.neg(self.z))
 
    def __pos__(self):
        return Vec3d(operator.pos(self.x), operator.pos(self.y), operator.pos(self.z))
 
    def __abs__(self):
        return Vec3d(abs(self.x), abs(self.y), abs(self.z))
 
    def __invert__(self):
        return Vec3d(-self.x, -self.y, -self.z)
 
    # vectory functions
    def get_length_sqrd(self): 
        """length of vector according to formula"""
        return self.x**2 + self.y**2 + self.z**2
 
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)      
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
        self.z *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")
        
    def rotate_around_z(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotate_around_x(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        y = self.y*cos - self.z*sin
        z = self.y*sin + self.z*cos
        self.y = y
        self.z = z
 
    def rotate_around_y(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        z = self.z*cos - self.x*sin
        x = self.z*sin + self.x*cos
        self.z = z
        self.x = x
 
    def rotated_around_z(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec3d(x, y, self.z)
    
    def rotated_around_x(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        y = self.y*cos - self.z*sin
        z = self.y*sin + self.z*cos
        return Vec3d(self.x, y, z)
    
    def rotated_around_y(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        z = self.z*cos - self.x*sin
        x = self.z*sin + self.x*cos
        return Vec3d(x, self.y, z)
    
    def get_angle_around_z(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle_around_z(self, angle_degrees):
        self.x = math.sqrt(self.x**2 + self.y**2)
        self.y = 0
        self.rotate_around_z(angle_degrees)
    angle_around_z = property(get_angle_around_z, __setangle_around_z, None, "gets or sets the angle of a vector in the XY plane")
 
    def get_angle_around_x(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.z, self.y))
    def __setangle_around_x(self, angle_degrees):
        self.y = math.sqrt(self.y**2 + self.z**2)
        self.z = 0
        self.rotate_around_x(angle_degrees)
    angle_around_x = property(get_angle_around_x, __setangle_around_x, None, "gets or sets the angle of a vector in the YZ plane")
 
    def get_angle_around_y(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.x, self.z))
    def __setangle_around_y(self, angle_degrees):
        self.z = math.sqrt(self.z**2 + self.x**2)
        self.x = 0
        self.rotate_around_y(angle_degrees)
    angle_around_y = property(get_angle_around_y, __setangle_around_y, None, "gets or sets the angle of a vector in the ZX plane")
 
    def get_angle_between(self, other):
        v1 = self.normalized()
        v2 = Vec3d(other)
        v2.normalize_return_length()
        return math.degrees(math.acos(v1.dot(v2)))
            
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec3d(self)
 
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return length
 
    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1] + self.z*other[2])
        
    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2 + (self.z - other[2])**2)
        
    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2 + (self.z - other[2])**2
        
    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1] + other[2]*other[2]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Vec3d(x, y, 1)
    
    def cross(self, other):
        return Vec3d(self.y*other[2] - self.z*other[1], self.z*other[0] - self.x*other[2], self.x*other[1] - self.y*other[0])
    
    def interpolate_to(self, other, range):
        return Vec3d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range, self.z + (other[2] - self.z)*range)
    
    def convert_to_basis(self, x_vector, y_vector, z_vector):
        return Vec3d(self.dot(x_vector)/x_vector.get_length_sqrd(),
            self.dot(y_vector)/y_vector.get_length_sqrd(),
            self.dot(z_vector)/z_vector.get_length_sqrd())
 
    def __getstate__(self):
        return [self.x, self.y, self.z]
        
    def __setstate__(self, dict):
        self.x, self.y, self.z = dict
        
########################################################################
## Unit Testing                                                       ##
########################################################################
if __name__ == "__main__":
 
    import unittest
    import pickle
 
    ####################################################################
    class UnitTestVec3d(unittest.TestCase):
    
        def setUp(self):
            pass
        
        def testCreationAndAccess(self):
            v = Vec3d(111,222,333)
            self.assert_(v.x == 111 and v.y == 222 and v.z == 333)
            v.x = 333
            v[1] = 444
            v.z = 555
            self.assert_(v[0] == 333 and v[1] == 444 and v[2] == 555)
 
        def testMath(self):
            v = Vec3d(111,222,333)
            self.assertEqual(v + 1, Vec3d(112,223,334))
            self.assert_(v - 2 == [109,220,331])
            self.assert_(v * 3 == (333,666,999))
            self.assert_(v / 2.0 == Vec3d(55.5, 111, 166.5))
            self.assert_(v / 2 == (55, 111, 166))
            self.assert_(v ** Vec3d(2,3,2) == [12321, 10941048, 110889])
            self.assert_(v + [-11, 78, 67] == Vec3d(100, 300, 400))
            self.assert_(v / [11,2,9] == [10,111,37])
 
        def testReverseMath(self):
            v = Vec3d(111,222,333)
            self.assert_(1 + v == Vec3d(112,223,334))
            self.assert_(2 - v == [-109,-220,-331])
            self.assert_(3 * v == (333,666,999))
            self.assert_([222,999,666] / v == [2,4,2])
            self.assert_([111,222,333] ** Vec3d(2,3,2) == [12321, 10941048, 110889])
            self.assert_([-11, 78,67] + v == Vec3d(100, 300, 400))
 
        def testUnary(self):
            v = Vec3d(111,222,333)
            v = -v
            self.assert_(v == [-111,-222,-333])
            v = abs(v)
            self.assert_(v == [111,222,333])
 
        def testLength(self):
            v = Vec3d(1,4,8)
            self.assert_(v.length == 9)
            self.assert_(v.get_length_sqrd() == 81)
            self.assert_(v.normalize_return_length() == 9)
            self.assert_(v.length == 1)
            v.length = 9
            self.assert_(v == Vec3d(1,4,8))
            v2 = Vec3d(10, -2, 12)
            self.assert_(v.get_distance(v2) == (v - v2).get_length())
            
        def testAngles(self):            
            v = Vec3d(0, 3, -3)
            self.assertEquals(v.angle_around_y, 180)
            self.assertEquals(v.angle_around_x, -45)
            self.assertEquals(v.angle_around_z, 90)
 
            v2 = Vec3d(v)
            v.rotate_around_x(-90)
            self.assertEqual(v.get_angle_between(v2), 90)
 
            v = Vec3d(v2)
            v.rotate_around_y(-90)
            self.assertAlmostEqual(v.get_angle_between(v2), 60)
 
            v = Vec3d(v2)
            v.rotate_around_z(-90)
            self.assertAlmostEqual(v.get_angle_between(v2), 60)
 
            v2.angle_around_z -= 90
            self.assertEqual(v.length, v2.length)
            self.assertEquals(v2.angle_around_z, 0)
            self.assertEqual(v2, [3, 0, -3])
            self.assert_((v - v2).length > .00001)
            self.assertEqual(v.length, v2.length)
            v2.rotate_around_y(300)
            self.assertAlmostEquals(v.get_angle_between(v2), 60)
            v2.rotate_around_y(v2.get_angle_between(v))
            angle = v.get_angle_between(v2)
            self.assertAlmostEquals(v.get_angle_between(v2), 0)  
 
        def testHighLevel(self):
            basis0 = Vec3d(5.0, 0, 0)
            basis1 = Vec3d(0, .5, 0)
            basis2 = Vec3d(0, 0, 3)
            v = Vec3d(10, 1, 6)
            self.assert_(v.convert_to_basis(basis0, basis1, basis2) == [2, 2, 2])
            self.assert_(v.projection(basis0) == (10, 0, 0))
            self.assert_(basis0.dot(basis1) == 0)
            
        def testCross(self):
            lhs = Vec3d(1, .5, 3)
            rhs = Vec3d(4, 6, 1)
            self.assert_(lhs.cross(rhs) == [-17.5, 11, 4])
            
        def testComparison(self):
            int_vec = Vec3d(3, -2, 4)
            flt_vec = Vec3d(3.0, -2.0, 4.0)
            zero_vec = Vec3d(0, 0, 0)
            self.assert_(int_vec == flt_vec)
            self.assert_(int_vec != zero_vec)
            self.assert_((flt_vec == zero_vec) == False)
            self.assert_((flt_vec != int_vec) == False)
            self.assert_(int_vec == (3, -2, 4))
            self.assert_(int_vec != [0, 0, 0])
            self.assert_(int_vec != 5)
            self.assert_(int_vec != [3, -2, 4, 15])
        
        def testInplace(self):
            inplace_vec = Vec3d(5, 13, 17)
            inplace_ref = inplace_vec
            inplace_src = Vec3d(inplace_vec)
            inplace_vec *= .5
            inplace_vec += .5
            inplace_vec /= (3, 6, 9)
            inplace_vec += Vec3d(-1, -1, -1)
            alternate = (inplace_src*.5 + .5)/Vec3d(3, 6, 9) + [-1, -1, -1]
            self.assertEquals(inplace_vec, inplace_ref)
            self.assertEquals(inplace_vec, alternate)
        
        def testPickle(self):
            testvec = Vec3d(5, .3, 8.6)
            testvec_str = pickle.dumps(testvec)
            loaded_vec = pickle.loads(testvec_str)
            self.assertEquals(testvec, loaded_vec)
    
    ####################################################################
    unittest.main()
 
    ######################################################################## 
