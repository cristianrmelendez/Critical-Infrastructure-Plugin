import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    # Get Weather radar stations
    response = requests.get(
            "https://coast.noaa.gov/arcgis/rest/services/MarineCadastre/PhysicalOceanographicAndMarineHabitat/MapServer/3/query?where=1%3D1&outFields=*&outSR=4326&f=json").json()
    weather_radar_stations = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'WeatherRadarStations', 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    weather_radar_stations_fields = QgsFields()
    # More can be added
    weather_radar_stations_fields.append(QgsField('Id', QVariant.Int))
    weather_radar_stations_fields.append(QgsField('Name', QVariant.String))
    weather_radar_stations_fields.append(QgsField('Radar Type', QVariant.String))
    weather_radar_stations_fields.append(QgsField('Antenna Elevation', QVariant.String))


    prov = layer.dataProvider()
    prov.addAttributes(weather_radar_stations_fields)

    layer.startEditing()

    for e in weather_radar_stations:
        # Setting the feature for each Cell tower
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the cell tower to the point
        feat.setAttributes(
            [e['attributes']['OBJECTID'], e['attributes']['siteName'], e['attributes']['radarType'],
             e['attributes']['antennaElevation']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer

