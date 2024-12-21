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


def get_avatar_link(user: dict) -> str:
    return f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}?size=96"


class DiscordWrapper:
    AUTH = (settings.CLIENT_ID, settings.CLIENT_SECRET)
    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    OAUTH_TOKEN_URL = f'{settings.API_ENDPOINT}/oauth2/token'

    """
    Return access token response
    https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-response
    """

    
    def process_code(self, code: str):
        token = self.exchange_code(code)
        if token is None:
            return None

        user = get_user(token['access_token'])
        self.revoke_access_token(token)
        return user

    def exchange_code(self, code: str):
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.REDIRECT_URI,
        }
        r = requests.post(
            self.OAUTH_TOKEN_URL,
            data=data,
            headers=self.HEADERS,
            auth=(settings.CLIENT_ID, settings.CLIENT_SECRET)
        )
        if r.status_code == 400:
            return None
        r.raise_for_status()
        return r.json()

    def revoke_access_token(self, access_token):
        data = {
            'token': access_token,
            'token_type_hint': 'access_token'
        }
        r = requests.post(
            self.OAUTH_TOKEN_URL + '/revoke',
            auth=self.AUTH,
            data=data,
            headers=self.HEADERS,
        )

        r.raise_for_status()
        return r.json()
