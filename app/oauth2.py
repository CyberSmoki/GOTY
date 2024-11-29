from goty import settings
import requests


def get_oauth2_link() -> str:
    return "https://discord.com/oauth2/authorize?" + "&".join(
        [
            f"client_id={settings.CLIENT_ID}",
            "response_type=code",
            f"redirect_uri={settings.REDIRECT_URI}",
            "scope=identify"
        ]
    )


def get_user(token: str) -> dict:
    ...
    r = requests.get(
        f'{settings.API_ENDPOINT}/users/@me',
        headers={'Authorization': f'Bearer {token}'}
    )
    r.raise_for_status()
    return r.json()


class DiscordWrapper:
    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    """
    Return access token response
    https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-response
    """

    def process_code(self, code: str) -> dict:
        token = self.exchange_code(code)
        user = get_user(token['access_token'])
        return user

    def exchange_code(self, code: str) -> dict:
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.REDIRECT_URI,
        }
        r = requests.post(
            f'{settings.API_ENDPOINT}/oauth2/token',
            data=data,
            headers=self.HEADERS,
            auth=(settings.CLIENT_ID, settings.CLIENT_SECRET)
        )
        r.raise_for_status()
        return r.json()
