from datetime import datetime, timedelta
from django.utils.timezone import make_aware

def get_last_week_date_range():
    end_date = make_aware(datetime.now())
    start_date = end_date - timedelta(days=7)
    return start_date, end_date
