from functools import wraps


def context_data(context: dict):
    """Декратор для расширения контекста классов-представлений.
       На вход ожидается словарь для расширения словаря контекста
       метода по умолчанию get_context_data.
    """
    def wrapper(cls):
        get_context_data = cls.get_context_data

        @wraps(cls.get_context_data)
        def decorated_get_context_data(self, **kwargs):
            real_context = get_context_data(self, **kwargs)
            real_context.update(context)
            return real_context
        cls.get_context_data = decorated_get_context_data
        return cls
    return wrapper
