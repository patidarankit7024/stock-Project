from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class HistoricalData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.BigIntegerField()

class Portfolio(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.CharField(max_length=100)  # Example user-based portfolio
    created_at = models.DateTimeField(auto_now_add=True)

class TradeLog(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    action = models.CharField(max_length=10)  # BUY or SELL
    quantity = models.IntegerField()
    price = models.FloatField()
    date = models.DateField()
    balance_after_trade = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
