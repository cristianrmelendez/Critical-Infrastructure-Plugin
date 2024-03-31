import os

from .layer_providers import AircraftLandingFacilities
from .layer_providers import CellTowers
from .layer_providers import ChildCareCenters
from .layer_providers import Courthouses
from .layer_providers import DialysisCenters
from .layer_providers import Docks
from .layer_providers import FireStations
from .layer_providers import Hospitals
from .layer_providers import MajorStateGovernmentBuildings
from .layer_providers import Pharmacies
from .layer_providers import PoliceStations
from .layer_providers import Schools
from .layer_providers import Universities
from .layer_providers import WeatherRadarStations


def get_layers(layer_dictionary, state):

    layers = []
    for filename in list(layer_dictionary.keys()):

        if layer_dictionary[filename]:
            command = filename + ".get_layer('" + state + "')"
            layer = eval(command)
            layers.append(layer)

        else:
            pass

    return layers
