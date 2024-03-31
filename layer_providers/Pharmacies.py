from PyQt5.QtCore import QVariant
from qgis.core import *
import csv
import requests


def get_layer(state):
    response = requests.get(
        "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Pharmacies/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    pharmacies = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Pharmacies-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    pharmacies_fields = QgsFields()
    # More can be added
    pharmacies_fields.append(QgsField('Id', QVariant.Int))
    pharmacies_fields.append(QgsField('Name', QVariant.String))
    pharmacies_fields.append(QgsField('City', QVariant.String))
    pharmacies_fields.append(QgsField('Address', QVariant.String))
    pharmacies_fields.append(QgsField('Website', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(pharmacies_fields)

    layer.startEditing()

    for e in pharmacies:
        # Setting the feature for each Hospital
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the government buildings to the point
        feat.setAttributes([e['attributes']['ID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['ADDRESS'], e['attributes']['WEBSITE']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer
