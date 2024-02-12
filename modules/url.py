class change_url():
    def __init__(self, url: str):
        self.url = url
        pass

    def get_postUrl(self):
        id = self.get_id()
        return f"https://mbasic.facebook.com/story.php?story_fbid={id}&id=100063532603663"
    
    def get_reactorsUrl(self):
        id = self.get_id()
        return f"https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit=60&total_count=17&ft_ent_identifier={id}"
    
    def get_id(self):
        return self.url.split('/')[5]