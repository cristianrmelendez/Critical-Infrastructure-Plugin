import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    # Universities
    response = requests.get(
            "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Colleges_and_Universities/FeatureServer/0/query?where=STATE%20like%20'%25" + state + "%25'&outFields=*&outSR=4326&f=json").json()
    universities = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'Universities-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    university_fields = QgsFields()
    # More can be added
    university_fields.append(QgsField('Id', QVariant.Int))
    university_fields.append(QgsField('Name', QVariant.String))
    university_fields.append(QgsField('City', QVariant.String))
    university_fields.append(QgsField('Address', QVariant.String))
    university_fields.append(QgsField('Population', QVariant.Int))
    university_fields.append(QgsField('Website', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(university_fields)

    layer.startEditing()

    for e in universities:
        # Setting the feature for each University
        feat = QgsFeature()
        # Append field values

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the university to the point
        feat.setAttributes([e['attributes']['OBJECTID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['ADDRESS'], e['attributes']['POPULATION'], e['attributes']['WEBSITE']])

        # Adding the feature to the layer
        prov.addFeatures([feat])


    layer.updateExtents()
    layer.commitChanges()

    return layer


