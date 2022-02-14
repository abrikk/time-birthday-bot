from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command


async def show_all_tasks(message: types.Message, scheduler):
    print(scheduler.get_jobs())
    list_of_jobs = scheduler.get_jobs()
    for job in scheduler.get_jobs():
        print("name: %s, trigger: %s, next run: %s, handler: %s" % (
            job.name, job.trigger, job.next_run_time, job.func))

    if list_of_jobs is not None:
        text = "\n\n".join("name: {name}, trigger: {trigger}, next run: {next_run}".
                                format(name=job.name, trigger=job.trigger,
                                       next_run=job.next_run_time)
                                for job in list_of_jobs)
    else:
        text = "Jobstore is empty."
    await message.answer(text)


def register_show_all_tasks(dp: Dispatcher):
    dp.register_message_handler(show_all_tasks, Command("show_tasks"))
