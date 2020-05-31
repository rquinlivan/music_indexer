from os import walk, path
from typing import Optional, List, Generator

import click
import eyed3

from dataclasses import dataclass

from mutagen.flac import FLAC, StreamInfo

import sqlite3

file_extensions = ['mp3', 'flac']


@dataclass
class MusicFile:
  title: str
  artist: str
  album: str
  album_artist: str
  track_number: int
  full_path: str
  length: int


def file_extension(filename):
  return filename.split('.')[-1]


def mp3_handler(file_path) -> MusicFile:
  audiofile = eyed3.load(file_path)
  return MusicFile(
    title = audiofile.tag.title,
    artist = audiofile.tag.artist,
    album = audiofile.tag.album,
    album_artist = audiofile.tag.album_artist,
    track_number = audiofile.tag.track_num,
    full_path = file_path,
    length = 0
  )


def flac_handler(file_path) -> MusicFile:
  audiofile = FLAC(file_path)
  stream_info: StreamInfo = audiofile.info
  metadata = {k: v for (k, v) in audiofile.metadata_blocks[2]}
  return MusicFile(
    title = metadata['TITLE'],
    artist = metadata['ARTIST'],
    album = metadata['ALBUM'],
    album_artist = metadata['ALBUMARTIST'],
    track_number = int(metadata['TRACKNUMBER']),
    full_path = file_path,
    length = 0
  )


handlers = {
  'mp3':  lambda f: mp3_handler(f),
  'flac': lambda f: flac_handler(f)
}


def index_files(search_path) -> Generator[MusicFile, None, None]:
  for root, dirs, files in walk(search_path):
    music_files = ((f, file_extension(f)) for f in files if file_extension(f) in file_extensions)
    for filename, extension in music_files:
      handler = handlers.get(extension)
      if not handler:
        print(f"Couldn't find handler for file type {extension}")
      else:
        music_file = handler(path.join(root, filename))
        yield music_file


def escape(in_str) -> str:
  if not in_str or type(in_str) is not str:
    return "unknown"
  in_str = in_str.replace('\'', '')
  return r""+in_str


@click.command()
@click.option('--search_path', help = 'Path to your music files')
@click.option('--database', help = 'Path to output SQLite data files')
def index(search_path, database):
  """
  Index files and build a database.
  """
  music_files = index_files(search_path)
  conn = sqlite3.connect(database)
  conn.execute(f"""
    create table if not exists music_files (
      title text,
      artist text,
      album text,
      album_artist text,
      track_number integer,
      full_path text,
      length integer
    )
  """)
  for mf in music_files:
    sql = f"""
      insert into music_files
      (title, artist, album, album_artist, track_number, full_path, length)
      values (
        '{escape(mf.title)}',
        '{escape(mf.artist)}',
        '{escape(mf.album)}',
        '{escape(mf.album_artist)}',
        '{escape(mf.track_number)}',
        '{escape(mf.full_path)}',
        {mf.length}
      )
    """
    conn.execute(sql)
  conn.commit()
  conn.close()
