import requests
from PIL import Image
from io import BytesIO

username = 'bigrigneedsfuel'
getUserURL = 'https://api.sleeper.app/v1/user/{}'.format(username)
response = requests.get(getUserURL)

data = response.json()
user_id = data.get('user_id')

getLeaguesURL = 'https://api.sleeper.app/v1/user/{}/leagues/nfl/2024'.format(user_id)
response = requests.get(getLeaguesURL)
leagueData = response.json()

userLeagues = {league.get('name'): league.get('avatar') for league in leagueData}
userLeaguesAndThumbnails = {}

for league, avatar_id in userLeagues.items():

    getAvatarThumbnailURL = 'https://sleepercdn.com/avatars/{}'.format(avatar_id)
    response = requests.get(getAvatarThumbnailURL)
    if response.status_code == 200:
        # Open and display the image using PIL
        image = Image.open(BytesIO(response.content))
        image.show()

        width,height = image.size
        print(width,height)

    else:
        # Load default image
        print(league)