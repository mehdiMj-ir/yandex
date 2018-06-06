#-*- coding: utf-8 -*-

import locale
import requests 

class Translater(object):

    def __init__(self, key = None, text = None, 
                 from_lang = None, to_lang = None, 
                 hint = [], ui = None):
        self.valid_lang = ['az','sq','am','en','ar','hy','af','eu','ba','be','bn','my',
                          'bg','bs','cy','hu','vi','ht','gl','nl','mrj','el','ka','gu',
                           'da','he','yi','id','ga','it','is','es','kk','kn','ca','ky',
                           'zh','ko','xh','km','lo','la','lv','lt','lb','mg','ms','ml',
                           'mt','mk','mi','mr','mhr','mn','de','ne','no','pa','pap','fa',
                           'pl','pt','ro','ru','ceb','sr','si','sk','sl','sw','su','tg',
                           'th','tl','ta','tt','te','tr','udm','uz','uk','ur','fi','fr',
                           'hi','hr','cs','sv','gd','et','eo','jv','ja']

        self.valid_format = ['plain', 'html' ]
        self.valid_default_ui = ['ru','en','tr']
        
        self.default_ui = locale.getlocale()[0].split('_')[0]

        if not self.default_ui in self.valid_lang:
            self.default_ui = 'en'

        if not ui: self.ui = self.default_ui
        self.hint = hint
        self.base_url = 'https://translate.yandex.net/api/v1.5/tr.json/'
        self.key = key
        self.text = text
        self.from_lang = from_lang
        self.to_lang = to_lang

    def set_key(self, key):
        if key: self.key = key

    def set_text(self, text):
        if text: self.text = text

    def set_default_ui(self, lang):
        if lang and lang in self.valid_lang: self.ui = lang
        else: self.default_ui = self.default_ui

    def set_ui(self, lang):
        if lang and lang in self.valid_lang: self.ui = lang
        else: self.ui = self.default_ui

    def set_hint(self, *langs):
        for lang in langs:
            if lang in self.valid_lang:
                self.hint.append(lang)

    def set_from_lang(self, lang):
        if lang and lang in self.valid_lang: self.from_lang = lang

    def set_to_lang(self, lang):
        if lang and lang in self.valid_lang: self.to_lang = lang

    def translate(self):
        if not self.key:
            return "Please set Api key"
        if not self.text:
            return "Please set Text"
        if not self.from_lang:
            return "Please set source lang"
        if not self.to_lang:
            return "Please set destination lang"

        data = {'key' : self.key, 'text' : self.text, 
                'lang' : '{}-{}'.format(self.from_lang,self.to_lang)}
        query = 'translate?'
        url = self.base_url + query 
        response = requests.get(url, data)
        if response.status_code == 401 : return 'Invalid API key'
        if response.status_code == 402 : return 'Blocked API key'
        if response.status_code == 402 : return 'Exceeded the daily limit on the amount of translated text'
        if response.status_code == 413 : return "Exceeded the maximum text size"
        if response.status_code == 422 : return "The text cannot be translated"
        if response.status_code == 501 : return "The specified translation direction is not supported"
        if not response.status_code == 200: return "Failed to translate text! {}".format(response.reason)
        result = response.json()
        return result['text'][0]

    def detect_lang(self):
        if not self.key:
            "Please set Api key"

        if not self.text:
            return "Please set a text"

        data = {'key' : self.key, 'text' : self.text, 'hint' : ','.join(self.hint)}
        query = 'detect?'
        url = self.base_url + query
        response = requests.get(url, data)
        if response.status_code == 401: return "Invalid API key"
        if response.status_code == 402: return "Blocked API key"
        if response.status_code == 404: return "Exceeded the daily limit on the amount of translated text"
        if not response.status_code == 200:
            return "Failed to detect the language! (response code {}".format(response.reason)
        result = response.json()
        return result['lang']

    def get_langs(self):
        if not self.key:
            return "please set Api key"

        data = {'key' : self.key, 'ui' : self.ui}
        query = 'getLangs?'
        url = self.base_url + query
        response = requests.get(url, data)
        if response.status_code == 401: return "Invalid API key"
        if response.status_code == 402: return "Blocked API key"
        if not response.status_code == 200:
            return "Failed to get list of supported languages! (response code {})".format(response.reason)
        result = response.json()
        return result['dirs']

