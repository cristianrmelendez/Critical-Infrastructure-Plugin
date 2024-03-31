import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get(
            "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Hospital/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    hospitals = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Hospitals-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    hospitals_fields = QgsFields()
    # More can be added
    hospitals_fields.append(QgsField('Id', QVariant.Int))
    hospitals_fields.append(QgsField('Name', QVariant.String))
    hospitals_fields.append(QgsField('City', QVariant.String))
    hospitals_fields.append(QgsField('County', QVariant.String))
    hospitals_fields.append(QgsField('Address', QVariant.String))
    hospitals_fields.append(QgsField('Owner', QVariant.String))
    hospitals_fields.append(QgsField('Beds', QVariant.Int))
    hospitals_fields.append(QgsField('Trauma', QVariant.String))
    hospitals_fields.append(QgsField('Helipad', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(hospitals_fields)

    layer.startEditing()

    for e in hospitals:
        # Setting the feature for each Hospital
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the hospital to the point
        feat.setAttributes([e['attributes']['OBJECTID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['COUNTY'], e['attributes']['ADDRESS'], e['attributes']['OWNER'],
                            e['attributes']['BEDS'], e['attributes']['TRAUMA'], e['attributes']['HELIPAD']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

