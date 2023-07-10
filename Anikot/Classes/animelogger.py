import time

import requests

from Classes.animesearcher import AnimeSearcher


class AnimeLogger(AnimeSearcher): # Class to get the user's info about
    def __init__(self, pseudo, fonclog=None, usertest=False):
        self.pseudo = pseudo
        if fonclog is not None:
            fonclog("Getting user info ...")
        self.user = self.get_user(pseudo)
        super().__init__(pseudo)
        if not usertest:
            timer = time.time()
            self.get_MediaList(fonclog)
            fonclog(f"Media list retrieved in {time.time()-timer} seconds")
            timer = time.time()
            self.seperate_category(fonclog)
            fonclog(f"Media list seperated in {time.time()-timer} seconds")
            fonclog("Done!")

    def get_user(self, pseudo): # Returns the user's id
        query = '''
        query ($userName: String!) {
          User (name: $userName) {
            id
            name
            avatar {
              large
              medium
            }
          }
        }
        '''

        var = {
            "userName": self.pseudo
        }

        anilist_response = requests.post('https://graphql.anilist.co',
                      json={'query': query, 'variables': var})

        if anilist_response.status_code != 200:
            quit(f"Error getting user info : {anilist_response.json()}")
        else:
            return anilist_response.json()

