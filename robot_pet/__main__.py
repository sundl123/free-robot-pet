from chatbot import start_chatbot
import sys
import os


def add_python_pkgs():
    top_dir = os.path.dirname(os.path.abspath(__file__))

    python_pkg_path = os.path.join(top_dir, "wakeup")
    sys.path.append(python_pkg_path)

    python_pkg_path = os.path.join(top_dir, "vision")
    sys.path.append(python_pkg_path)

    python_pkg_path = os.path.join(top_dir, "../CLBROBOT")
    sys.path.append(python_pkg_path)


if __name__ == '__main__':
    add_python_pkgs()
    start_chatbot()