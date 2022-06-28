from http import HTTPStatus

from service.api_client_base import APIService
from service.api_client_dataclasses import BillStat, MonthStat, UserData, UserMonthStat, UserWeekStat, WeekStat


class FakeAPIService(APIService):
    async def get_bill(self) -> BillStat:
        return BillStat([147892, 147983, 147894])

    async def get_week_stat(self) -> WeekStat:
        return WeekStat(
            [UserWeekStat(971746479, "UTC+3", "24", 2, 3, 2, 1, 1), UserWeekStat(971746479, "UTC+4", "25", 3, 4, 2, 1, 1)]
        )

    async def get_month_stat(self) -> MonthStat:
        return MonthStat(
            [UserMonthStat(971746479, "UTC+3", 6, 8, 9.4, 4.3), UserMonthStat(971746479, "UTC+4", 6, 3, 6.4, 7.3)]
        )

    async def authenticate_user(self, telegram_id: int) -> UserData | None:  # если неавторизированный пользователь
        """TODO: consider the case if the user is not registered in site"""
        return UserData("Bob", "UTC+3", "24")
        # return None

    async def set_user_timezone(self, telegram_id: int, user_timezone: str) -> HTTPStatus:
        return HTTPStatus.OK
