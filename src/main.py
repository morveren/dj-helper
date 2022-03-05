import os

import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.aiff import AIFF
from mutagen.wave import WAVE
from tinytag import TinyTag
from pydub import AudioSegment

from shutil import move,move


from tqdm import tqdm

from functools import partial

from absl import app

import time

EXTS = {".flac":FLAC,".mp3":partial(MP3,ID3=EasyID3),".wav":TinyTag.get,".aiff":AIFF}



def get_new_path(fpath,processor,foldername = "soulseek",ext=None,fields = ["artist","album","title"]):
    """Generate new path for a file to move to

    Parameters
    ----------
    fpath : str
        Current file path
    processor : mutagen object
        processor for extracting information from the file
    foldername : str, optional
        name of folder within /music_store/holding, by default "soulseek"
    ext : string, optional
        file extension, by default None

    Returns
    -------
    str
        New filepath
    """
    if ext is None:
        ext = os.path.splitext(fpath)[-1]
    # fields = ["artist","album","title"]
    try:
        audio = processor(fpath)
    # except mutagen.flac.error as e:
    #     return None
    except Exception as e:
        print(f"Unable to process path {fpath}")
        return None
        
    song_attrs = {}
    for field in fields:
        field_val = f"Unknown {field}"
        if not isinstance(audio,dict):
            try:
                val_poss = getattr(audio,field)
                if val_poss is not None:
                    field_val = getattr(audio,field)
            except:
                pass
        elif field in audio:
            field_vals = audio[field]
            if len(field_vals)>0:
                field_val = field_vals[0]
        song_attrs[field] = field_val
    if song_attrs["title"] == f"Unknown title":
        song_attrs["title"] = os.path.splitext(os.path.split(fpath)[-1])[0]
    return os.path.join("/music_store/holding",foldername.strip("/"),song_attrs["artist"],song_attrs["album"],song_attrs["title"]+ext)


def import_files(dir):
        # get files
        print("Getting files...")
        fpaths = {ext:[] for ext in EXTS}
        # get filepaths
        for root, dirs, files in os.walk(dir):
            for filename in files:
                ext = None
                for ext in EXTS:
                    if filename.endswith(ext):
                        fpaths[ext].append(os.path.join(root,filename))
                        break
        print("Found files with the following extensions:\n","\n".join([ext + ":" + str(len(fpaths[ext])) + '\n' for ext in fpaths]))


        # print("found flac files:",",".join(fpaths[".flac"]]))
                        
        print("Creating mappings to new destinations...")
        fpath_mappings = {}
        for ext in fpaths:
            for fpath in tqdm(fpaths[ext]):
                fpath_mappings[fpath] = get_new_path(fpath,EXTS[ext],foldername=dir)
        print("Moving files over...")
        counter = 0
        for fpath in tqdm(fpath_mappings):
            dest = fpath_mappings[fpath]
            if dest is not None:
                # check haven't already imported
                if not os.path.exists(dest):
                    # removed as aiff not importing right now
                    if fpath.endswith(".flac"):
                        sound = AudioSegment.from_file(fpath)
                        fileroot = os.path.splitext(fpath)[0]
                        fpath_new = fileroot + ".aiff"
                        sound.export(fpath_new, format="aiff")
                        os.remove(fpath) # delete old file
                        fpath = fpath_new # update to new path
                        dest = os.path.splitext(dest)[0] + ".aiff" # update destination
                    folder,filename = os.path.split(dest)
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    move(fpath,dest)
                    counter +=1
                else:
                    print(f"Not importing {dest} as it already exists")
                    # remove
                    os.remove(fpath)
        
        print("File import complete.",f"Imported {counter} out of {len(fpath_mappings)} files")

def cleanup_empty_folders(path):
    print("cleaning")
    for root, dirs, files in os.walk(path,topdown=False):
        print(root,dirs,files)
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))

def main(_):
    # run infinite loop
    while True:
        print("Importing soulseek")
        import_files("/soulseek")
        print("Importing bandcamp")
        import_files("/bandcamp")
        # print("Cleaning up folders")
        # cleanup_empty_folders("/soulseek")
        time.sleep(5)

if __name__ == "__main__":
    app.run(main)
