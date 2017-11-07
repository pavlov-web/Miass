import datetime
import time
from tzlocal import get_localzone

tz = get_localzone() # Получаем локальную зону
print(tz)