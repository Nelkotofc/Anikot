import copy
import time


class AnimeFilter:
    def __init__(self, anime_searcher, **kwargs):
        self.anime_searcher = anime_searcher
        self.reasons = {}
        self.utilisation = {}
        self.availables_animes = []

        self.log = kwargs["logs"]
        self.result = self.run(**kwargs)

    def reason(self, anime_id, msg):

        self.reasons[anime_id] = msg

        if msg in self.utilisation:
            self.utilisation[msg] += 1
        else:
            self.utilisation[msg] = 1

    def filtering(self, **kwargs):

        animes = copy.copy(self.anime_searcher.anime_list)

        self.utilisation["Total"] = len(list(animes.keys()))

        availables_animes = []

        for anime_id in list(animes.keys()):
            json = animes[anime_id]

            for name in list(kwargs.keys()): # filtering options
                value = kwargs[name]

                if name == "adult" and value is False and json["media"]["extra"]["isAdult"] is True:
                    # None/True -> False : removed
                    self.reason(anime_id, f"This anime is for adults")
                    break

                if kwargs["whitelists"] is not None and json["userlist"]["inside"] not in kwargs["whitelists"]:
                    self.reason(anime_id, f"This anime category is not whitelisted")
                    break
                if kwargs["blacklists"] is not None and json["userlist"]["inside"] in kwargs["blacklists"]:
                    self.reason(anime_id, f"This anime category is blacklisted")
                    break

                if name == "format":
                    if value is not None:
                        if json["media"]["extra"]["format"] not in value:
                            self.reason(anime_id, f"This anime format is not in {value}")
                            break

                if name == "aired":
                    if value is not None:
                        if json["media"]["aired"] != value:
                            self.reason(anime_id, f"This anime aired value is not {value}")
                            break

                if name == "status":
                    if value is not None:
                        if json["media"]["extra"]["status"] not in value:
                            self.reason(anime_id, f"This anime status is not in {value}")
                            break

                if kwargs["whitelist_countries"] is not None and json["media"]["extra"]["countryOfOrigin"] not in \
                        kwargs[
                            "whitelist_countries"]:
                    self.reason(anime_id, f"This anime country is not whitelisted")
                    break
                if kwargs["blacklist_countries"] is not None and json["media"]["extra"]["countryOfOrigin"] in kwargs[
                    "blacklist_countries"]:
                    self.reason(anime_id, f"This anime country is blacklisted")
                    break

                if name == "whitelist_genres":
                    if value is not None:

                        if kwargs["whitelist_any_genres"] is False or kwargs["whitelist_any_genres"] is None:
                            # Needs all genres

                            breaked = False

                            for genre in value:
                                genre_in_value = genre in json["media"]["genres"]

                                if genre_in_value is False:
                                    self.reason(anime_id, f"This anime needs every one of these genres: {value}")
                                    breaked = True
                                    break

                            if breaked:
                                break

                        else:
                            # Needs at least one genre

                            has = 0

                            for genre in value:
                                genre_in_value = genre in json["media"]["genres"]

                                if genre_in_value is True:
                                    has += 1

                            if has == 0:
                                self.reason(anime_id, f"This anime needs at least one of these genres: {value}")
                                break

                if name == "blacklist_genres":
                    if value is not None:

                        breaked = False

                        for genre in value:
                            genre_in_value = genre in json["media"]["genres"]

                            if genre_in_value is True:
                                self.reason(anime_id, f"This anime must not have any of these genres: {value}")
                                breaked = True
                                break

                        if breaked:
                            break

            else:
                availables_animes.append(animes[anime_id])

        self.utilisation["Filtered"] = len(availables_animes)

        return availables_animes

    def sorting_kwarg(self, **kwargs):

        # Popularity/Trending/AverageScore/UserScore/Favorites/
        # StartDate/EndDate/MeanScore/Aired/AiredEpisodes/Duration/IsFavourite/
        # NextAiring/Status/AiredEpisodesLeft/TotalEpisodes/Category/TotalEpisodesLeft/Country

        match kwargs["sort"]:
            case "Popularity":
                return ["media", "extra", "popularity"]

            case "Trending":
                return ["media", "extra", "trending"]

            case "AverageScore":
                return ["media", "score"]

            case "UserScore":
                return ["userlist", "score"]

            case "Favorites":
                return ["media", "extra", "favourites"]

            case "StartDate":
                return ["media", "extra", "startDate", "seconds"]

            case "EndDate":
                return ["media", "extra", "endDate", "seconds"]

            case "MeanScore":
                return ["media", "extra", "meanScore"]

            case "Aired":
                return ["media", "aired"]

            case "AiredEpisodes":
                return ["media", "aired_episodes"]

            case "Duration":
                return ["media", "extra", "duration"]

            case "IsFavourite":
                return ["media", "isFavourite"]

            case "NextAiring":
                return ["media", "extra", "nextAiringEpisode", "timeUntilAiring"]

            case "Status":
                return ["media", "extra", "status"]

            case "AiredEpisodesLeft":
                return ["userlist", "aired_episodes_left"]

            case "TotalEpisodes":
                return ["media", "total_episodes"]

            case "Category":
                return ["userlist", "inside"]

            case "TotalEpisodesLeft":
                return ["userlist", "total_episodes_left"]

            case "Country":
                return ["media", "extra", "countryOfOrigin"]

        return None

    def sorting(self, lis, **kwargs):
        order = self.sorting_kwarg(**kwargs)

        def dict_linner(dic, values):
            try:
                for value in values:
                    dic = dic[value]

                if dic is True:
                    dic = 2
                if dic is False:
                    dic = 1

                if dic is None:
                    return 0

                return dic
            except:
                return 0

        try:

            lis.sort(key=lambda x: dict_linner(x, order))

            if not kwargs["reverse"]:
                lis.reverse()

            return lis
        except:
            try:
                if not kwargs["reverse"]:
                    lis.reverse()

                return lis
            except:
                return lis

    def run(self, **kwargs):
        timer = time.time()
        availables_animes = self.filtering(**kwargs)
        self.log(f"Filtering time: {time.time() - timer}")
        timer = time.time()
        sorted_animes = self.sorting(availables_animes, **kwargs)
        self.log(f"Sorting time: {time.time() - timer}")
        return sorted_animes





