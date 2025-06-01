import random
import string
import json


def random_name():
    return ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(5)])


def random_email():
    return random_name() + '@gmail.com'


def random_password():
    return random_name() + ''.join([random.choice(string.digits) for i in range(4)])


def random_age():
    return str(random.choice(range(0, 10)))


def random_type():
    return random.choice(['dog', 'cat', 'reptile', 'hamster', 'parrot'])


def random_gender():
    return random.choice(['Female', 'Male'])

def extract_pet_id(pets_list: list):
    return [pet.id for pet in pets_list.list]

def extract_not_liked_pet_id(pets_list: list):
    return [pet.id for pet in pets_list.list if pet.likes_count == 0]