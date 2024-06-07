from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled
import math
class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'
    
