from .serializers import (AUserSerializer, AccountSerializer,
                          ActionSerializer, TransactionSerializer,
                          CategorySerializer)
from .models import AUser, Account, Action, Transaction, Category
from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import random
from datetime import timezone, timedelta
from django.core.mail import send_mail
from db import email
from django.template.loader import render_to_string



class AUserList(generics.ListCreateAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = AUser.objects.all()
    serializer_class = AUserSerializer

    def get_queryset(self):
        """Возвращать объект только для текущего аутентифицированного
           пользователя"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создать новый атрибут"""
        serializer.save(user=self.request.user)


class AUserDetail(generics.RetrieveUpdateAPIView):

    serializer_class = AUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = AUser.objects.all()

    def get_queryset(self):
        """Возвращать объект только для текущего аутентифицированного
           пользователя"""
        return self.queryset.filter(user=self.request.user)


class AUserDetail2(viewsets.ModelViewSet):

    serializer_class = AUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = AUser.objects.all()

    def perform_create(self, serializer):
        """Создать нового клиента"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Возвращать объект только для текущего аутентифицированного
           пользователя"""
        return self.queryset.filter(user=self.request.user)


class AUserDetail3(generics.RetrieveUpdateAPIView):

    serializer_class = AUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = AUser.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class AccountViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        """Создать новый аккаунт"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Возвращать объект только для текущего аутентифицированного
           пользователя"""
        return self.queryset.filter(user=self.request.user)


class ActionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Action.objects.all()

    def get_queryset(self):
        """Возвращать объект только для текущего аутентифицированного
           пользователя"""
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # проверить, принадлежит ли запрошенная учетная запись пользователю

        try:
            account = Account.objects.filter(
                user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)
            content = {'error': 'Нет такой учетной записи'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

class CategorySerializer(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()

    def get_queryset(self):
        """Возвращать объект только для текущего аутентифицированного
           пользователя"""
        return self.queryset.filter(name=self.request.user)

    def perform_create(self, serializer):
        """Создать новый атрибут"""
        serializer.save(name=self.request)


class TransactionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin):
    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            account = Account.objects.filter(
                user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)
            content = {'error': 'Нет такой учетной записи'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        try:
            Transaction.make_transaction(**serializer.validated_data)
        except ValueError:
            content = {'error': 'Недостаточно средств'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_queryset(self):
        """Возвращать объект только для текущего аутентифицированного
           пользователя"""
        # получить учетную запись пользователя
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)

# emails = email
# def send(request):
#     me = 'Название компании <{}>'.format(settings.EMAIL_HOST_USER)
#     subject = 'Тестовое письмо'
#
#     attachments = {
#         'Тестовое вложение.pdf': join(settings.MEDIA_ROOT,
#         'test_attachment.pdf')
#     }
#
#     now = timezone.now()
#     delta_sec = -70  # Нужно, чтобы первое письмо было отправлено сразу же
#
#     for email in emails:
#         delta_sec += random.randint(86300, 86500)
#         scheduled_time = now + timedelta(seconds=delta_sec)
#
#         message = render_to_string('my_app/email.html',
#         {'email': email, 'some_var': 'xxx'})
#         headers = {'To': 'Получатель письма от компании <{}>'.format(email)}
#         send(email, me, subject=subject,
#              message=message, html_message=message,
#              scheduled_time=scheduled_time, headers=headers,
#              attachments=attachments)

