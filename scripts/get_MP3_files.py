import imp
import os

if __name__ == "__main__":
    loc = os.path.join('/home/ubuntu/PodcastRecommender/', "scripts/GrabMP3.py")
    MP3s = imp.load_source('Grab_MP3S', loc)
    MP3s = MP3s.Grab_MP3S()
    MP3s.send_to_S3()