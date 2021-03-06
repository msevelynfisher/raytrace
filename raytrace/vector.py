import numpy as np

class V3:
    
    def __init__(self, x, y, z):
        xx = np.array(x, dtype = np.float64)
        yy = np.array(y, dtype = np.float64)
        zz = np.array(z, dtype = np.float64)
        
        if xx.shape != yy.shape or xx.shape != zz.shape:
            raise ValueError('Dimension mismatch.')
        
        if len(xx.shape) == 0:
            self.x = xx.reshape((1))
            self.y = yy.reshape((1))
            self.z = zz.reshape((1))
        elif len(xx.shape) == 1:
            self.x = xx
            self.y = yy
            self.z = zz
        else:
            raise ValueError('V3 supports only 0d and 1d arrays.')
    
    def __str__(self):
        return '[\n\t'+str(self.x)+',\n\t'+str(self.y)+',\n\t'+str(self.z)+'\n]'
    
    def __eq__(self, other):
        if isinstance(other, V3):
            return np.logical_and(
                np.abs(self.x - other.x) < 1e-14,
                np.abs(self.y - other.y) < 1e-14,
                np.abs(self.z - other.z) < 1e-14
            )
        else:
            return False
    
    def __len__(self):
        return len(self.x)
    
    def allEqual(self, other):
        if isinstance(other, V3):
            if isinstance(self.x, np.ndarray) or isinstance(other.x, np.ndarray):
                return ((self.x == other.x).all()
                    and (self.y == other.y).all()
                    and (self.z == other.z).all())
            else:
                return self == other
        else:
            return False
    
    def __add__(self, other):
        return V3(self.x + other.x, self.y + other.y, self.z + other.z)
        
    def __sub__(self, other):
        return V3(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def __mul__(self, other):
        if isinstance(other, V3):
            return V3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return V3(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other):
        if isinstance(other, V3):
            return V3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return V3(self.x / other, self.y / other, self.z / other)
    
    def scale(self, scalar):
        return V3(scalar * self.x, scalar * self.y, scalar * self.z)
        
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def normsq(self):
        return self.dot(self)
    
    def norm(self):
        return np.sqrt(self.normsq())
        
    def unit(self):
        return self.scale(1/self.norm())
        
    def cross(self, other):
        return V3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
        
    def mapToXYZ(self, f):
        return V3(f(self.x), f(self.y), f(self.z))
    
    def extract(self, mask):
        return V3(
            np.extract(mask, self.x),
            np.extract(mask, self.y),
            np.extract(mask, self.z)
        )
    
    def place(self, mask, other):
        np.place(self.x, mask, other.x)
        np.place(self.y, mask, other.y)
        np.place(self.z, mask, other.z)
    
    def copyfrom(self, src, casting='same_kind', where=True):
        np.copyto(self.x, src.x, casting, where)
        np.copyto(self.y, src.y, casting, where)
        np.copyto(self.z, src.z, casting, where)
    
    def repeat(self, n):
        return V3(
            np.repeat(self.x, n),
            np.repeat(self.y, n),
            np.repeat(self.z, n)
        )
    
    def where(self, use_first, other):
        return V3(
            np.where(use_first, self.x, other.x),
            np.where(use_first, self.y, other.y),
            np.where(use_first, self.z, other.z)
        )
    
    def clip(self, mn, mx):
        return V3(
            np.clip(self.x, mn, mx),
            np.clip(self.y, mn, mx),
            np.clip(self.z, mn, mx)
        )


class Ray:
    def __init__(self, r, v):
        self.r = r
        self.v = v.unit()
    def __len__(self):
        return len(self.r)
    def trace(self, dist):
        return self.r + self.v * dist
    def extract(self, mask):
        return Ray(
            self.r.extract(mask),
            self.v.extract(mask)
        )
    def transform(self, transform):
        return Ray(
            transform.apply(self.r),
            transform.apply(self.v).unit()
        )
