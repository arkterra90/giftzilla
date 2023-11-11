import random
import string
from .models import giftGroups, listPair
from register.models import User

# create groupPin generator
def generate_pin():
    while True:
        # Generate a random 5-character alphanumeric PIN (uppercase letters and numbers)
        characters = string.ascii_uppercase + string.digits +string.ascii_lowercase
        random_pin = ''.join(random.choice(characters) for _ in range(5))

        # Check if the PIN is already used
        if not giftGroups.objects.filter(groupPin=random_pin).exists():
            return(random_pin)
        
# creates pairings at reg admin request
def regPairs(people, noPairs, max_attempts=100, max_retries=10):
    givers = list(people)
    receivers = list(people)
    pairings = None

    for _ in range(max_retries):
        pairings = []
        for giver in givers:
            attempts = 0
            while attempts < max_attempts:
                receiver = random.choice(receivers)
                if giver != receiver and (giver, receiver) not in pairings and (giver, receiver) not in noPairs:
                    pairings.append((giver, receiver))
                    receivers.remove(receiver)
                    break
                attempts += 1

            if attempts >= max_attempts:
                pairings = None  # Reset pairings if unsuccessful within the limit
                break

        if pairings:
            break  # Successful pairings found, exit the loop

    return pairings
