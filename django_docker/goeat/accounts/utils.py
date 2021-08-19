import random

# def id_generator(size=4 , chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

chars = 'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789'

def id_generator(size=4 , chars=chars):
    return ''.join(random.choice(chars) for _ in range(size))