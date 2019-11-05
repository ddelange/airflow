# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from google.cloud.translate_v2 import Client

from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook


class CloudTranslateHook(GoogleCloudBaseHook):
    """
    Hook for Google Cloud translate APIs.
    """

    _client = None

    def __init__(self, gcp_conn_id='google_cloud_default'):
        super(CloudTranslateHook, self).__init__(gcp_conn_id)

    def get_conn(self):
        """
        Retrieves connection to Cloud Translate

        :return: Google Cloud Translate client object.
        :rtype: google.cloud.translate_v2.Client
        """
        if not self._client:
            self._client = Client(credentials=self._get_credentials())
        return self._client

    @GoogleCloudBaseHook.quota_retry()
    def translate(
        self, values, target_language, format_=None, source_language=None, model=None
    ):
        """Translate a string or list of strings.

        See https://cloud.google.com/translate/docs/translating-text

        :type values: str or list
        :param values: String or list of strings to translate.

        :type target_language: str
        :param target_language: The language to translate results into. This
                                is required by the API and defaults to
                                the target language of the current instance.

        :type format_: str
        :param format_: (Optional) One of ``text`` or ``html``, to specify
                        if the input text is plain text or HTML.

        :type source_language: str or None
        :param source_language: (Optional) The language of the text to
                                be translated.

        :type model: str or None
        :param model: (Optional) The model used to translate the text, such
                      as ``'base'`` or ``'nmt'``.

        :rtype: str or list
        :returns: A list of dictionaries for each queried value. Each
                  dictionary typically contains three keys (though not
                  all will be present in all cases)

                  * ``detectedSourceLanguage``: The detected language (as an
                    ISO 639-1 language code) of the text.
                  * ``translatedText``: The translation of the text into the
                    target language.
                  * ``input``: The corresponding input value.
                  * ``model``: The model used to translate the text.

                  If only a single value is passed, then only a single
                  dictionary will be returned.
        :raises: :class:`~exceptions.ValueError` if the number of
                 values and translations differ.
        """
        client = self.get_conn()

        return client.translate(
            values=values,
            target_language=target_language,
            format_=format_,
            source_language=source_language,
            model=model,
        )
