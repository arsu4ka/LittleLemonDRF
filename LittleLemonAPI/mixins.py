from rest_framework.request import Request


class SerializerByMethodMixin:
    serializer_class_by_method = dict()
    request = Request

    def get_serializer_class(self):
        if self.request.method.lower() in self.serializer_class_by_method:
            return self.serializer_class_by_method[self.request.method.lower()]
        else:
            return self.serializer_class_by_method['get']

