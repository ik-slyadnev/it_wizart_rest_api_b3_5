from services.dm_api.account.account import AccountApi
from services.dm_api.account.login import LoginApi
from configs.configuration import Configuration

class DMApiAccount:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.account_api = AccountApi(configuration=self.configuration)
        self.login_api = LoginApi(configuration=self.configuration)
