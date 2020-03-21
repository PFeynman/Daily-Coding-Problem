import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import email
import re

# The creation of the service has been copied from https://developers.google.com/gmail/api/quickstart/python

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def create_service():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)

  service = build('gmail', 'v1', credentials=creds)

  return service

def get_label_id(service):
  label_name = 'Daily Coding Problem'
  label_id = None
  results = service.users().labels().list(userId='me').execute()
  labels = results.get('labels', [])

  for label in labels:
    if label['name'] == label_name:
      label_id = label['id']
      break
  
  return label_id

def get_problem_number(msg_string):
  pattern = 'Problem #[0-9]+'
  return re.search(pattern, msg_string).group(0).replace('Problem #', '')

def extract_statement(msg_string):
  begining_string = 'Good morning! Here\'s your coding interview problem for today.\r\n\r\n'
  ending_string = '--------------------------------------------------------------------------------'

  statement = msg_string.partition(begining_string)[2]
  statement = statement.split(ending_string)[0]
  statement = statement.replace('=3D', '=')

  return statement

def create_directory(problem_number, statement):
  path = f'Problem {problem_number}'

  try:
    os.mkdir(path)
  except OSError:
    print ("Creation of the directory %s failed" % path)
  else:
    readme = open(f'{path}/README.md', 'w', newline='')
    readme.write(f'# {path}')
    readme.write('\r\n\r\n')
    readme.write(statement)
    readme.close()

    problem_file = open(f'{path}/problem_{problem_number}.py', 'w')
    problem_file.close()

    tests_file = open(f'{path}/test_problem_{problem_number}.py', 'w')
    tests_file.write('import unittest\r\n')
    tests_file.write(f'class TestsProblem{problem_number}(unittest.TestCase):')
    tests_file.close()

def main():
    
    service = create_service()

    label_id = get_label_id(service)

    results = service.users().messages().list(userId='me', labelIds=[label_id], q="is:unread").execute()
    while 'nextPageToken' in results:
      results = service.users().messages().list(userId='me', labelIds=[label_id], pageToken=results['nextPageToken'], q="is:unread").execute()

    message = service.users().messages().get(userId='me', id=results['messages'][-1]['id'], format='raw').execute()
    
    msg_bytes = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    msg_string = msg_bytes.decode('ASCII')
    msg_string = msg_string.replace('=\r\n', '')

    problem_number = get_problem_number(msg_string)
    problem_statement = extract_statement(msg_string)
    create_directory(problem_number, problem_statement)

if __name__ == '__main__':
    main()