import unittest

from src.models.schedule.schedule_enums import *


class TestScheduleEnums(unittest.TestCase):

    def test_scheduletype_enum(self):
        # values are correct
        self.assertEqual(ScheduleType.SECOND.value, 1)
        self.assertEqual(ScheduleType.MINUTE.value, 2)
        self.assertEqual(ScheduleType.HOUR.value, 3)
        self.assertEqual(ScheduleType.DAY.value, 4)
        self.assertEqual(ScheduleType.WEEK.value, 5)
        self.assertEqual(ScheduleType.MONTH.value, 6)
        self.assertEqual(ScheduleType.YEAR.value, 7)

        # names are correct
        self.assertEqual(ScheduleType.SECOND.name, "SECOND")
        self.assertEqual(ScheduleType.MINUTE.name, "MINUTE")
        self.assertEqual(ScheduleType.HOUR.name, "HOUR")
        self.assertEqual(ScheduleType.DAY.name, "DAY")
        self.assertEqual(ScheduleType.WEEK.name, "WEEK")
        self.assertEqual(ScheduleType.MONTH.name, "MONTH")
        self.assertEqual(ScheduleType.YEAR.name, "YEAR")
    

    def test_day_enum(self):
        # values are correct
        self.assertEqual(Day.MONDAY.value, 1)
        self.assertEqual(Day.TUESDAY.value, 2)
        self.assertEqual(Day.WEDNESDAY.value, 3)
        self.assertEqual(Day.THURSDAY.value, 4)
        self.assertEqual(Day.FRIDAY.value, 5)
        self.assertEqual(Day.SATURDAY.value, 6)
        self.assertEqual(Day.SUNDAY.value, 7)

        # names are correct
        self.assertEqual(Day.MONDAY.name, "MONDAY")
        self.assertEqual(Day.TUESDAY.name, "TUESDAY")
        self.assertEqual(Day.WEDNESDAY.name, "WEDNESDAY")
        self.assertEqual(Day.THURSDAY.name, "THURSDAY")
        self.assertEqual(Day.FRIDAY.name, "FRIDAY")
        self.assertEqual(Day.SATURDAY.name, "SATURDAY")
        self.assertEqual(Day.SUNDAY.name, "SUNDAY")

    
    def test_month_enum(self):
        # values are correct
        self.assertEqual(Month.JANUARY.value, 1)
        self.assertEqual(Month.FEBRUARY.value, 2)
        self.assertEqual(Month.MARCH.value, 3)
        self.assertEqual(Month.APRIL.value, 4)
        self.assertEqual(Month.MAY.value, 5)
        self.assertEqual(Month.JUNE.value, 6)
        self.assertEqual(Month.JULY.value, 7)
        self.assertEqual(Month.AUGUST.value, 8)
        self.assertEqual(Month.SEPTEMBER.value, 9)
        self.assertEqual(Month.OCTOBER.value, 10)
        self.assertEqual(Month.NOVEMBER.value, 11)
        self.assertEqual(Month.DECEMBER.value, 12)

        # names are correct
        self.assertEqual(Month.JANUARY.name, "JANUARY")
        self.assertEqual(Month.FEBRUARY.name, "FEBRUARY")
        self.assertEqual(Month.MARCH.name, "MARCH")
        self.assertEqual(Month.APRIL.name, "APRIL")
        self.assertEqual(Month.MAY.name, "MAY")
        self.assertEqual(Month.JUNE.name, "JUNE")
        self.assertEqual(Month.JULY.name, "JULY")
        self.assertEqual(Month.AUGUST.name, "AUGUST")
        self.assertEqual(Month.SEPTEMBER.name, "SEPTEMBER")
        self.assertEqual(Month.OCTOBER.name, "OCTOBER")
        self.assertEqual(Month.NOVEMBER.name, "NOVEMBER")
        self.assertEqual(Month.DECEMBER.name, "DECEMBER")


    def test_month_days(self):
        self.assertEqual(Month.FEBRUARY.days(2020), 29, msg="is leap year")
        self.assertEqual(Month.FEBRUARY.days(2021), 28)
        self.assertEqual(Month.JANUARY.days(2021), 31)



if __name__ == '__main__':
    unittest.main()