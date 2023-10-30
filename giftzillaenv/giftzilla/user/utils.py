import random
import string
from .models import giftGroups

# create groupPin generator
def generate_pin():
    while True:
        # Generate a random 5-character alphanumeric PIN (uppercase letters and numbers)
        characters = string.ascii_uppercase + string.digits
        random_pin = ''.join(random.choice(characters) for _ in range(5))

        # Check if the PIN is already used
        if not giftGroups.objects.filter(pin=random_pin).exists():
            return(random_pin)