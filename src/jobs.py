from datetime import timedelta
from string import Template

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from constants.callback_data import CALLBACK_DONE_BILL_COMMAND, CALLBACK_SKIP_BILL_COMMAND
from core import config
from core.send_message import send_message, send_statistics
from service.api_client import APIService
from service.repeat_message import repeat_after_one_hour_button


async def weekly_stat_job(context: CallbackContext) -> None:
    """
    Send weekly statistics on the number of requests in the work
    """
    week_statistics = await APIService().get_week_stat()
    template_message = Template(
        "Вы делали добрые дела 7 дней!\n"
        'Посмотрите, как прошла ваша неделя  в *""Просто спросить""*\n'
        "Закрыто заявок - *$tickets_closed*\n"
        "В работе *$tickets_in_work* заявок  за неделю\n\n"
        "Истекает срок у *$tickets_expiring заявок*\n"
        "У *$tickets_expired* заявок срок истек\n\n"
        "Открыть [Trello](https://trello.com)\n\n"
        "Мы рады работать в одной команде :)\n"
        "*Так держать!*"
    )
    alias_dict = dict(
        tickets_closed="last_week_user_tickets_closed",
        tickets_in_work="last_week_user_tickets_in_work",
        tickets_expiring="last_week_user_tickets_expiring",
        tickets_expired="last_week_user_tickets_expired",
    )
    await send_statistics(
        context,
        template_message,
        alias_dict,
        week_statistics,
    )


async def monthly_stat_job(context: CallbackContext) -> None:
    """
    Send monthly statistics on the number of successfully
    closed requests.
    Only if the user had requests
    """
    mont_statistics = await APIService().get_month_stat()
    template_message = Template(
        "Это был отличный месяц!\n"
        'Посмотрите, как он прошел в *""Просто спросить""* 🔥\n\n'
        "Количество закрытых заявок - *$tickets_closed*\n"
        "Рейтинг - *$rating*\n"
        "Среднее время ответа - *$ticket_resolve_avg_time*\n\n"
        "Открыть [Trello](https://trello.com)\n\n"
        "Мы рады работать в одной команде :)\n"
        "*Так держать!*"
    )
    alias_dict = dict(
        tickets_closed="user_tickets_closed",
        rating="user_rating",
        ticket_resolve_avg_time="user_ticket_resolve_avg_time",
    )
    await send_statistics(
        context,
        template_message,
        alias_dict,
        mont_statistics,
    )


async def monthly_bill_reminder_job(context: CallbackContext) -> None:
    """
    Send monthly reminder about the receipt formation during payment
    Only for self-employed users
    """
    bill_stat = await APIService().get_bill()
    user_list = bill_stat.telegram_ids
    for telegram_id in user_list:
        context.job_queue.run_once(daily_bill_remind_job, when=timedelta(seconds=1), user_id=telegram_id)


async def daily_bill_remind_job(context: CallbackContext) -> None:
    """
    Send message every day until delete job from JobQueue
    :param context:
    :return:
    """
    job = context.job
    message = "Вам необходимо сформировать чек"
    bill_done_button = InlineKeyboardButton(text="✅ Уже отправил(а)", callback_data=CALLBACK_DONE_BILL_COMMAND)
    bill_skip_button = InlineKeyboardButton(text="🕑 Скоро отправлю", callback_data=CALLBACK_SKIP_BILL_COMMAND)
    menu = InlineKeyboardMarkup([[repeat_after_one_hour_button], [bill_done_button], [bill_skip_button]])
    await send_message(chat_id=job.user_id, text=message, reply_markup=menu, context=context)
    send_time = config.MONTHLY_RECEIPT_REMINDER_TIME
    # user_utc = context.user_data.get("UTC")
    # Не смог понять, в каком виде хранятся данные о часовом поясе юзера. Здесь надо переопределить информацию о
    # времени отправки сообщения
    # if user_utc:
    #     send_time += user_utc

    context.job_queue.run_daily(
        daily_bill_remind_job,
        time=send_time,
        user_id=job.user_id,
        name=f"send_{job.user_id}_bill_until_complete",
    )
