# Music Indexer

`music_indexer` is a tool for indexing messy directories of music files. It grew out of my need to track the different places
I was storing music files of various formats.

`music_indexer` searches a root directory for music files and generates a SQLite database file with metadata (artist, track 
number, etc.) which can be used for further analysis and management scripts.

## Motivation

I store music files on several different drives. I got sick of having to search through all of them to find my music. 
Furthermore, I couldn't find a single music player that properly indexed across large drives and output a SQL format
for user analysis. I decided to write this tool to provide a foundation for building a better solution for data geeks
who have a large music collection.

## Coming Soon

- A GUI!
- Supporting additional file formats
- Auto-generated analytics

![Screenshot](http://rquinlivan.net/wp-content/uploads/2020/05/Screen-Shot-2020-05-30-at-23.28.47-PM.png)
