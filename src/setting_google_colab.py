import requests
import os
import os.path as pth
from multiprocessing import Pool
from functools import partial
from tqdm.notebook import tqdm
import zipfile


##### Goggle Colab Configures ######
def download_file_from_google_drive(id_, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params = { 'id' : id_ }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id_, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
        
    basename = response.headers['Content-Disposition'].split(';')[1].split('filename=')[1].replace('\"', '')
    full_dst_filenname = pth.join(destination, basename)
    save_response_content(response, full_dst_filenname)
    return full_dst_filenname

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

file_id_list = [
    '************key***************',
]

destination = 'data' ### YOUR_DOWNLOAD_PATH
os.makedirs(destination, exist_ok=True)

filename_list = []

# ### Use single process
# for file_id in file_id_list:
#     filename = download_file_from_google_drive(id_=file_id, destination=destination)
#     print('{} is done!'.format(filename))
#     filename_list.append(filename)

### If you want to download more faster
download_func = partial(download_file_from_google_drive, destination=destination)
with Pool(4) as pool:
    for i, filename in tqdm(enumerate(pool.imap_unordered(download_func, file_id_list)), total=len(file_id_list)):
        print('{} is done!'.format(filename))
        filename_list.append(filename)

zip_filename_list = [filename for filename in filename_list if filename.endswith('.zip')]
    
for zip_filename in tqdm(zip_filename_list):
    with zipfile.ZipFile(zip_filename) as target_zip:
        dest_path = pth.splitext(zip_filename)[0]
        os.makedirs(dest_path, exist_ok=True)
        target_zip.extractall(dest_path)
        print('{} is done!'.format(dest_path))

os.listdir('data/')
os.listdir('data/KT_data_20200717')
os.listdir('data/KT_data_20200717/COVID_19')
