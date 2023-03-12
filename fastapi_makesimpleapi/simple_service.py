class SimpleService:
    def __init__(self):
        self.service_name = "Simple Service"

    def get_name(self) -> str:
        return self.service_name

    def get_dict(self, key: str, value: int) -> dict:
        return {key: value}
