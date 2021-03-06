# -*- coding: utf-8 -*-

import json
import wave
import requests
import re
from watsonStreamX import watsonStream


class Watson:

    VERSION = "v1"

    def __init__(self, username, password, url):
        self.auth = (username, password)  # basic
        self.version = self.VERSION
        m = re.match(r'(.+?)://(.+?)/(.+?)/api', url)
        if m is None:
            raise Exception('不正なURLが渡されました')
        self.domain = m.group(2)
        self.service = m.group(3)

    def get_token(self):
        url = self._get_url(service="authorization", action="token") + "?url=" + self._get_url_short()
        return requests.get(url, auth=self.auth)


    def recognize_stream(self, token, start_params={}):
        # 注意: query parameterの最初はwatson-tokenでないといけない
        url = self._get_url(scheme="wss", action="recognize") \
              + "?watson-token={token}&model={model}".format(token=token, model="ja-JP_BroadbandModel")
        stream = watsonStream(url, start_params=start_params)
        return stream

    def tag_recognize(self, image_path):
        url = self._get_url(action="tag/recognize")
        headers = {"Content_Type": "multipart/form-data"}
        files = {"img_File": open(image_path, "rb")}
        return requests.post(url, files=files, headers=headers, auth=self.auth)

    def get_tag_labels(self):
        url = self._get_url(action="tag/labels")
        return requests.get(url, auth=self.auth)

    def _get_url_short(self, scheme="https", service=None):
        if service is None:
            service = self.service
        return "{scheme}://{domain}/{service}/api".format(scheme=scheme, domain=self.domain, service=service)

    def _get_url(self, scheme="https", service=None, action=None):
        if service is None:
            service = self.service
        return "{scheme}://{domain}/{service}/api/{version}/{action}" \
            .format(scheme=scheme, domain=self.domain, service=service, version=self.version, action=action)

    def _get_wave_type_str(self, path):
        wave = self._get_wave_info(path)
        return ";".join(["audio/wav", "rate=" + str(wave["rate"]), "channels=" + str(wave["channels"])])

    def _get_wave_info(self, path):
        f = wave.open(path, "rb")
        info = {"channels": f.getnchannels(), "rate": f.getframerate()}
        f.close()
        return info
