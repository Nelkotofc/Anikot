import webbrowser


class AnimeToker: # Class to manage the token
    def __init__(self, **kwargs):
        kwargs["logs"]("Getting token ...")
        self.token = self.get_token(kwargs.get('client_id'), kwargs.get('fonction'), kwargs.get('args'), kwargs.get('openWebbrowser'), kwargs.get('WebSiteArgument'))
        kwargs["logs"](f"Token: {self.token}")

    def get_token(self, client_id, fonction, args, openWebbrowser, WebSiteArgument):

        if args is None:
            args = []

        if WebSiteArgument is None:
            WebSiteArgument = False

        if openWebbrowser is None:
            openWebbrowser = True

        if client_id is None:
            quit("There is no client_id provided")

        if fonction is None:
            quit("There is no fonction provided")

        if openWebbrowser:

            webbrowser.open(f'https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&response_type=token')


        if WebSiteArgument:
            return fonction(WebSiteArgument, *args)

        return fonction(*args)