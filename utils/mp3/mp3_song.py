import os
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, TIT2, TALB, TPE1, USLT, TRCK


class MP3Song:

    def __init__(self, filepath):
        if not os.path.exists(filepath):
            raise Exception('No file was found in path: %s' % filepath)
        if not filepath.endswith('.mp3'):
            raise Exception('The file must be a mp3 file')
        self.filename = os.path.basename(filepath)[:-4]
        self.filepath = filepath
        try:
            self.id3 = ID3(filepath)
        except ID3NoHeaderError:
            self.id3 = ID3()

    def save(self):
        self.id3.save(self.filepath)

    def set_title(self, title):
        self.id3['TIT2'] = TIT2(encoding=3, text=title)

    def set_album(self, album):
        self.id3['TALB'] = TALB(encoding=3, text=album)

    def set_artist(self, artist):
        self.id3['TPE1'] = TPE1(encoding=3, text=artist)

    def set_lyric(self, lyric):
        if len(self.id3.getall('USLT')) != 0:
            self.id3.delall('USLT')
        self.id3['USLT'] = USLT(lang='eng', desc='', text=lyric)

    def set_cover(self, cover_file):
        if len(self.id3.getall('APIC')) != 0:
            self.id3.delall('APIC')
        with open(cover_file, 'rb') as cover:
            self.id3['APIC'] = APIC(
                mime='image/jpeg',  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc='Cover',
                data=cover.read()
            )

    def set_track_number(self, track_number):
        self.id3['TRCK'] = TRCK(encoding=3, text=track_number)

    def print_tags(self):
        tags = self.id3
        for key in tags.keys():
            if hasattr(tags[key], 'text'):
                if len(tags[key].text) > 64:
                    print('{}: {}'.format(key, tags[key][:64]))
                else:
                    print('{}: {}'.format(key, tags[key]))
            elif hasattr(tags[key], 'data'):
                if len(tags[key].data) > 64:
                    print('{}: {}'.format(key, tags[key].data[:64]))
                else:
                    print('{}: {}'.format(key, tags[key].data))
            elif key.startswith('PRIV'):
                pass
            else:
                print('{}: {}'.format(key, tags[key]))

    def print_known_tags(self):
        tags = self.id3
        # self.print_tags()
        print('Title: {}'.format(tags['TIT2'] if 'TIT2' in tags else '[No title, song name or content description]'))
        print('Album: {}'.format(tags['TALB'] if 'TALB' in tags else '[No album, movie or show title ]'))
        print('Artist: {}'.format(tags['TPE1'] if 'TPE1' in tags else '[No artist, lead performer(s) or soloist(s)]'))
        print('Lyric: {}'.format('YES' if tags.getall('USLT') != 0 else 'No'))
        print('Cover: {}'.format('YES' if tags.getall('APIC') != 0 else 'No'))
        print('Track number: ({})'.format(tags['TRCK'] if 'TRCK' in tags else '???'))

        '''
Title: Don't Let Me Down
COMM::eng: Comment ID3v2
COMM:Catalog Number:eng: catalog
POPM:Windows Media Player 9 Series: POPM(email='Windows Media Player 9 Series', rating=128)
PRIV:WM/Mood:m o o d   : b      'm\x00o\x00o\x00d\x00\x00\x00'

TCMP: 1
TCOM: composer
TCON: Charts
TCOP: copyright
TENC: encoded by
TEXT: A1

TMOO: mood

TPE2: Album artist
TPE3: conductor
TPUB: publisher
TRCK: 004
TSRC: isrc
TXXX:replaygain_album_gain: 232.00 dB
TXXX:replaygain_track_gain: -10.11 dB
USLT::eng: A2
WXXX:: url
APIC:: b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x03\x02\x02\x03\x03\x02\x03\x03\x03\x03\x03\x04\x07\x05\x04\x04\x04\x04\t\x06\x07\x05\x07\n\t\x0b\x0b\n\t\n\n\x0c\r\x11\x0e\x0c'
COMM:ID3v1 Comment:eng: Comment ID3v1
TDRC: 2016
        '''

        '''
4.20    AENC    [[#sec4.20|Audio encryption]]
4.15    APIC    [#sec4.15 Attached picture]
4.11    COMM    [#sec4.11 Comments]
4.25    COMR    [#sec4.25 Commercial frame]
4.26    ENCR    [#sec4.26 Encryption method registration]
4.13    EQUA    [#sec4.13 Equalization]
4.6     ETCO    [#sec4.6 Event timing codes]
4.16    GEOB    [#sec4.16 General encapsulated object]
4.27    GRID    [#sec4.27 Group identification registration]
4.4     IPLS    [#sec4.4 Involved people list]
4.21    LINK    [#sec4.21 Linked information]
4.5     MCDI    [#sec4.5 Music CD identifier]
4.7     MLLT    [#sec4.7 MPEG location lookup table]
4.24    OWNE    [#sec4.24 Ownership frame]
4.28    PRIV    [#sec4.28 Private frame]
4.17    PCNT    [#sec4.17 Play counter]
4.18    POPM    [#sec4.18 Popularimeter]
4.22    POSS    [#sec4.22 Position synchronisation frame]
4.19    RBUF    [#sec4.19 Recommended buffer size]
4.12    RVAD    [#sec4.12 Relative volume adjustment]
4.14    RVRB    [#sec4.14 Reverb]
4.10    SYLT    [#sec4.10 Synchronized lyric/text]
4.8     SYTC    [#sec4.8 Synchronized tempo codes]
4.2.1   TBPM    [#TBPM BPM (beats per minute)]
4.2.1   TCOM    [#TCOM Composer]
4.2.1   TCON    [#TCON Content type]
4.2.1   TCOP    [#TCOP Copyright message]
4.2.1   TDAT    [#TDAT Date]
4.2.1   TDLY    [#TDLY Playlist delay]
4.2.1   TENC    [#TENC Encoded by]
4.2.1   TEXT    [#TEXT Lyricist/Text writer]
4.2.1   TFLT    [#TFLT File type]
4.2.1   TIME    [#TIME Time]
4.2.1   TIT1    [#TIT1 Content group description]
4.2.1   TIT3    [#TIT3 Subtitle/Description refinement]
4.2.1   TKEY    [#TKEY Initial key]
4.2.1   TLAN    [#TLAN Language(s)]
4.2.1   TLEN    [#TLEN Length]
4.2.1   TMED    [#TMED Media type]
4.2.1   TOAL    [#TOAL Original album/movie/show title]
4.2.1   TOFN    [#TOFN Original filename]
4.2.1   TOLY    [#TOLY Original lyricist(s)/text writer(s)]
4.2.1   TOPE    [#TOPE Original artist(s)/performer(s)]
4.2.1   TORY    [#TORY Original release year]
4.2.1   TOWN    [#TOWN File owner/licensee]
4.2.1   TPE2    [#TPE2 Band/orchestra/accompaniment]
4.2.1   TPE3    [#TPE3 Conductor/performer refinement]
4.2.1   TPE4    [#TPE4 Interpreted, remixed, or otherwise modified by]
4.2.1   TPOS    [#TPOS Part of a set]
4.2.1   TPUB    [#TPUB Publisher]
4.2.1   TRDA    [#TRDA Recording dates]
4.2.1   TRSN    [#TRSN Internet radio station name]
4.2.1   TRSO    [#TRSO Internet radio station owner]
4.2.1   TSIZ    [#TSIZ Size]
4.2.1   TSRC    [#TSRC ISRC (international standard recording code)]
4.2.1   TSSE    [#TSEE Software/Hardware and settings used for encoding]
4.2.1   TYER    [#TYER Year]
4.2.2   TXXX    [#TXXX User defined text information frame]
4.1     UFID    [#sec4.1 Unique file identifier]
4.23    USER    [#sec4.23 Terms of use]
4.9     USLT    [#sec4.9 Unsychronized lyric/text transcription]
4.3.1   WCOM    [#WCOM Commercial information]
4.3.1   WCOP    [#WCOP Copyright/Legal information]
4.3.1   WOAF    [#WOAF Official audio file webpage]
4.3.1   WOAR    [#WOAR Official artist/performer webpage]
4.3.1   WOAS    [#WOAS Official audio source webpage]
4.3.1   WORS    [#WORS Official internet radio station homepage]
4.3.1   WPAY    [#WPAY Payment]
4.3.1   WPUB    [#WPUB Publishers official webpage]
4.3.2   WXXX    [#WXXX User defined URL link frame]        
        '''