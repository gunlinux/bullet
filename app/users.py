from typing import ClassVar


class Users:
    data: ClassVar[str] = ''

    def __init__(self) -> None:
        if not self.data:
            with open('app/data/users.json', 'r') as f:
                Users.data = f.read()
            print(f'load self.data {self.data}')
 
    @classmethod
    def get_users(cls) -> str:
        return cls.data
