# Compilation of python scripts for automatize daily tasks



## mp3

---

Description

### How to use it
[erno]: <> (Separate this project in another git repository and write step 1 and 2)
1. Clone project
2. Open folder
3. Build the docker image `docker build . -t mp3-manager --network=host`  
    * You can replace `mp3-manager` for the name of the image that you want (If that is the case remember to replace it in all the steps).
    * `--network=host` is needed in order to install the requirements.
4. Move to your music folder.
5. Run a container with the script `docker run --rm -v "$(pwd)":/app/music mp3-manager`
    * `--rm` remove the container after execution.
    * `"$(pwd)"` refers to the current folder where the music is supposed to be.
    
### Available commands

> ls

Show a list of every mp3 files in this folder. Arguments:

| Parameters | Optional | Meaning |
| ---------- | -------- | ------- |
| `-r` or `--recursive` | Yes | Show every mp3 files in sub folders also |

> update

Update the metadata of one, or some mp3 files. Arguments:

| Parameters | Optional | Meaning |
| ---------- | -------- | ------- |
| `--title` \<title> | Yes | Update the mp3 title |
| `--artist` \<artist> | Yes | Update the mp3 artist |
| `--album` \<album>| Yes | Update the mp3 album |
| `-r` or `--recursive` | Yes | Update every mp3 files in sub folders also |
| \<filename> | No | Name of the file that will be updated |

> info

Show the metadata of one mp3 file.

| Parameters | Optional | Meaning |
| ---------- | -------- | ------- |
| \<filename> | No | Name of the file that the data will be shown |


    parser.add_argument('--merge-lyric', '-ml', action='store_true')
    parser.add_argument('--search-lyric', '-sl', action='store_true')
    parser.add_argument('--track-number')
    parser.add_argument('--cover', '-c')




## `lyric.py`
Get the lyric of a song from www.letras.com passing the name of the song and searching in the first 4 search results.

## `mh.py`
Randomize weapons in monster hunter games.