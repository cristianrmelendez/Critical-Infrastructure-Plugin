import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    # Fire Stations
    response = requests.get(
            "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Major_State_Government_Buildings/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    government_buildings = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'MajorStateGovernmentBuildings-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    government_buildings_fields = QgsFields()
    # More can be added
    government_buildings_fields.append(QgsField('Id', QVariant.Int))
    government_buildings_fields.append(QgsField('Name', QVariant.String))
    government_buildings_fields.append(QgsField('City', QVariant.String))
    government_buildings_fields.append(QgsField('County', QVariant.String))
    government_buildings_fields.append(QgsField('Address', QVariant.String))
    government_buildings_fields.append(QgsField('Directions', QVariant.String))
    government_buildings_fields.append(QgsField('Description', QVariant.String))
    government_buildings_fields.append(QgsField('Agencies', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(government_buildings_fields)

    layer.startEditing()

    for e in government_buildings:
        # Setting the feature for each Hospital
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the government buildings to the point
        feat.setAttributes([e['attributes']['OBJECTID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['COUNTY'], e['attributes']['ADDRESS'], e['attributes']['DIRECTIONS'],
                            e['attributes']['NAICSDESCR'], e['attributes']['AGENCIES']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

