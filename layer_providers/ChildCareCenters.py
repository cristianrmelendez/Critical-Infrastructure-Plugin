import requests
from PyQt5.QtCore import QVariant
from qgis.core import *


def get_layer(state):
    response = requests.get(
        "https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/ChildCareCenter1/FeatureServer/0/query?where=STATE%20%3D%20'" + state + "'&outFields=*&outSR=4326&f=json").json()
    child_care_centers = response["features"]

    layer = QgsVectorLayer('Point?crs=epsg:4326', 'ChildCareCenters-' + state, 'memory')
    crs = layer.crs()
    crs.createFromId(4326)
    layer.setCrs(crs)

    child_care_centers_fields = QgsFields()
    # More can be added
    child_care_centers_fields.append(QgsField('Id', QVariant.Int))
    child_care_centers_fields.append(QgsField('Name', QVariant.String))
    child_care_centers_fields.append(QgsField('City', QVariant.String))
    child_care_centers_fields.append(QgsField('County', QVariant.String))
    child_care_centers_fields.append(QgsField('Address', QVariant.String))
    child_care_centers_fields.append(QgsField('Population', QVariant.Int))
    child_care_centers_fields.append(QgsField('Website', QVariant.String))
    child_care_centers_fields.append(QgsField('Telephone', QVariant.String))

    prov = layer.dataProvider()
    prov.addAttributes(child_care_centers_fields)

    layer.startEditing()

    for e in child_care_centers:
        # Setting the feature for each child care centers
        feat = QgsFeature()

        # Adding the lat/lon to the point
        point = QgsPointXY(e['geometry']['x'], e['geometry']['y'])
        feat.setGeometry(QgsGeometry.fromPointXY(point))

        # Adding the attributes of the child care centers to the point
        feat.setAttributes([e['attributes']['ID'], e['attributes']['NAME'], e['attributes']['CITY'],
                            e['attributes']['COUNTY'], e['attributes']['ADDRESS'], e['attributes']['POPULATION'],
                            e['attributes']['WEBSITE'], e['attributes']['TELEPHONE']])

        # Adding the feature to the layer
        prov.addFeatures([feat])

    layer.updateExtents()
    layer.commitChanges()

    return layer
