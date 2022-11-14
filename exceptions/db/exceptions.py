from exceptions.exceptions import AppException


class DBDuplicateKeyException(AppException):
    _column: str

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self._set_column_from_message()

    def get_column(self) -> str:
        return self._column

    def _set_column_from_message(self):
        """Extracts key or column name from a MySQL Integrity error string.

        Example: Duplicate entry 'email@gmail.com' for key 'users.email_idx'
        """
        if not self._message:
            raise Exception(
                "Attempted to extract key from error message before message property was set"
            )

        try:
            [_, source] = self._message.split(" for key '")
            [table_name, key] = source.split(".")
            [column, _] = key.split("_")

            self._column = column
        except ValueError:
            raise Exception(
                "Failed to extract key from Duplicate Key Exception. This is most likely because the column key or index name format is incorrect"
            )
