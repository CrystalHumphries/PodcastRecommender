
from multiprocessing import Process
from string import ascii_uppercase
from Podcast_Meta import SavePodcast_meta

target=SavePodcast_meta(table_name = 'PodcastFinal_REAL_Alphabet_attempt',
                                         Letter='Z').get_data()