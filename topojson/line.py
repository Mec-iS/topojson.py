"""
Functions to treat coordinates in a Line.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from topojson.arcs import Arcs
from topojson.utils import point_compare, is_point, Strut


class Line:
    """
    A class to build a topology from a Line object.
    
    :param Q: scientific notation for the level of quantization (ie. 1e4)
    """
    def __init__(self, Q):
        self.arcs = Arcs(Q)
        self.line_arcs = []

    @classmethod
    def mysterious_line_test(cls, a, b):
        """Test equality plus a type check"""
        for arg in (a, b):
            if not isinstance(arg, list):
                return True
        return a == b

    def arc(self, current_arc, last=False):
        n = len(current_arc)
        if last and not len(self.line_arcs) and n == 1:
            point = current_arc[0]
            index = self.arcs.get_index(point)
            if len(index):
                self.line_arcs.append(index[0])
            else:
                index.append(self.arcs.length)
                self.line_arcs.append(index[0])
                self.arcs.push(current_arc)
        elif n > 1:
            self.line_arcs.append(self.arcs.check(current_arc))

    def line(self, points, opened):
        """
        Transform a set of points.
        
        :param points: an array of points
        :param opened: 
        :return: 
        """
        n = len(points)
        current_arc = Strut()
        k = 0
        p = False
        t = False
        if not opened:
            points.pop()
            n -= 1
        while k < n:
            t = self.arcs.peak(points[k])
            if opened:
                break
            if p and not self.mysterious_line_test(p, t):
                t_inp = all(map(lambda line: line in p, t))
                p_int = all(map(lambda line: line in t, p))
                if t_inp and not p_int:
                    k -= 1
                break
            p = t
            k += 1
        # If no shared starting point is found for closed lines, rotate to minimum.
        if k == n and isinstance(p, list) and len(p) > 1:
            point0 = points[0]
            i = 2
            k = 0
            while i<n:
                point = points[i]
                if point_compare(point0, point) > 0:
                    point0 = point
                    k = i
                i += 1
        i = -1
        if opened:
            m = n-1
        else:
            m = n
        while i < m:
            i += 1
            point = points[(i + k) % n]
            p = self.arcs.peak(point)
            if not self.mysterious_line_test(p, t):
                t_inp = all(map(lambda line: line in p, t))
                p_int = all(map(lambda line: line in t, p))
                if t_inp:
                    current_arc.append(point)
                self.arc(current_arc)
                if not t_inp and not p_int and len(current_arc):
                    self.arc(Strut([current_arc[-1], point]))
                if p_int and len(current_arc):
                    current_arc = Strut([current_arc[-1]])
                else:
                    current_arc = Strut()
            if not len(current_arc) or point_compare(current_arc[-1], point):
                current_arc.append(point) # skip duplicate points
            t = p
        self.arc(current_arc, True)
        return self.line_arcs

    def line_closed(self, points):
        return self.line(points,False)

    def line_open(self, points):
        return self.line(points,True)

    def map_func (self, arc):
        """Map function for a line, to be passed in `self.arcs.map()`"""
        if len(arc) == 2 and type(arc[0]) == type(1):
            arc = [arc]
        i = 1
        n = len(arc)
        point = arc[0]
        x1 = point[0]
        x2 = dx = y2 = dy = False
        y1 = point[1]
        points = [[int(x1), int(y1)]]
        while i < n:
            point = arc[i]
            if not is_point(point):
                i += 1
                continue
            x2 = point[0]
            y2 = point[1]
            dx = int(x2 - x1)
            dy = int(y2 - y1)
            if dx or dy:
                points.append([dx, dy])
                x1 = x2
                y1 = y2
            i += 1
        return points

    def get_arcs(self):
        return self.arcs.map(self.map_func)
