
## ID3 tags
Code example
```python
from mutagen.id3 import ID3

tags = ID3('file_path')
for key in tags.keys():
    # print all of the keys and its current value
    print('{} = {}'.format(key, tags[key]))
```

To see all possible tags see this [link](https://id3.org/id3v2.3.0#ID3v2_header).
