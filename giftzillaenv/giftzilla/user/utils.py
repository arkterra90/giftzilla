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