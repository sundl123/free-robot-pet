import erniebot

def get_current_temperature(location: str, unit: str) -> dict:
    return {'temperature': 25, 'unit': '摄氏度'}

functions = [
    {
        'name': 'get_current_temperature',
        'description': "获取指定城市的气温",
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': "城市名称",
                },
                'unit': {
                    'type': 'string',
                    'enum': [
                        '摄氏度',
                        '华氏度',
                    ],
                },
            },
            'required': [
                'location',
                'unit',
            ],
        },
        'responses': {
            'type': 'object',
            'properties': {
                'temperature': {
                    'type': 'integer',
                    'description': "城市气温",
                },
                'unit': {
                    'type': 'string',
                    'enum': [
                        '摄氏度',
                        '华氏度',
                    ],
                },
            },
        },
    },
]

erniebot.api_type = 'aistudio'
erniebot.access_token = '989b45bce1ef5826310826a3a02c2d554725caa0'

messages = [
    {
        'role': 'user',
        'content': "深圳市今天气温如何？"
    }
]

response = erniebot.ChatCompletion.create(
    model='ernie-bot',
    messages=messages,
    functions=functions
)
print(response)
assert hasattr(response, 'function_call')
function_call = response.function_call
print(function_call)


import json

name2function = {'get_current_temperature': get_current_temperature}
func = name2function[function_call['name']]
args = json.loads(function_call['arguments'])
res = func(location=args['location'], unit=args['unit'])


messages.append(
    {
        'role': 'assistant',
        'content': None,
        'function_call': function_call
    }
)
messages.append(
    {
        'role': 'function',
        'name': function_call['name'],
        'content': json.dumps(res, ensure_ascii=False)
    }
)
response = erniebot.ChatCompletion.create(
    model='ernie-bot',
    messages=messages,
)
print(response.result)