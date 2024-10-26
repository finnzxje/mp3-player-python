from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


class Track:
    def __init__(self, file_path):
        """"
        Initialize the Track class
        """
        self.title = file_path.split("/")[-1].split(".mp3")[0]
        self.artist = ""
        self.album = ""
        self.duration = 0
        self.file_path = file_path
        self.get_metadata()

    def get_metadata(self):
        """"
        Get metadata from MP3 file and return it as a dictionary
        """
        audio = MP3(self.file_path)
        try:
            id3 = EasyID3(self.file_path)

        except ID3NoHeaderError:
            print("ID3 tag not found in file: {}".format(self.file_path))
            return {
                "title": self.title,
                "artist": "Not found",
                "album": "Not found",
                "duration": audio.info.length,
                "file_path": self.file_path
            }


        self.duration = audio.info.length

        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration,
            "file_path": self.file_path
        }

    def get_path(self):
        """"
        Return the file path of the track
        """
        return self.file_path

    def get_duration(self):
        """"
        Return the duration of the track
        """
        return self.duration

    def __str__(self):
        """
        Return the title of the track
        """
        return self.title

if __name__ == "__main__":
    """"
    Test the Track class with local file path
    """
    test = Track("C:\\Users\\minh2\\OneDrive\\Desktop\\python beginner project (mini)\\audio\\get-up-on-your-feet-204255.mp3")
    print(test.get_duration())
    print ("eh")