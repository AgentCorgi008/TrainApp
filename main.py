import pickle
from user_db import UserDB
from main_gui import TrainApp


def main() -> None:
    user = UserDB()
    if user.check_user_exist():
        user.create_default_user()
    app = TrainApp()
    app.run()


if __name__ == "__main__":
    main()
