from multiprocessing import Process
from string import ascii_uppercase
from Podcast_Meta import SavePodcast_meta

if __name__ == "__main__":
    proc = []
    for alpha in ascii_uppercase:
        p = Process(target=SavePodcast_meta(table_name = 'PodcastFinal_REAL_Alphabet_attempt',
                                             Letter=alpha).get_data())
        p.start()
        proc.append(p)
    for p in proc:
        p.join()
