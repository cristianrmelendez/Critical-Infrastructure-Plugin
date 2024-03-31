import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get("https://services.arcgis.com/xOi1kZaI0eWDREZv/ArcGIS/rest/services/Aviation_Facilities"
                            "/FeatureServer/0/query?where=STATE_CODE%20%3D%20'" + state +
                            "'&outFields=*&outSR=4326&f=json").json()

    airports = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'AircraftLandingFacilities-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    airports_fields = QgsFields()
    # More can be added
    airports_fields.append(QgsField('Id', QVariant.Int))
    airports_fields.append(QgsField('Name', QVariant.String))
    airports_fields.append(QgsField('Type', QVariant.String))
    airports_fields.append(QgsField('City', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(airports_fields)

    layer.startEditing()

    for e in airports:
        # Setting the feature for each airport
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the airports to the point
        feat.setAttributes(
            [e['attributes']['OBJECTID'], e['attributes']['ARPT_NAME'], e['attributes']['SITE_TYPE_CODE'],
             e['attributes']['CITY']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer
# ***************************************************************************/
