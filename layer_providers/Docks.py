import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get(
            "https://services7.arcgis.com/n1YM8pTrFmm7L4hs/arcgis/rest/services/Docks/FeatureServer/0/query?where=STATE_POSTAL_CODE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    docks = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Docks-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    docks_fields = QgsFields()
    # More can be added
    docks_fields.append(QgsField('Id', QVariant.Int))
    docks_fields.append(QgsField('Name', QVariant.String))
    docks_fields.append(QgsField('County', QVariant.String))
    docks_fields.append(QgsField('City', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(docks_fields)

    layer.startEditing()

    for e in docks:
        # Setting the feature for each Docks
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the dock to the point
        feat.setAttributes([e['attributes']['OBJECTID'], e['attributes']['NAV_UNIT_NAME'], e['attributes']['COUNTY_NAME'],
                            e['attributes']['CITY_OR_TOWN']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

