class LoginResult:
    user_id: int
    token: str
    r_token: str

    def __init__(self, user_id: int, token: str, r_token: str) -> None:
        self.user_id = user_id
        self.token = token
        self.r_token = r_token
