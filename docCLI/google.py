import sys
from pathlib import Path
import httplib2

from googleapiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/drive'

def get_client_secret():
    try:
        secret_file = Path.cwd() / 'credentials/client_secret.json'
        if not secret_file.is_file():
            raise FileNotFoundError()
    except FileNotFoundError:
        print('Unable to find client secret. Exiting...')
        sys.exit(1)
    else:
        return secret_file


APPLICATION_NAME = 'docCLI'

def get_credentials():
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
    CLIENT_SECRET_FILE: Path = get_client_secret()
    home_dir = Path.home()
    credential_dir = home_dir / '.credentials'
    if not credential_dir.exists():
        credential_dir.mkdir()
    credential_path = credential_dir / 'drive-googleapis.json'

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
    return credentials

def drive_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('drive', 'v3', http=http)
    return service
