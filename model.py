ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551
# We've taken the precaution of running the password through a hashing function first. 
# We can hash in Python! hash('string')

def authenticate(username, password):
    if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
        return ADMIN_USER # Why are we returning this? Instead of True/False earlier? Hm.
    else: 
        return None


# Note: We've made authenticate into a dual use function. 
# It has the original capability, tell us if the username and password are valid or not, 
# but it also returns the user attached to those credentials if we need it. 
# In this form, we can check success of an authenticate by simply checking 
# if the value is None or not None (False or True), and if we need the username as well, 
# we already have it.
