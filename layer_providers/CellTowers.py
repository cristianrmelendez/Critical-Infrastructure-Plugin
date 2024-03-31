import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get(
            "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Cellular_Towers_New/FeatureServer/0/query?where=LocState%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    cell_towers = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'CellTowers-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    cell_towers_fields = QgsFields()
    # More can be added
    cell_towers_fields.append(QgsField('Id', QVariant.Int))
    cell_towers_fields.append(QgsField('Name', QVariant.String))
    cell_towers_fields.append(QgsField('City', QVariant.String))
    cell_towers_fields.append(QgsField('County', QVariant.String))
    cell_towers_fields.append(QgsField('Address', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(cell_towers_fields)

    layer.startEditing()

    for e in cell_towers:
        # Setting the feature for each Cell tower
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the cell tower to the point
        feat.setAttributes(
            [e['attributes']['FID'], "Cell Tower - " + e['attributes']['Licensee'], e['attributes']['LocCity'],
             e['attributes']['LocCounty'], e['attributes']['LocAdd']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

