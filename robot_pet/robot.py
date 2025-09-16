class Robot:
    robot_function = {}

    def setup(self):
        print("setup up a robot")

    def listen(self):
        print("list to user")
        return ""

    def speak(self, text):
        print('People 父类中的 say() 方法。')

    def wakeup(self):
        print("this robot has waken up")

    def sleep(self):
        print("this robot has been put to sleep")

    def process_function_call(self, function_name, function_args):
        print(f'process function call, {function_name}, {function_args}')
        func = self.robot_function[function_name]["implementation"]

        if function_name == "play_music":
            function_args['chatbot'] = self
        res = func(function_args)

        return res

    def cleanup(self):
        print("clean up a robot")

    def get_functions(self):
        functions = []
        for func_name, func_details in self.robot_function.items():
            functions.append(func_details["documentation"])
        return functions