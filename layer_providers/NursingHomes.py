from PyQt5.QtCore import QVariant
from qgis.core import *
import csv
import requests


def get_layer(state):
    response = requests.get(
        "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/NursingHomes2024/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    nursing_homes = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'NursingHomes-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    nursing_homes_fields = QgsFields()
    # More can be added
    nursing_homes_fields.append(QgsField('Id', QVariant.String))
    nursing_homes_fields.append(QgsField('Name', QVariant.String))
    nursing_homes_fields.append(QgsField('Address', QVariant.String))
    nursing_homes_fields.append(QgsField('City', QVariant.String))
    nursing_homes_fields.append(QgsField('Type', QVariant.String))
    nursing_homes_fields.append(QgsField('Status', QVariant.String))
    nursing_homes_fields.append(QgsField('Population', QVariant.Double))
    nursing_homes_fields.append(QgsField('NAICS_Desc', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(nursing_homes_fields)

    layer.startEditing()

    for e in nursing_homes:
        # Setting the feature for each Nursing Home
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the nursing homes to the point
        feat.setAttributes([e['attributes']['ID'], e['attributes']['NAME'], e['attributes']['ADDRESS'],
                            e['attributes']['CITY'], e['attributes']['TYPE'], e['attributes']['STATUS'], 
                            e['attributes']['POPULATION'], e['attributes']['NAICS_DESC']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer
