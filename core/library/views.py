from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book, BorrowRequest
from .serializers import BookSerializer, BorrowRequestSerializer, BorrowRequestDetailSerializer



class BookAPIView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BorrowRequestAPIView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get(self, request):
        if request.user.is_staff:
            borrow_requests = BorrowRequest.objects.all()
            serializer = BorrowRequestDetailSerializer(borrow_requests, many=True)
        else:
            borrow_requests = BorrowRequest.objects.filter(user=request.user)
            serializer = BorrowRequestSerializer(borrow_requests, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.validated_data.get('book')
            try:
                book = Book.objects.get(id=id)
            except Book.DoesNotExist:
                return Response({"error": "The specified book does not exist."}, status=status.HTTP_404_NOT_FOUND)

            start_date = serializer.validated_data.get('borrow_start_date')
            end_date = serializer.validated_data.get('borrow_end_date')

            overlapping_requests = BorrowRequest.objects.filter(
                book=book,
                borrow_end_date__gte=start_date,
                borrow_start_date__lte=end_date,
                status='approved'
            )

            if overlapping_requests.exists():
                return Response({"error": "The book is already borrowed during the specified period."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            borrow_request = BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            return Response({"error": "Borrow request not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff:
            serializer = BorrowRequestSerializer(borrow_request, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Only admin can modify borrow requests."}, status=status.HTTP_403_FORBIDDEN)

