import requests
from PyQt5.QtCore import QVariant
from qgis.core import *

def get_layer(state):
    # Schools
    response = requests.get(
        "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Public_Schools/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    schools = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Schools-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    schools_fields = QgsFields()
    # More can be added
    schools_fields.append(QgsField('Id', QVariant.Int))
    schools_fields.append(QgsField('Name', QVariant.String))
    schools_fields.append(QgsField('City', QVariant.String))
    schools_fields.append(QgsField('County', QVariant.String))
    schools_fields.append(QgsField('Address', QVariant.String))
    schools_fields.append(QgsField('Population', QVariant.Int))
    schools_fields.append(QgsField('Website', QVariant.String))
    schools_fields.append(QgsField('Telephone', QVariant.String))
    schools_fields.append(QgsField('Starting grade', QVariant.String))
    schools_fields.append(QgsField('End grade', QVariant.String))


    prov = layer.dataProvider()
    prov.addAttributes(schools_fields)

    layer.startEditing()

    for e in schools:
        # Setting the feature for each Hospital
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the Schools to the point
        feat.setAttributes([e['attributes']['OBJECTID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['COUNTY'], e['attributes']['ADDRESS'], e['attributes']['POPULATION'],
                            e['attributes']['WEBSITE'], e['attributes']['TELEPHONE'], e['attributes']['ST_GRADE'],
                            e['attributes']['END_GRADE']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer
