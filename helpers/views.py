from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from helpers.models import QuestionCategory, Callback, PolicyConf
from helpers.serializers import QuestionCategorySerializer, CallbackSerializer, PolicyConfSerializer


class QuestionCategoryListAPIView(ListAPIView):

    serializer_class = QuestionCategorySerializer
    queryset = QuestionCategory.objects.all()


class CallbackCreateAPIView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = CallbackSerializer
    model = Callback


class PolicyConfAPIView(ListAPIView):

    queryset = PolicyConf.objects.all()
    serializer_class = PolicyConfSerializer
    model = PolicyConf
