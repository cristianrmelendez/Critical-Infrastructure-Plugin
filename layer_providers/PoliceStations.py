import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    # Police Stations
    response = requests.get(
            "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Local_Law_Enforcement_Locations/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    police_stations = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'PoliceStations-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    police_stations_fields = QgsFields()
    # More can be added
    police_stations_fields.append(QgsField('Id', QVariant.Int))
    police_stations_fields.append(QgsField('Name', QVariant.String))
    police_stations_fields.append(QgsField('City', QVariant.String))
    police_stations_fields.append(QgsField('County', QVariant.String))
    police_stations_fields.append(QgsField('Address', QVariant.String))
    police_stations_fields.append(QgsField('Telephone', QVariant.String))
    police_stations_fields.append(QgsField('Type', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(police_stations_fields)

    layer.startEditing()

    for e in police_stations:
        # Setting the feature for each Hospital
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the hospital to the point
        feat.setAttributes([e['attributes']['OBJECTID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['COUNTY'], e['attributes']['ADDRESS'], e['attributes']['TELEPHONE'],
                            e['attributes']['TYPE']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

