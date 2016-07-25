from datetime import datetime, date
import time
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.utils import humanize_datetime
from rest_framework import serializers, ISO_8601


class DynamoDBDateTimeToTimestampField(serializers.DateTimeField):
    def to_internal_value(self, value):
        if isinstance(value, datetime):
            self.fail('date')

        if isinstance(value, datetime):
            return self.enforce_timezone(value)

        for frm in self.input_formats:
            if frm.lower() == ISO_8601:
                try:
                    parsed = parse_datetime(value)
                except (ValueError, TypeError):
                    pass
                else:
                    if parsed is not None:
                        return int(time.mktime(self.enforce_timezone(parsed).timetuple()))
            else:
                try:
                    parsed = datetime.strptime(value, frm)
                except (ValueError, TypeError):
                    pass
                else:
                    return int(time.mktime(self.enforce_timezone(parsed).timetuple()))

        humanized_format = humanize_datetime.datetime_formats(self.input_formats)
        self.fail('invalid', format=humanized_format)

    def to_representation(self, value):
        try:
            value = datetime.fromtimestamp(value)
        except TypeError:
            return ''

        if self.format is None:
            return value

        if self.format.lower() == ISO_8601:
            value = value.isoformat()
            if value.endswith('+00:00'):
                value = value[:-6] + 'Z'
            return value
        return value.strftime(self.format)


class DynamoDBDateToTimestampField(serializers.DateField):
    def __init__(self, *args, **kwargs):
        super(DynamoDBDateToTimestampField, self).__init__(*args, **kwargs)

    def to_internal_value(self, value):
        if isinstance(value, datetime):
            self.fail('datetime')

        if isinstance(value, date):
            return value

        for frm in self.input_formats:
            if frm.lower() == ISO_8601:
                try:
                    parsed = parse_date(value)
                except (ValueError, TypeError):
                    pass
                else:
                    if parsed is not None:
                        return int(time.mktime(parsed.timetuple()))
            else:
                try:
                    parsed = datetime.strptime(value, frm)
                except (ValueError, TypeError):
                    pass
                else:
                    return int(time.mktime(parsed.date().timetuple()))

        humanized_format = humanize_datetime.date_formats(self.input_formats)
        self.fail('invalid', format=humanized_format)

    def to_representation(self, value):
        """
        For DynamoDB proposal we use string iso format date and datetime
        """
        try:
            value = datetime.fromtimestamp(value)
        except TypeError:
            return ''

        if self.format is None:
            return value

        # Applying a `DateField` to a datetime value is almost always
        # not a sensible thing to do, as it means naively dropping
        # any explicit or implicit timezone info.

        if self.format.lower() == ISO_8601:
            return value.isoformat()
        return value.strftime(self.format)
