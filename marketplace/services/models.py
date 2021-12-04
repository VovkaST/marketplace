class NaturalKeyModel:
    def set_values(self, data):
        for field_name, value in data.items():
            setattr(self, field_name, value)
        return self

    def natural_key(self):
        raise NotImplementedError('Method is not implemented')
