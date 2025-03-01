import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get(
            "https://services7.arcgis.com/n1YM8pTrFmm7L4hs/ArcGIS/rest/services/Docks/FeatureServer/0/query?where=STATE_POST%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    docks = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Docks-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    docks_fields = QgsFields()
    docks_fields.append(QgsField('FID', QVariant.Int))
    docks_fields.append(QgsField('NAV_UNIT_NAME', QVariant.String))
    docks_fields.append(QgsField('CITY_OR_TOWN', QVariant.String))
    docks_fields.append(QgsField('STREET_ADD', QVariant.String))
    docks_fields.append(QgsField('STATE_POSTAL_CODE', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(docks_fields)

    layer.startEditing()

    for e in docks:
        feat = QgsFeature()
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))
        feat.setAttributes([
            e['attributes']['FID'],
            e['attributes']['NAV_UNIT_N'],
            e['attributes']['CITY_OR_TO'],
            e['attributes']['STREET_ADD'],
            e['attributes']['STATE_POST']
        ])
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

