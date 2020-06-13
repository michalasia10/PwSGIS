from qgis import *

# zad1
warstwa = iface.activeLayer()
features = [i for i in warstwa.getFeatures()]

for i in range(len(features)):
    type = QgsWkbTypes.displayString(features[i].geometry().wkbType())
print(type)


# zad2
class Building_select:
    def __init__(self, file, changeX, changeY, pick):
        self.file = file
        self.changeX = changeX
        self.changeY = changeY
        self.pick = pick
        self.shift()

    def add(self):
        """
        Funkcja przyjmuje plik, w zaleĹĽnoĹ›ci od rozszerzenia zapisuje jako warste VectorowÄ… lub RastrtowÄ…
        """
        projekt = QgsProject.instance()
        projekt.fileName()
        (filepath, filename) = os.path.split(self.file)
        (name, extension) = os.path.splitext(filename)
        if extension == ".shp":
            try:
                vector = iface.addVectorLayer(os.path.join(filepath, filename), "new", "ogr")
                return vector
            except:
                print("Sth is wrong with value")
        elif extension == ".tif":
            try:
                raster = iface.addRasterLayer(file)
                return raster
            except:
                print("Sth is wrong with value")
        else:
            print("Sth is wrong with value")

    def check_type(self):
        warstwa = self.add()
        #        warstwa = iface.activeLayer()
        features = [i for i in warstwa.getFeatures()][:self.pick]
        for i in range(len(features)):
            type = QgsWkbTypes.displayString(features[i].geometry().wkbType())
        print(type)
        return type

    def shift(self):
        warstwa = self.add()
        features = [obiekt for obiekt in warstwa.getFeatures()][:self.pick]

        typ = self.check_type()
        type = f'as{typ}()'

        mem_layer = QgsVectorLayer(f"{typ}", "tymczasowe", "memory")
        pr = mem_layer.dataProvider()

        nowe = []
        old_geom = [x.geometry().asMultiPolygon() for x in features]

        for i in range(len(old_geom) - 1):
            for pt in old_geom[i][0]:
                new_pt = [pt[j] + QgsVector(self.changeX, self.changeY) for j in range(len(pt))]
                nowe.append(new_pt)

        for j in range(len(nowe)):
            bufor = QgsFeature(j)
            bufor.setGeometry(QgsGeometry.fromPolygonXY([nowe[j]]))
            pr.addFeatures([bufor])

        QgsProject.instance().addMapLayer(mem_layer)


new = Building_select(file='C:/Users/misie/Downloads/budynki_select.shp', changeX=100, changeY=200, pick=10)
# new.check_type()
