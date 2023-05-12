import os
import argparse
from utils.mp3.mp3_song import MP3Song
from utils.mp3.mp3_utils import print_mp3_files


def get_mp3_files_in(path, is_recursive):
    all_mp3 = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            if is_recursive:
                all_mp3 += get_mp3_files_in(os.path.abspath(file_path), is_recursive)
        else:
            if file.lower().endswith('.mp3'):
                all_mp3.append(file_path)
    return all_mp3


def get_lyric_from_txt(filename):
    if os.path.exists('%s.txt' % filename):
        lyric_file = open('%s.txt' % filename, 'r')
        return lyric_file.read()
    else:
        return None


def update_tags(mp3, args):
    if args.info:
        mp3.print_known_tags()
    if args.title:
        mp3.set_title(args.title)
        print('Updating title to %s' % args.title)
    if args.album:
        mp3.set_album(args.album)
        print('Updating album to %s' % args.album)
    if args.artist:
        mp3.set_artist(args.artist)
        print('Updating artist to %s' % args.artist)
    if args.merge_lyric:
        if os.path.exists('%s.txt' % mp3.filename):
            lyric_file = open('%s.txt' % mp3.filename, 'r')
            lyric = lyric_file.read()
        else:
            lyric = None
        if lyric:
            lyric = get_lyric_from_txt(mp3.filename)
            if lyric:
                mp3.set_lyric(lyric)
                print('Updating lyric')
    if args.cover:
        if not os.path.exists(args.cover):
            raise Exception('The selected cover path is not valid')
        mp3.set_cover(args.cover)
        print('Updating cover')
    if args.track_number:
        mp3.set_track_number(args.track_number)
        print('Updating track number to %s' % args.track_number)
    mp3.save()
    print('Done\n')


def main():
    parser = argparse.ArgumentParser(description='Manage metadata for mp3 files.')

    list_sub_parser = parser.add_subparsers(dest='command', required=True, title='Commands',
                                            metavar='  Run \'[command] --help\' for more information on a command.')
    ls = list_sub_parser.add_parser('ls', help='Show a list of every mp3 files in this folder.')
    ls.add_argument('-r', help='Show every mp3 files in sub folders also.', action='store_true')

    update = list_sub_parser.add_parser('update', help='Update the metadata of one or some mp3 files.')
    update.add_argument('--title', help='Update the mp3 title')
    update.add_argument('--artist', help='Update the mp3 artist')
    update.add_argument('--album', help='Update the mp3 album')
    update.add_argument('-r', help='Update every mp3 files in sub folders also.', action='store_true')
    update.add_argument('file')

    info = list_sub_parser.add_parser('info', help='Show the metadata of one mp3 file.')
    info.add_argument('file')

    parser.add_argument('--merge-lyric', '-ml', action='store_true')
    parser.add_argument('--search-lyric', '-sl', action='store_true')
    parser.add_argument('--track-number')
    parser.add_argument('--cover', '-c')
    # parser.add_argument('--lyric')

    args = parser.parse_args()

    if args.command == 'ls':
        is_recursive = True if args.recursive is not None else False
        print_mp3_files(os.curdir, is_recursive)
    elif args.command == 'update':
        # todo update this
        if args.file == '.':
            is_recursive = True if args.recursive is not None else False
            mp3s = get_mp3_files_in(os.curdir, is_recursive)
            for file in mp3s:
                mp3 = MP3Song(file)
                print('Analyzing %s.mp3:' % mp3.filename)
                update_tags(mp3, args)
        else:
            mp3 = MP3Song(args.file)
            print(mp3.filename)
            update_tags(mp3, args)
    elif args.command == 'info':
        # todo improve the info shown
        if os.path.exists(args.file):
            mp3 = MP3Song(args.file)
            mp3.print_known_tags()
        else:
            print('ERROR: File not found')


if __name__ == '__main__':
    main()
