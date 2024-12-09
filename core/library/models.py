from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    borrow_start_date = models.DateField()
    borrow_end_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'borrow_start_date', 'borrow_end_date'],
                name='unique_borrow_period'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"
