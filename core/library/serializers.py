from rest_framework import serializers
from .models import Book, BorrowRequest

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = '__all__'

    def validate(self, data):
        if data['borrow_start_date'] >= data['borrow_end_date']:
            raise serializers.ValidationError("The borrow start date must be before the end date.")
        return data

class BorrowRequestDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = BorrowRequest
        fields = '__all__'