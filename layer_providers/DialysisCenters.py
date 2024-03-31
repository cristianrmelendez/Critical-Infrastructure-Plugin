from PyQt5.QtCore import QVariant
from qgis.core import *
import csv
import requests


def get_layer(state):
    response = requests.get(
        "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Dialysis_Centers/FeatureServer/0/query?where=State%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    dialysis_centers = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'DialysisCenters-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    dialysis_center_fields = QgsFields()
    # More can be added
    dialysis_center_fields.append(QgsField('Id', QVariant.Int))
    dialysis_center_fields.append(QgsField('Name', QVariant.String))
    dialysis_center_fields.append(QgsField('City', QVariant.String))
    dialysis_center_fields.append(QgsField('Address', QVariant.String))
    dialysis_center_fields.append(QgsField('Status', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(dialysis_center_fields)

    layer.startEditing()
    for e in dialysis_centers:
        # Setting the feature for each dialysis centers
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the dialysis centers to the point
        feat.setAttributes([e['attributes']['FID'], e['attributes']['Name'], e['attributes']['City'],
                            e['attributes']['Address'], e['attributes']['Status']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer
