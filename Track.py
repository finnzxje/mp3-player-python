from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
class Track:
    def __init__(self):
        """"
        Initialize the Track class
        """
        self.title = ""
        self.artist = ""
        self.album = ""
        self.duration = 0
        self.file_path = ""

    def get_metadata(self, file_path):
        """"
        Get metadata from MP3 file and return it as a dictionary
        """
        audio = MP3(file_path)
        try:
            id3 = EasyID3(file_path)
        except ID3NoHeaderError:
            print("ID3 tag not found in file: {}".format(file_path))
            return {
                "title": "Not found",
                "artist": "Not found",
                "album": "Not found",
                "duration": audio.info.length,
                "file_path": file_path
            }

        self.title = id3["title"][0]
        self.artist = id3["artist"][0]
        self.album = id3["album"][0]
        self.duration = audio.info.length
        self.file_path = file_path

        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration,
            "file_path": self.file_path
        }

if __name__ == "__main__":
    """"
    Test the Track class with local file path
    """
    test = Track()
    print(test.get_metadata("C:\\Users\\LENOVO\\Desktop\\TEFLON DON.mp3"))
