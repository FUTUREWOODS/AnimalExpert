#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""IBM Watson Developer Cloud ÇÃ Visual RecognitionÇ≈ï®ëÃîFéØÇçsÇ§
"""
import os
import sys
import json
import cv2
import requests
from pit import Pit
password="722249c5-1201-41c8-bb55-67be4f1ffeec"
username="p83q2pSXrWdK"


url = 'https://gateway.watsonplatform.net/visual-recognition-beta/api/v2/classify?version=2015-12-02'

filepath = "temp.jpg"  # path to image file
cap = cv2.VideoCapture(0)
ret, lena = cap.read()
while 1:
  ret, lena = cap.read()
  kye=cv2.waitKey(1)
  if  kye == ord('a'):
        break
  cv2.imshow("flame",lena)
cv2.imwrite(filepath , lena)


filename = os.path.basename(filepath)

res = requests.post(
    url, auth=(password,username),
    files={
        'imgFile': (filename, open(filepath, 'rb')),
        }
    )
if res.status_code == requests.codes.ok:
    data = json.loads(res.text)
    for img in data['images']:
        print('{}'.format(img['image']))
        for label in img['scores']:
            print('    {:30}: {}'.format(label['name'], label['score']))

else:  # error
    print('stauts_code: {} (reason: {})'.format(res.status_code, res.reason))
    sys.exit(1)
    
while 1:
  cv2.imshow("flame",lena)
  kye=cv2.waitKey(1)
  if  kye == ord('a'):
        break