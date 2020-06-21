class Bird:

    def __init__(self, name, spot, filepath):
        """

        :param name: string
        :param spot: string
        :param filepath: path/string
        """
        self.name = name
        self.spot = spot
        self.filepath = filepath

        self.project()
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

    @name.setter
    def name(self, name):
        self.__name = name

    @spot.setter
    def spot(self, spot):
        self.__spot = spot

    @filepath.setter
    def filepath(self, filepath):
        self.__filepath = filepath

    def project(self):
        projekt = QgsProject.instance()
        projekt.setFileName(self.name)
        projekt.write(self.spot)
        projekt.read(self.spot)
        return projekt.fileName()

    def load(self):
        """
        Funkcja ładuje nową warstwe z ścieżki podaje i szuka pliku 'Lista9_warstwa.shp'
        :return: zwraca vector
        """
        vector = iface.addVectorLayer(os.path.join(self.filepath, 'Lista9_warstwa.shp'), "ptaki", "ogr")
        return vector

    def count(self):
        """
        Funkcja ma na celu obliczenie prawdopodobieństwa wystąpenia w danej lokalizacji. Do obliczeń użyto kolumny NUMPOINTS"
        iteracja po wszystkich obiektach
        """
        warstwa = self.load()
        #        warstwa = iface.activeLayer()
        pr = warstwa.dataProvider()

        sumaP = sum(filter(None, [f['NUMPOINTS'] for f in qgis.utils.iface.activeLayer().getFeatures()]))
        print('.\n..\n...\n zaktualizowano')

        pr.addAttributes([QgsField('P', QVariant.Double)])
        warstwa.updateFields()
        #        próbba printu sumy
        with edit(warstwa):
            for obiekt in warstwa.getFeatures():
                obiekt.setAttribute(obiekt.fieldNameIndex('P'), obiekt['NUMPOINTS'] / sumaP)
                warstwa.updateFeature(obiekt)
            print('zaktualizowano')

        check = sum(filter(None, [i['P'] for i in warstwa.getFeatures()]))

        if round(check) == 1:
            print('Suma prawdopodobieńst równa jedności, suma prawdopodobieństw wynosi {}'.format(round(check,3)))


new = Bird(name='Nowy', spot='C:/Users/misie/Desktop/', filepath='C:/Users/misie/Downloads/')