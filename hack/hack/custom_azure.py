
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'strageforhack36o' # <storage_account_name>
    account_key = '0noTnpz6YAgW4UjuJkM7hD7Glo+S+LAeD/0aKFD53nISV1aw6GAnsx2lLZvPveXjcyCdLQ3tOj+R+AStv6/sRw==' # <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'strageforhack36o' # <storage_account_name>
    account_key = '+R/PFHg41m/ixbHSITMpqkA2ieDGMr9bIJQEgNwusaSs8RU79J2R5qqm6MvZpK5sFl5wn/JnbJiz+AStx0atjA==' # <storage_account_key>
    azure_container = 'static'
    expiration_secs = None