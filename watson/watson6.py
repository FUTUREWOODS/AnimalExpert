# -*- coding: utf-8 -*-

import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import random
import json
import sys
import requests
from watsonC import Watson
from PepperStream import PepperModuleClass
import threading
import time
from naoqi import (ALProxy, ALBroker, ALModule)

PEPPER_IP = "192.168.1.6"

