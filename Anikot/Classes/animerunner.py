import json

from Classes.animefilter import AnimeFilter
from Classes.animelogger import AnimeLogger
from Classes.animesender import AnimeSender


class AnimeRunner: # Class to create interface and/or interact with the Anilist application
    def __init__(self, **kwargs):
        print("Starting ...")

        pseudo = kwargs.get("pseudo") if kwargs.get("pseudo") is not None else quit("Pseudo is not defined")

        self.logs = kwargs.get("logs_file_path")

        if self.logs is not None:
            open(self.logs, "w").close()
            if kwargs.get("logs") is None:
                print("Logs method is not defined")
                kwargs["logs"] = self.log

        else:
            print("Logs file path is not defined")
            kwargs["logs"] = self.log

        kwargs["logs"](f"Pseudo: {pseudo}")
        self.anime_logger = AnimeLogger(pseudo, kwargs["logs"])
        self.export_animes(**kwargs)
        kwargs["logs"]("AnimeLogger finished")
        #self.anime_sender = AnimeSender(self.anime_logger, **kwargs)
        kwargs["logs"]("AnimeSender finished")

        self.logs_kwargs = kwargs.get("logs")

        if kwargs.get("filtering"):
            kwargs["logs"](f"Total Filtering : {len(self.filtering(**kwargs))}")


    def log(self, msg):
        if self.logs is None:
            print(msg)
        else:
            with open(self.logs, "a") as f:

                if type(msg) is dict:
                    f.write(json.dumps(msg) + "\n")
                else:
                    f.write(msg + "\n")

                f.close()


    def filtering(self, **kwargs):

        if kwargs.get("logs") is None:
            kwargs["logs"] = self.logs_kwargs
        kwargs["logs"]("Filtering ...")
        Filter = AnimeFilter(self.anime_logger, **kwargs)
        if kwargs.get("export_filters") is not None:
            self.export_file(kwargs.get("export_filters"), Filter.result)
        if kwargs.get("export_reasons") is not None:
            self.export_file(kwargs.get("export_reasons"), Filter.reasons)
            self.export_file(kwargs.get("export_reasons"), Filter.utilisation, w="a")
        return Filter.result

    def export_file(self, filepath, dictionary, w="w"):
        try:
            with open(filepath, w) as f:
                f.write(json.dumps(dictionary, indent=4, sort_keys=True) + "\n")
                f.close()
        except:
            quit(f"Error exporting file : {filepath} - {json.dumps(dictionary, indent=4, sort_keys=True)}")


    def export_animes(self, **kwargs):

        if kwargs.get("export_file"):
            self.export_file(kwargs.get("export_file_path"), self.anime_logger.anime_list)


        if kwargs.get("export_category_file"):
            self.export_file(kwargs.get("export_category_file_path"), self.anime_logger.category_list)





