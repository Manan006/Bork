import internalapi
import os
from easypydb import DB

from internalapi.cache import *
from internalapi.user import user
from internalapi.methods import *
from internalapi.borks import *
from internalapi.session import *

# experimentation code

for ua in user.fetchAll().content:
	print(ua.userid, ua.username)

# end experimentation code

import webapp.init
# anything after this point will not run