import requests
from PIL import Image
from io import BytesIO

from utils import *

class SleeperBackend:
    def __ini__(self):
        pass

    def set_username(self, username):
        '''Set the sleeper username for the session'''
        self.username = username

    def set_user_id(self):
        '''GET the user id from the Sleeper API user endpoint'''
        getUserURL = 'https://api.sleeper.app/v1/user/{}'.format(self.username)
        response = requests.get(getUserURL)

        data = response.json()
        self.user_id = data.get('user_id')

    def get_user_leagues(self):
        '''GET the user leagues form the Sleeper API leagues endpoint'''
        getLeaguesURL = 'https://api.sleeper.app/v1/user/{}/leagues/nfl/2024'.format(self.user_id)
        response = requests.get(getLeaguesURL)
        self.leagueData = response.json()
        self.leagueNames = [league.get('name') for league in self.leagueData]

    

    def get_league_images(self):
        '''GET the user league images from the Sleeper API avatars endpoint'''
        self.userLeaguesAndImages = {}
        userLeaguesAndAvatarID = \
        {league.get('name'): league.get('avatar') for league in self.leagueData}

        # Loop through each league and retrieve the thumbnail image
        for league, avatar_id in userLeaguesAndAvatarID.items():
            getAvatarThumbnailURL = 'https://sleepercdn.com/avatars/{}'.format(avatar_id)
            response = requests.get(getAvatarThumbnailURL)
            if response.status_code == 200:
                # Open and display the image using PIL
                image = Image.open(BytesIO(response.content))
                image = image.resize(LEAGUE_IMAGE_SIZE)
                image.show()
                print(image.size)
                # Not sure the best way to store this is yet for react
                self.userLeaguesAndImages[league] = image
            else:
                # Load default image
                size = (80,80)
                with Image.open(DEFAULT_LEAGUE_IMAGE) as image:
                    image = image.resize(LEAGUE_IMAGE_SIZE)
                    
                image.show()
                self.userLeaguesAndImages[league] = image
