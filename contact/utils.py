from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


def get_upcoming_follow_up(begin_date, frequency):
  now = datetime.now()
  today = date(now.year, now.month, now.day)
  diff = relativedelta(today, begin_date)
  
  if today <= begin_date:
    return begin_date
  
  if frequency == 'once':
    return None
  elif frequency == 'weekly':
    if diff.days % 7 == 0:
      return today
    num_days_in_future = 7 - (diff.days % 7)
    return today + timedelta(days=num_days_in_future)
  elif frequency == 'quarterly':
    if diff.days == 0 and diff.months == 0:
      return begin_date + relativedelta(years=+diff.years)
    if diff.days == 0 and diff.months % 3 == 0:
      return begin_date + relativedelta(months=+diff.months) + relativedelta(years=+diff.years)
    num_months_since_start = (int(diff.months / 3) + 1) * 3
    return begin_date + relativedelta(months=+num_months_since_start) + relativedelta(years=+diff.years)
  elif frequency == 'monthly':
    num_months = diff.months
    if diff.days == 0:
      return begin_date + relativedelta(months=+num_months) + relativedelta(years=+diff.years)
    return begin_date + relativedelta(months=+num_months + 1) + relativedelta(years=+diff.years)
  elif frequency == 'annually':
    num_years = diff.years
    if diff.days == 0 and diff.months == 0:
      return begin_date + relativedelta(years=+num_years)
    return begin_date + relativedelta(years=+num_years + 1)
  else:
    return None