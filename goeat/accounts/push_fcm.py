from firebase_admin import messaging

def push_team_request(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(sound='default', badge=0,)
            ),
        ),
        token=token,
    )

    try:
        response = messaging.send(message)
        print(response)
    except Exception as e:
        print(e)

def push_notice(token_list, title, body):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(sound='default', badge=0,)
            ),
        ),
        tokens=token_list,
    )

    try:
        response = messaging.send_multicast(message)
    except:
        pass