from firebase_admin import messaging

def send_to_firebase_cloud_messaging(token, title, body):
    token1 = 'f_Aw-meoDE9srshE5AACql:APA91bEU6UxsBtSfrEHR9cRb8x9bJuuQVvrvvGbQxXJ6WR5OuqBkdXz9AXd9i7See_pSt3gAznKxqYu5v3UYsEGZ-hLTrouAcSCInj3GGPV6qM25FmC5R11zRTU0XXbSH3xwcAENH9DM'
    token2 = 'eizBaXl-jkwVnL5PMOqGwB:APA91bEfEVvmhHXN6zESMbHfO8Sdnvh2ei3xQEbrf9Fm5Y8p1pg9Be6mjdS_h1IpSQwXiGNhm8kDYXqdeeotyeGLuFtaXgtHrSaq3Ij5ktlO9K0b29WHzg-7NESXpaRoy-rH7Y1QCm_K'
    
    token_list = [token1, token2]

    # message = messaging.Message(
    #     notification=messaging.Notification(
    #         title=title,
    #         body=body,
    #     ),
    #     apns=messaging.APNSConfig(
    #         payload=messaging.APNSPayload(
    #             aps=messaging.Aps(sound='default', badge=0,)
    #         ),
    #     ),
    #     token=token,
    # )

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