# tracker/views.py
import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stock, HistoricalData, Portfolio, TradeLog
from django.db.models import F
import datetime

ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key'

@api_view(['GET'])
def fetch_realtime_data(request):
    stock_symbols = request.GET.getlist('symbols')
    data = {}
    for symbol in stock_symbols:
        url = f'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': '1min',
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data[symbol] = response.json()
    return Response(data)

@api_view(['GET'])
def get_portfolio_value(request):
    portfolio = Portfolio.objects.annotate(stock_price=F('stock__close_price'))
    value = sum(item.stock_price * item.quantity for item in portfolio)
    return Response({'portfolio_value': value})

@api_view(['POST'])
def simulate_trade(request):
    data = request.data
    action = data['action']  # BUY or SELL
    stock_symbol = data['symbol']
    quantity = int(data['quantity'])
    price = float(data['price'])

    # Fetch or create stock entry
    stock, _ = Stock.objects.get_or_create(symbol=stock_symbol)
    portfolio, _ = Portfolio.objects.get_or_create(stock=stock, user='default_user')

    if action == 'BUY':
        portfolio.quantity += quantity
    elif action == 'SELL':
        portfolio.quantity -= quantity

    # Save portfolio update
    portfolio.save()

    # Log trade
    TradeLog.objects.create(
        stock=stock,
        action=action,
        quantity=quantity,
        price=price,
        date=datetime.date.today(),
        balance_after_trade=portfolio.quantity * price
    )
    return Response({'status': 'Trade simulated successfully!'})
