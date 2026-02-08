from src.infrastructure.database.repository.user_repo import UserRepository


class UserService:
    def __init__(
            self,
            repo: UserRepository
    ):
        self.repo = repo
