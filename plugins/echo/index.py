
from core.tomorin import on_event, on_activator, new_api, admin_list


@on_activator.command('echo')
def echo(session):
    """
    回声
    复读你的话
    """
    print(session.data)
    if session.command.args and session.user.id in admin_list:
        # session.message_create(content=session.command.text)
        session.send(session.command.text)

#
# @on_activator.timer('00:44')
# def clock1():
#     print('clock1')
#     new_api_1 = new_api('red', '211134009')
#     new_api_1.message_create(channel_id='666808414', content='睡醒了')
#
#
# @on_activator.interval(5)
# def miaow():
#     print('喵喵喵')