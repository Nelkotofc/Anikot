from datetime import date

import requests


class AnimeSearcher:
    popItems = ["averageScore", "episodes", "genres", "relations", "title"]
    def __init__(self, username):
        self.username = username
        self.anime_list = {} # Dictionary of anime objects
        self.today = date.today()
        self.category_list = {} # Dictionary of category objects

        # {category_name: [anime_id,...]}


        # media_id : {relations: {relation_type: [media_id, ...]}, userlist: {inside: LIST_NAME, episode: episode_watched, score: userscore}, media: {score: media_average_score, aired_episodes: media_aired_episodes, total_episodes: media_total_episodes, titles: {english: media_english, romaji: media_romaji}}}

    def seperate_category(self, fonclog):
        fonclog("Seperating categories...")
        for anime_id in list(self.anime_list.keys()):
            category_name = self.anime_list[anime_id]["userlist"]["inside"]
            if category_name != None:
                if category_name not in self.category_list:
                    self.category_list[category_name] = []
                self.category_list[category_name].append(anime_id)
    def create_titles(self, english, romaji, native):
        return {"english": english, "romaji": romaji, "native": native}

    def create_media(self, score, aired_episodes, total_episodes, titles, genres, aired, extras):
        return {"score": score, "aired_episodes": aired_episodes, "total_episodes": total_episodes, "titles": titles, "genres": genres, "aired": aired, "extra": extras}

    def create_userlist(self, inside, episode, score, total_episodes_left, aired_episodes_left):
        return {"inside": inside, "episode": episode, "score": score, "total_episodes_left": total_episodes_left, "aired_episodes_left": aired_episodes_left}

    def create_anime(self, media_id, relations, userlist, media):
        result = {"relations": relations, "userlist": userlist, "media": media}
        self.anime_list[media_id] = result

        return result

    def get_MediaList(self, fonclog):
        # Get the list of media from the user's account and return it as a list of Media objects
        fonclog("Getting media list...")

        query = '''
                query ($userName: String!) {
                  MediaListCollection (userName: $userName, type: ANIME) {
                    lists {
                      name
                      entries {
                        progress
                        score
                        media {
                          id
                          status
                          format
                          description
                          endDate {
                            year
                            month
                            day
                          }
                          season
                          seasonYear
                          seasonInt
                          duration
                          countryOfOrigin
                          trailer {
                            site
                            thumbnail
                          }
                          coverImage {
                            extraLarge
                            large
                            medium
                            color
                          }
                          bannerImage
                          synonyms
                          meanScore
                          popularity
                          trending
                          favourites
                          isFavourite
                          averageScore
                          episodes
                          isAdult
                          nextAiringEpisode {
                            episode
                            timeUntilAiring
                          }
                          genres
                          startDate {
                            year
                            month
                            day
                          }
                          title {
                            english
                            romaji
                            native
                          }
                          relations {
                            edges {
                              relationType
                              node {
                                id
                                format
                                status
                                description
                                endDate {
                                  year
                                  month
                                  day
                                }
                                season
                                isAdult
                                seasonYear
                                seasonInt
                                duration
                                countryOfOrigin
                                trailer {
                                  site
                                  thumbnail
                                }
                                isFavourite
                                coverImage {
                                  extraLarge
                                  large
                                  medium
                                  color
                                }
                                bannerImage
                                synonyms
                                meanScore
                                popularity
                                trending
                                favourites
                                averageScore
                                episodes
                                nextAiringEpisode {
                                  episode
                                  timeUntilAiring
                                }
                                genres
                                startDate {
                                  year
                                  month
                                  day
                                }
                                title {
                                  english
                                  romaji
                                  native
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
                '''

        variables = {
            'userName': self.username
        }

        anilist_response = requests.post('https://graphql.anilist.co',
                                         json={'query': query, 'variables': variables})

        if anilist_response.status_code != 200:
            quit(f"Error getting media list: {anilist_response.json()}")
        else:

            for category_json in anilist_response.json()['data']['MediaListCollection']['lists']:
                category_name = category_json['name']
                category_entries = category_json['entries']
                for anime_json in category_entries:
                    media_id = anime_json['media']['id']
                    media_english_title = anime_json['media']['title']['english']
                    media_romaji_title = anime_json['media']['title']['romaji']
                    media_native_title = anime_json['media']['title']['native']
                    media_score = anime_json['media']['averageScore']
                    media_total_episodes = anime_json['media']['episodes']
                    try :media_next_airing_episode = anime_json['media']['nextAiringEpisode']['episode']
                    except: media_next_airing_episode = None
                    media_start_date = anime_json['media']['startDate']
                    media_start_year = media_start_date['year']
                    media_start_month = media_start_date['month']
                    media_start_day = media_start_date['day']
                    media_progress = anime_json['progress']
                    media_user_score = anime_json['score']
                    media_genres = anime_json['media']['genres']
                    media_end_date = anime_json['media']['endDate']
                    media_end_year = media_end_date['year']
                    media_end_month = media_end_date['month']
                    media_end_day = media_end_date['day']

                    media_total_minutes = None
                    media_aired_minutes = None
                    media_watch_minutes = None
                    media_total_episodes_left = None
                    media_aired_episodes_left = None

                    media_relations = anime_json['media']['relations']
                    media_relations_dict = {}

                    media_extras = anime_json['media']
                    for item in self.popItems:
                        media_extras.pop(item)


                    media_aired_episodes = None

                    try:
                        media_startDate = date(media_start_year, media_start_month, media_start_day)
                        media_extras['startDate']['seconds'] = (media_startDate-date(1, 1, 1)).total_seconds()

                        if (self.today-media_startDate).total_seconds() >= 0:

                            if media_next_airing_episode is None:
                                media_aired_episodes = media_total_episodes
                            else:
                                media_aired_episodes = media_next_airing_episode-1
                    except: pass

                    try:
                        media_endDate = date(media_end_year, media_start_month, media_start_day)
                        media_extras['endDate']['seconds'] = (media_endDate - date(1, 1, 1)).total_seconds()
                    except:
                        pass

                    if media_aired_episodes is None:
                        media_aired_episodes = 0

                    media_aired = True if media_aired_episodes > 0 else False

                    try:
                        media_aired_episodes_left = media_aired_episodes - media_progress
                    except:
                        media_aired_episodes_left = None

                    try:
                        media_total_episodes_left = media_total_episodes - media_progress
                    except:
                        media_total_episodes_left = media_aired_episodes_left

                    for anime_relation in media_relations['edges']:

                        relation_type = anime_relation['relationType']

                        if relation_type != "ADAPTATION":

                            media_id_relation = anime_relation['node']['id']
                            media_english_title_relation = anime_relation['node']['title']['english']
                            media_romaji_title_relation = anime_relation['node']['title']['romaji']
                            media_native_title_relation = anime_relation['node']['title']['native']
                            media_score_relation = anime_relation['node']['averageScore']
                            try: media_next_airing_episode_relation = anime_relation['node']['nextAiringEpisode']['episode']
                            except: media_next_airing_episode_relation = None
                            media_total_episodes_relation = anime_relation['node']['episodes']
                            media_start_date_relation = anime_relation['node']['startDate']
                            media_start_year_relation = media_start_date_relation['year']
                            media_start_month_relation = media_start_date_relation['month']
                            media_start_day_relation = media_start_date_relation['day']
                            media_genres_relation = anime_relation['node']['genres']
                            media_end_date_relation = anime_relation['node']['endDate']
                            media_end_year_relation = media_end_date_relation['year']
                            media_end_month_relation = media_end_date_relation['month']
                            media_end_day_relation = media_end_date_relation['day']

                            if relation_type not in media_relations_dict:
                                media_relations_dict[relation_type] = []

                            media_relations_dict[relation_type].append(media_id_relation)

                            media_aired_episodes_relation = None

                            media_extras_relation = anime_relation['node']
                            for item in self.popItems:
                                try:
                                    media_extras_relation.pop(item)
                                except:
                                    pass

                            try:

                                media_startDate_relation = date(media_start_year_relation, media_start_month_relation, media_start_day_relation)
                                media_extras_relation['startDate']['seconds'] = (media_startDate_relation - date(1, 1, 1)).total_seconds()

                                if (self.today-media_startDate_relation).total_seconds() > 0:
                                    if media_next_airing_episode_relation is None:
                                        media_aired_episodes_relation = media_total_episodes_relation
                                    else:
                                        media_aired_episodes_relation = media_next_airing_episode_relation - 1
                            except:
                                pass

                            try:
                                media_endDate_relation = date(media_end_year_relation, media_start_month_relation, media_start_day_relation)
                                media_extras_relation['endDate']['seconds'] = (media_endDate_relation - date(1, 1, 1)).total_seconds()
                            except:
                                pass

                            if media_aired_episodes_relation is None:
                                media_aired_episodes_relation = 0

                            media_aired_relation = True if media_aired_episodes_relation > 0 else False

                            if media_id_relation not in self.anime_list or self.anime_list[media_id_relation]["userlist"]["inside"] == None:
                                self.create_anime(media_id_relation, {}, self.create_userlist(None, None, None, None, None), self.create_media(media_score_relation, media_aired_episodes_relation, media_total_episodes_relation, self.create_titles(media_english_title_relation, media_romaji_title_relation, media_native_title_relation), media_genres_relation, media_aired_relation, media_extras_relation))

                    self.create_anime(media_id, media_relations_dict, self.create_userlist(category_name, media_progress, media_user_score, media_total_episodes_left, media_aired_episodes_left), self.create_media(media_score, media_aired_episodes, media_total_episodes, self.create_titles(media_english_title, media_romaji_title, media_native_title), media_genres, media_aired, media_extras))



