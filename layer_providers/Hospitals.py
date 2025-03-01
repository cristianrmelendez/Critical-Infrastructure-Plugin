import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get(
            "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Hospitals_gdb/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    hospitals = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Hospitals-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    hospitals_fields = QgsFields()
    hospitals_fields.append(QgsField('ID', QVariant.String))
    hospitals_fields.append(QgsField('NAME', QVariant.String))
    hospitals_fields.append(QgsField('ADDRESS', QVariant.String))
    hospitals_fields.append(QgsField('CITY', QVariant.String))
    hospitals_fields.append(QgsField('STATE', QVariant.String))
    hospitals_fields.append(QgsField('BEDS', QVariant.Int))
    hospitals_fields.append(QgsField('TRAUMA', QVariant.String))
    hospitals_fields.append(QgsField('HELIPAD', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(hospitals_fields)

    layer.startEditing()

    for e in hospitals:
        feat = QgsFeature()
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))
        feat.setAttributes([
            e['attributes']['ID'],
            e['attributes']['NAME'],
            e['attributes']['ADDRESS'],
            e['attributes']['CITY'],
            e['attributes']['STATE'],
            e['attributes']['BEDS'],
            e['attributes']['TRAUMA'],
            e['attributes']['HELIPAD']
        ])
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

