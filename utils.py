from db_models import Course
import datetime
from const import date_format


def row_to_dict(row):
    result = {}
    for column in get_courses_columns():
        value = getattr(row, column)
        if isinstance(value, datetime.date):
            value = value.strftime(date_format)
        result[column] = value
    return result


def get_courses_columns():
    columns = [column.name for column in Course.__table__.columns]
    return columns
