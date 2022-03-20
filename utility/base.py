import uuid
import os


class BaseUtils:

    def get_file_extension(
        self,
        file_name: str,
    ) -> str:
        return os.path.splitext(file_name)[1]

    def generate_unique_name(self, file_name: str) -> str:
        file_extension = self.get_file_extension(file_name)
        file_name = self.get_file_name(file_name)
        return str(file_name + str(uuid.uuid4().hex) + file_extension).lower()

    def get_file_name(self, file_: str) -> str:
        return os.path.splitext(file_)[0]

    def change_suffix(self, filename, extension="png"):
        return self.get_file_name(filename) + "." + extension


base_utils = BaseUtils()
