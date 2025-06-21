import requests
import tempfile
import os

from urllib.parse import urlparse
from pydub import AudioSegment

def download_file_as_temp(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        file_name = get_file_name(file_url)
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file_name)

        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(response.content)
        
    return temp_file_path

def get_file_name(file_url):
    parsed_url = urlparse(file_url)
    file_name = os.path.basename(parsed_url.path)

    return file_name

def ogg_to_mp3(ogg_file_path):
    ogg_file_name = get_file_name(ogg_file_path)
    print('[INFO] ogg file name: ', ogg_file_name)
    mp3_file_name = ''.join(ogg_file_name.split('.')[:-1]) + '.mp3'
    print('[INFO] mp3 file name: ', mp3_file_name)
    audio_segment = AudioSegment.from_ogg(ogg_file_path)

    temp_dir = tempfile.gettempdir()
    mp3_file_path = os.path.join(temp_dir, mp3_file_name)

    audio_segment.export(mp3_file_path)

    return mp3_file_path
