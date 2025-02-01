from services.mailhog.mailhog import MailhogApi
from configs.configuration import Configuration

class MailHogAPI:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api  = MailhogApi(configuration=self.configuration)
