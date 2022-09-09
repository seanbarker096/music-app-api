from api.db import DB

def test_db():
    print('yooooo')
    assert DB.get_password_from_db() == 'very-secret'


if __name__ == '__main__':
    print('dsadfsafk')
    test_db()
