
from Classes.animetoker import AnimeToker

class AnimeSender(AnimeToker): # Class to send Querries to Anilist database
    def __init__(self, Anime_Logger, **kwargs):
        self.anime_logger = Anime_Logger
        super().__init__(**kwargs)

    def set_episode(self, anime_id, episode):
        # Set the episode of an anime

        mutation = '''
        mutation {
          SaveMediaListEntry(mediaId: $anime_id, progress: $episode) {
          
          
          }
        }
        
        '''


        pass
    def set_status(self, anime_id, status):
        # Set the status of an anime
        pass
    def del_anime(self, anime_id):
        # Delete an anime from media database/list
        pass

    def next_episode(self, anime_id, fonclog):
        watch = self.anime_logger.anime_list[anime_id]["userlist"]["episode"]+1
        episodes = self.anime_logger.anime_list[anime_id]['media']['aired_episodes']

        if watch == episodes:
            self.set_status(anime_id, "Completed")
            fonclog("Status set to Completed")
            return episodes
        elif watch < episodes:
            self.set_episode(anime_id, watch)
            fonclog("Episode set to {}".format(watch))
            return watch
        else:
            fonclog("Nothing changed.")
            return watch-1


