import praw


from core.credentials import get_credentials, CredentialsLoader
credentials = CredentialsLoader.get_credentials("../credentials.ini")['reddit']

from core.history import SwitcharooLog
from core import constants as consts

reddit = praw.Reddit(client_id=credentials["client_id"],
                     client_secret=credentials["client_secret"],
                     user_agent=consts.user_agent,
                     username=credentials["username"],
                     password=credentials["password"])

switcharoo = reddit.subreddit("switcharoo")

last_switcharoo = SwitcharooLog(reddit)

print("SwitcharooHelper Flair Sync v{} Ctrl+C to stop".format(consts.version))

for flair in switcharoo.flair():
    print(flair)
    current_count = last_switcharoo.stats.num_of_good_roos(user=flair['user'].name)
    badge_count = 0
    if flair['flair_css_class']:
        if flair['flair_css_class'][:6] == "badge-":
            badge_count = int(flair['flair_css_class'][6:])
        if badge_count > current_count:
            last_switcharoo.update_user_flair(flair['user'].name, badge_count - current_count)

