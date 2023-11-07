import random
import string
from .models import giftGroups

# create groupPin generator
def generate_pin():
    while True:
        # Generate a random 5-character alphanumeric PIN (uppercase letters and numbers)
        characters = string.ascii_uppercase + string.digits +string.ascii_lowercase
        random_pin = ''.join(random.choice(characters) for _ in range(5))

        # Check if the PIN is already used
        if not giftGroups.objects.filter(groupPin=random_pin).exists():
            return(random_pin)
        

def listPair(people, noPairs):

    # Shuffle the list of people randomly
    random.shuffle(people)

    # Initialize a list to store the pairs
    pairs = []

    # Pair people while avoiding exclusions
    while people:
        person = people.pop(0)
        partner = None
        
        # Find a partner for the current person who is not in the exclusion list
        for candidate in people:
            if (person, candidate) not in noPairs and (candidate, person) not in noPairs:
                partner = candidate
                break
        
        if partner:
            pairs.append((person, partner))
            people.remove(partner)
        else:
            return
            # If no suitable partner found, handle it as needed (e.g., skip or record it)

        # Print the pairs
    for pair in pairs:
        print(f'{pair[0]} is paired with {pair[1]}')
    return(pairs)
