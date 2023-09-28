def register():
    role = request.form.get('role')
    if role == 'owner':
        calendar_service = get_calendar_service()
        # Save owner's email to owner_email.txt
        with open('owner_email.txt', 'w') as f:
            f.write(calendar_service.calendarList().get(calendarId='primary').execute()['id'])
        with open('calendar_service.pkl', 'wb') as f:
            pickle.dump(calendar_service, f)
    elif role == 'assistant':
        gmail_service = get_gmail_service()
        # Save assistant's email to assistant_email.txt
        with open('assistant_email.txt', 'w') as f:
            f.write(gmail_service.users().getProfile(userId='me').execute()['emailAddress'])
        with open('gmail_service.pkl', 'wb') as f:
            pickle.dump(gmail_service, f)
    return redirect('/')
