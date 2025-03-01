import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get(
            "https://carto.nationalmap.gov/arcgis/rest/services/structures/MapServer/51/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    fire_stations = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'FireStations-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    fire_stations_fields = QgsFields()
    fire_stations_fields.append(QgsField('OBJECTID', QVariant.String))
    fire_stations_fields.append(QgsField('NAME', QVariant.String))
    fire_stations_fields.append(QgsField('ADDRESS', QVariant.String))
    fire_stations_fields.append(QgsField('CITY', QVariant.String))
    fire_stations_fields.append(QgsField('STATE', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(fire_stations_fields)

    layer.startEditing()

    for e in fire_stations:
        feat = QgsFeature()
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))
        feat.setAttributes([
            e['attributes']['OBJECTID'],
            e['attributes']['NAME'],
            e['attributes']['ADDRESS'],
            e['attributes']['CITY'],
            e['attributes']['STATE']
        ])
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

