import random
# from accounts.models import TeamRequest

chars = 'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789'

def id_generator(size=4 , chars=chars):
    return ''.join(random.choice(chars) for _ in range(size))

# def get_team_request_or_false(sender, receiver):
#     try:
#         return TeamRequest.objects.get(sender=sender, receiver=receiver)
#     except TeamRequest.DoesNotExist:
#         return False