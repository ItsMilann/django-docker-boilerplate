"""customised response.Response & viewsets.ModelViewSet to fit message, error, code in data"""

from rest_framework import response
from rest_framework import viewsets
from rest_framework import status as code


class Response(response.Response):
    """customised response.Response"""
    def __init__(self, data=None, status=None, error=None, message=None, obj=None):
        super().__init__(data=data, status=status)
        self.data = data
        self.status = status
        self.message = message
        self.error = error or {}
        self.obj = obj
        data = {}
        assert self.status, "missing required parameter, 'status'"
        if self.status >= 200 and self.status < 300:
            data["message"] = self.message or "request success"
        else:
            data["message"] = self.message or "something went wrong"
        data["error"] = self.error
        data["data"] = self.data


class ModelViewSet(viewsets.ModelViewSet):
    """custom model viewset with error and status in data"""
    def create(self, request, *args, **kwargs):
        data, message, status, error = {}, "Something went wrong", 201, {}
        serializer = self.get_serializer(data=request.data)
        obj = super().get_serializer_class()
        if serializer.is_valid():
            self.perform_create(serializer)
            message = f"{obj.Meta.model.verbose_name} created"
            data = serializer.data
        else:
            error = serializer.errors
            try:
                _ = error["non_field_errors"]
            except KeyError:
                error["non_field_errors"] = []
            status = 400
        return Response(data=data, error=error, message=message, obj=obj, status=status)

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        serializer_class = super().get_serializer_class()
        obj = serializer_class
        msg = f"{obj.Meta.model.verbose_name}'s list"
        return Response(data, message=msg, obj=obj, status=code.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        serializer_class = super().get_serializer_class()
        obj = serializer_class
        msg = f"{obj.Meta.model.verbose_name}'s detail"
        return Response(data, message=msg, obj=obj, status=code.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data, message, status, error = {}, "Something went wrong", 201, {}
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        obj = super().get_serializer_class()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            message = f"{obj.Meta.model.verbose_name} updated"
            data = serializer.data
            status = 200
        else:
            error = serializer.errors
            try:
                _ = error["non_field_errors"]
            except KeyError:
                error["non_field_errors"] = []
            status = 400
        return Response(data=data, error=error, message=message, obj=obj, status=status)

    def destroy(self, request, *args, **kwargs):
        data = super().destroy(request, *args, **kwargs).data
        serializer_class = super().get_serializer_class()
        obj = serializer_class
        msg = f"{obj.Meta.model.verbose_name} deleted"
        return Response(data, message=msg, obj=obj, status=200)
