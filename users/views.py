from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from Documents.models import Document
from Documents.permissions import Moderators
from users.serializers import PaymentsSerializer, RegisterSerializer
from users.services import create_price, create_session


class RegisterCreateAPIView(generics.CreateAPIView):
    """
    The registration view
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class MyTokenObtainPairView(TokenObtainPairView, TokenViewBase):
    """
    Overriding the TokenObtainPairView class to allow access to everyone
    """

    permission_classes = [AllowAny]


class PaymentsViewSet(viewsets.ModelViewSet):
    """
    Контроллер платежей с фильтрацией и сортировкой
    """

    serializer_class = PaymentsSerializer
    queryset = Document.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("pay_date",)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        price = create_price(int(payment.payment_amount))

        session_id, payment_link = create_session(price)
        payment.link = payment_link
        payment.session_id = session_id
        document = Document.objects.get(id=payment.paid_document.id)
        print(document)
        document.is_paid = True
        document.save()
        print(document.is_paid)
        payment.save()

    def get_permissions(self):
        """
        Method of providing access rights
        """

        if self.request.method in ("GET", "POST"):
            permission_classes = [Moderators]
        else:
            return False
        return [permission() for permission in permission_classes]
