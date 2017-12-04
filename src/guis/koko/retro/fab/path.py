import ctypes

class Path(object):

    def __init__(self, segments, nijk, dxyz, minxyz):
        self.segments = segments
        self.ni,   self.nj,   self.nk = nijk
        self.dx,   self.dy,   self.dz = dxyz
        self.xmin, self.ymin, self.zmin = minxyz

        self._vdata = None

    @property
    def vdata(self):
        if self._vdata is not None:  return self._vdata

        count = sum(map(lambda s: len(s)+2, self.segments))
        self._vdata = (ctypes.c_float*(count*4))()

        def xyz(pt):
            ''' Helper function to convert from lattice coordinates to
                real-space (mm) coordinates.'''
            return [pt[0]*self.dx/self.ni + self.xmin,
                    pt[1]*self.dy/self.nj + self.ymin,
                    pt[2]*self.dz/self.nk + self.zmin]

        vindex = 0
        for s in self.segments:
            self._vdata[vindex:vindex+4] = xyz(s[0]) + [0]
            vindex += 4

            for pt in s:
                self._vdata[vindex:vindex+4] = xyz(pt) + [0.3]
                vindex += 4

            self._vdata[vindex:vindex+4] = xyz(s[-1]) + [0]
            vindex += 4

        return self._vdata

    @classmethod
    def load(cls, filename):
        paths = []
        with open(filename, 'r') as f:
            f.readline()
            f.readline()
            nx, ny, nz = map(int, f.readline().split(' ')[-3:])
            dx, dy, dz = map(float, f.readline().split(' ')[-3:])
            xmin, ymin, zmin = map(float, f.readline().split(' ')[-3:])

            segments = []
            current  = []
            line = f.readline()
            complete = False
            while line:
                if 'segment end:' in line:
                    segments.append(current)
                elif 'segment start:' in line:
                    current = []
                elif 'path start:' in line:
                    pass
                elif 'path end:' in line:
                    complete = True
                else:
                    current.append(map(int, line.split(' ')[:-1]))
                line = f.readline()

        if not complete:
            return None
        return Path(segments, (nx, ny, nz), (dx, dy, dz), (xmin, ymin, zmin))
