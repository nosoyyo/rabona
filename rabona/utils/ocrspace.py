import json
import logging
import requests

from utils.config import ocr_space_apikey

logging.basicConfig(
    filename='log/ocr.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def ocr_space_file(filename: str,
                   overlay: bool=False,
                   api_key: str=ocr_space_apikey,
                   language: str='eng') -> dict:
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        'apikey': api_key,
        'language': language,
    }

    logging.info('going to make the ocr.space request.')

    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    j = r.content.decode()
    j = json.loads(j)
    logging.info(
        'got the ocr.space response {}\ngoing to RabonaParser. j type is {}'.format(j, type(j)))
    return j


def ocr_space_url(url, overlay=False, api_key=ocr_space_apikey, language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()
