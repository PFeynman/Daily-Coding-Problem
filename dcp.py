import pickle
import os.path
import base64
import re

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import email

# The creation of the service has been copied from https://developers.google.com/gmail/api/quickstart/python

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

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

def get_next_problem(service, label_id):
  subject_pattern = 'Daily Coding Problem: Problem #([0-9]+)'

  results = service.users().messages().list(userId='me', labelIds=[label_id], q="is:unread").execute()
  while 'nextPageToken' in results:
    results = service.users().messages().list(userId='me', labelIds=[label_id], pageToken=results['nextPageToken'], q="is:unread").execute()

  msg_index = -1
  message = service.users().messages().get(userId='me', id=results['messages'][msg_index]['id']).execute()
  match = re.match(subject_pattern, message['payload']['headers'][16]['value'])
  while match is None:
    mark_email_as_read(service, message['id'])
    msg_index -= 1
    message = service.users().messages().get(userId='me', id=results['messages'][msg_index]['id']).execute()
    match = re.match(subject_pattern, message['payload']['headers'][16]['value'])
  
  return message, match.group(1)

def mark_email_as_read(service, message_id):
  service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD'], 'addLabelIds': []}).execute()

def extract_statement(message):
  begining_string = 'Good morning! Here\'s your coding interview problem for today.\r\n\r\n'
  ending_string = '--------------------------------------------------------------------------------'
  
  msg_bytes = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'].encode('ASCII'))
  msg_string = msg_bytes.decode('ASCII')

  statement = msg_string.partition(begining_string)[2]
  statement = statement.split(ending_string)[0]
  statement = statement.replace('\r\n\r\n\r\n\r\n', '')

  return statement

def create_directory(problem_number, statement):
  path = f'Problem {problem_number}'

  try:
    os.mkdir(path)
  except OSError:
    print ("Creation of the directory %s failed" % path)
  else:
    with open(f'{path}/README.md', 'w', newline='') as readme:
      readme.write(f'# {path}')
      readme.write('\r\n\r\n')
      readme.write(statement)
      readme.close()

    with open(f'{path}/problem_{problem_number}.py', 'w') as problem_file:
      problem_file.close()

    with open(f'{path}/test_problem_{problem_number}.py', 'w') as tests_file:
      tests_file.write('import unittest\r\n')
      tests_file.write(f'class TestsProblem{problem_number}(unittest.TestCase):')
      tests_file.close()

def main():
    service = create_service()

    label_id = get_label_id(service)

    message, problem_number = get_next_problem(service, label_id)

    problem_statement = extract_statement(message)
    
    create_directory(problem_number, problem_statement)
    
    mark_email_as_read(service, message['id'])

if __name__ == '__main__':
    main()