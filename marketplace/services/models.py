class NaturalKeyModel:
    """Модель, добавляющая функционал получения натурального ключа объекта."""

    def set_values(self, data: dict):
        """Установка значений атрибутов экземпляра из словаря data, где
        ключи - это его атрибуты.

        :param data: Словарь значений для установки.
        :return: Текущий экземпляр объекта.
        """
        for field_name, value in data.items():
            setattr(self, field_name, value)
        return self

    def natural_key(self):
        """Базовый метод получения натурального ключа модели. Переопределяется
        в моделях-наследниках."""
        raise NotImplementedError('Method is not implemented')
