import requests
from PyQt5.QtCore import QVariant
from qgis.core import *

def get_layer(state):
    response = requests.get(
        "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Courthouses_gdb/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    courthouses = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Courthouses-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    courthouses_fields = QgsFields()
    # More can be added
    courthouses_fields.append(QgsField('Id', QVariant.Int))
    courthouses_fields.append(QgsField('Name', QVariant.String))
    courthouses_fields.append(QgsField('City', QVariant.String))
    courthouses_fields.append(QgsField('Address', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(courthouses_fields)

    layer.startEditing()

    for e in courthouses:
        # Setting the feature for each courthouse
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the courthouses to the point
        feat.setAttributes([e['attributes']['OBJECTID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['ADDRESS']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    return layer

