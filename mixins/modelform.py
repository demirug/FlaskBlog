from flask import request


class FormModelNotSet(Exception):
    pass


class ModelFormMixin:
    # Required empty copy of model instance for some actions
    model = None

    def __init__(self, instance=None, *args, **kwargs):
        """ Filling form fields from model data if fields names same """

        if not self.model:
            raise FormModelNotSet("Set `model` variable in form")

        super().__init__(*args, **kwargs)
        self.__instance = instance
        # Fill form with instance data if method is POST and instance exists
        if instance:
            if request.method == "GET":
                for field in self._fields:
                    if hasattr(instance, field):
                        getattr(self, field).data = getattr(instance, field)

        else:
            self.__instance = self.model()

    def get_instance(self):
        return self.__instance

    def save(self):
        """ Save form data to instance model if files name same """
        for field in self._fields:
            if hasattr(self.__instance, field):
                setattr(self.__instance, field, getattr(self, field).data)

        return self.__instance
