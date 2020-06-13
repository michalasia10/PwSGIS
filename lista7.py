from qgis import *


# zad1
def check_file(file):
    """
    Funkcja przyjmuje plik, w zależności od rozszerzenia zapisuje jako warste Vectorową lub Rastrtową
    """
    projekt = QgsProject.instance()
    projekt.fileName()
    (filepath, filename) = os.path.split(file)
    (name, extension) = os.path.splitext(filename)
    if extension == ".shp":
        try:
            vector = iface.addVectorLayer(os.path.join(filepath, filename), "new", "ogr")
            return vector
        except ValueError:
            print("Sth is wrong with value")
    elif extension == ".tif":
        try:
            raster = iface.addRasterLayer(file)
            return raster
        except ValueError:
            print("Sth is wrong with value")
    else:
        print("Sth is wrong with value")


raster = check_file('C:/Users/misie/Downloads/bogota.tif')


# zad2
def safe(raster, path):
    """
    Po dodaniu przez poprzednia funkcje warstwy rastrowej,
    funkcja safe zapisze wysokość,szerokość, zakres, typ rastra, liczbe kanałów oraz układ odniesienie
    :param raster: object = check_file(path in string)
    :param path: string
    :return: file with dict
    """
    import json
    dane = {'width': raster.width(),
            'height': raster.height(),
            'extent': raster.extent().toString(),
            'type': raster.rasterType(),
            'band_number': raster.bandCount(),
            'crs': raster.crs().authid()}
    with open(path, 'w') as file:
        file.write(json.dumps(dane))


safe(raster, 'C:/Users/misie/Desktop/file1.txt')

zad3


class Builings:

    def __init__(self, name, spot, filepath, value):
        """

        :param name: string
        :param spot: string
        :param filepath: path/string
        :param value: string
        """
        self.name = name
        self.spot = spot
        self.filepath = filepath
        self.value = value
        self.project()
        self.load()
        self.count()

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.__name

    @property
    def spot(self):
        return self.__spot

    @property
    def filepath(self):
        return self.__filepath

    @property
    def value(self):
        return self.__value

    @name.setter
    def name(self, name):
        self.__name = name

    @spot.setter
    def spot(self, spot):
        self.__spot = spot

    @filepath.setter
    def filepath(self, filepath):
        self.__filepath = filepath

    @value.setter
    def value(self, value):
        self.__value = value

    def project(self):
        projekt = QgsProject.instance()
        projekt.setFileName(self.name)
        projekt.write(self.spot)
        projekt.read(self.spot)
        return projekt.fileName()

    def load(self):
        """
        Funkcja ładuje nową warstwe z ścieżki podaje i szuka pliku 'Budynki_JG.shp'
        :return: zwraca vector
        """
        vector = iface.addVectorLayer(os.path.join(self.filepath, 'Budynki_JG.shp'), "budynki", "ogr")
        return vector

    def count(self):
        """
        Funkcja ma na celu obliczenie powierzchni dla kolumny 'building'  dla szukanego obiektu "value"
        iteracja po wszystkich obiektach w celu spełnienia warunku
        """
        warstwa = self.load()
        #        warstwa = iface.activeLayer()
        pr = warstwa.dataProvider()
        pr.addAttributes([QgsField('Nowa', QVariant.Double)])
        warstwa.updateFields()
        sum = 0
        #        próbba printu sumy
        with edit(warstwa):
            for obiekt in warstwa.getFeatures(QgsFeatureRequest(QgsExpression(f"\"building\"= '{self.value}' "))):
                sum += obiekt.geometry().area()
            print(sum)


#            for obiekt in warstwa.getFeatures():
#                if obiekt['building'] == '{self.value}':
#                    obiekt.setAttribute(obiekt.fieldNameIndex('Nowa'), obiekt.geometry().area())
#                sum += obiekt.geometry().area()
#                warstwa.updateFeature(obiekt)
#        print(sum)
#
new = Builings(name='Projekt', spot='C:/Users/misie/Desktop/', filepath='C:/Users/misie/Downloads/',
               value='residential')

# praca wykonana przez Michał Lasia @115485