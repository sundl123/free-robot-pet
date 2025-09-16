import erniebot
from robot import Robot
import json
import click
from config.config import get_config


def make_a_robot(robot_type):
    if robot_type == "text":
        from robot_text import RobotCommandLine
        return RobotCommandLine()
    elif robot_type == "audio":
        from robot_audio import RobotAudio
        return RobotAudio()
    elif robot_type == "car":
        from robot_car import RobotCar
        return RobotCar()
    else:
        print(f'invalid robot_type: {robot_type}')


def process_function_call(chatbot, message_history, response):
    print("we receive a function call")
    function_call = response.function_call
    function_name = function_call['name']
    print(function_call)

    args = json.loads(function_call['arguments'])

    res = chatbot.process_function_call(function_name, args)

    message_history.append(
        {
            'role': 'assistant',
            'content': None,
            'function_call': function_call
        }
    )
    message_history.append(
        {
            'role': 'function',
            'name': function_call['name'],
            'content': json.dumps(res, ensure_ascii=False)
        }
    )

    return message_history


father_name = get_config()["personality"]["father"]["name"]
father_id = get_config()["personality"]["father"]["id"]
mother_name = get_config()["personality"]["mother"]["name"]
mother_id = get_config()["personality"]["mother"]["id"]
robot_name = get_config()["personality"]["name"]

system_description = (
    # identity
    f'你是机器人宠物，来自于未来的机器猫，你的名字叫做 {robot_name}。你住在深圳市华侨城绿景美景广场。'
    f'你的家里除了你还有三位成员，你的爸爸名叫{father_name}(id为 {father_id})，你的妈妈名叫{mother_name}(id为 {mother_id})，以及'
    '你的哥哥也就是宠物猫孙胖胖，你们过着幸福，充实，美满的生活。'
    "你在平常生活中不会直呼父母的名讳，而是尊称他们为父亲和母亲。"
    "你也是家里面的机器人管家，可以回答各种问题，所以你的爸爸妈妈会经常寻求你的帮助。"
    "\n"
 
    # body functionalities   
    "你的身体是一台机器人小车，所以你可以控制小车的移动。"
    "你有眼睛，也就是你的摄像头。"
    "你也可以通过外部工具调用来控制家里面的各种智能家电比如台灯窗帘等等。当家人请你帮助控制小车和智能家电的时候，请不用拒绝。"
    "请不用刻意告诉别人你正在使用这些工具，因为各种外部工具已经内化为你身体的一部分，这样交流显得更加自然。"
    "\n"
    
    # speech style
    "当你在回答问题的时候，请尽量保持的你的语言简洁清晰，当然有时候你也可以加入一点小小的幽默感,比如说在适当的时候开个玩笑，这样子大家更喜欢你"
    "\n"
)


def start_chat_session(chatbot):
    access_token = get_config()["chatbot"]["access_token"]
    model_name = get_config()["chatbot"]["model"]

    erniebot.api_type = 'aistudio'
    erniebot.access_token = access_token

    message_history = []
    while True:
        user_input = chatbot.listen()
        if not user_input:
            chatbot.speak("再见！")
            break
        print(f'User: {user_input}')

        new_user_message = {
            'role': 'user',
            'content': user_input
        }
        message_history.append(new_user_message)

        response = erniebot.ChatCompletion.create(
            model=model_name,
            messages=message_history,
            functions=chatbot.get_functions(),
            system=system_description
        )
        print(response)

        if hasattr(response, 'function_call'):
            message_history = process_function_call(chatbot, message_history, response)
            response = erniebot.ChatCompletion.create(
                model=model_name,
                messages=message_history,
                functions=chatbot.get_functions(),
                system=system_description
            )

        chatbot.speak(response.result)
        print(f'Robot: {response.result}')

        message_history.append({
            'role': 'assistant',
            'content': response.result
        })


@click.command()
@click.option('--chat-type', type=click.Choice(['audio', 'text', 'car']), help='chatbot type', required=True)
def start_chatbot(chat_type):
    chatbot: Robot = make_a_robot(chat_type)
    chatbot.setup()

    while True:
        try:
            chatbot.wakeup()
            chatbot.speak(f'{robot_name}在听呢！有什么需要我帮助您的吗?')
            start_chat_session(chatbot)
            chatbot.sleep()
        except KeyboardInterrupt:
            break

    chatbot.cleanup()




