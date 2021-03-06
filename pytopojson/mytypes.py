"""
A module with data types used for calculating topologies.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
GEOMETRY_TYPES = (
  'LineString',
  'MultiLineString',
  'MultiPoint',
  'MultiPolygon',
  'Point',
  'Polygon',
  'GeometryCollection'
)


class Types:
    """
    A collection of Types.
    """
    def __init__(self, obj=None):
        self.obj(obj)
        self.outObj = None
        self.coords = list()

    def Feature(self,feature):
        if 'geometry' in feature:
            self.geometry(feature['geometry'])

    def FeatureCollection(self, collection):
        for feature in collection['features']:
            self.Feature(feature)

    def GeometryCollection(self, collection):
        if 'geometry' in collection:
            for geometry in collection['geometries']:
                self.geometry(geometry)

    def LineString(self, lineString):
        self.line(lineString['coordinates'])

    def MultiLineString(self, multiLineString):
        for coordinate in multiLineString['coordinates']:
            self.line(coordinate)

    def MultiPoint(self, multiPoint):
        for coordinate in multiPoint['coordinates']:
            self.point(coordinate)

    def MultiPolygon(self, multiPolygon):
        for coordinate in multiPolygon['coordinates']:
            self.polygon(coordinate)

    def Point(self, point):
        self.point(point['coordinates'])

    def Polygon(self, polygon):
        self.polygon(polygon['coordinates'])

    def obj(self, obj):
        if obj is None:
            self.outObj = None
        elif 'type' not in obj:
            self.outObj = dict()
            for fName in obj:
                self.outObj[fName] = self.FeatureCollection(obj[fName])
        elif obj['type'] == 'Feature':
            self.outObj = self.Feature(obj)
        elif obj['type'] == 'FeatureCollection':
            self.outObj = self.FeatureCollection(obj)
        elif obj['type'] in GEOMETRY_TYPES:
            self.outObj = self.geometry(obj)
        return self.outObj

    def geometry(self, geometry):
        if geometry is not None and geometry['type'] not in GEOMETRY_TYPES:
            raise ValueError('Type not allowed. Allowed types are {}'.format(str(GEOMETRY_TYPES)))
        elif geometry['type'] == 'LineString':
            return self.LineString(geometry)
        elif geometry['type'] == 'MultiLineString':
            return self.MultiLineString(geometry)
        elif geometry['type'] == 'MultiPoint':
            return self.MultiPoint(geometry)
        elif geometry['type'] == 'MultiPolygon':
            return self.MultiPolygon(geometry)
        elif geometry['type'] == 'Point':
            return self.Point(geometry)
        elif geometry['type'] == 'Polygon':
            return self.Polygon(geometry)
        elif geometry['type'] == 'GeometryCollection':
            return self.GeometryCollection(geometry)

    def point(self, coordinate):
        self.coords.append(coordinate)

    def line(self, coordinates):
        for coordinate in coordinates:
            self.point(coordinate)

    def polygon(self, coordinates):
        for coordinate in coordinates:
            self.line(coordinate)
