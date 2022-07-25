from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from dotenv import load_dotenv
import os
import requests
from requests_oauthlib import OAuth1


load_dotenv()

auth = OAuth1(os.environ['API_KEY'] , os.environ['SECRET'])

data = {
   "cat1": [
    {
      "id": 1,
      "name": "Cheap Coffee",
      "price": "$2.99",
      "priceCents": "299",
      "filename": "coffee.png",
      "description": "Gives you energy, but be careful not to drink too much",
      "stock": 1
    },
    {
      "id": 2,
      "name": "Mountain Dew",
      "price": "$2.99",
      "priceCents": "299",
      "filename": "dew.png",
      "description": "Nectar of The Gods",
      "stock": 2
    },
    {
      "id": 3,
      "name": "Doritos", 
      "price": "$2.99",
      "priceCents": "299",
      "filename": "doritos.png",
      "description": "",
      "stock": 2
    }
  ], 
  "cat2": [
    {
      "id": 4,
      "name": "Hoodie",
      "price": "$59.99",
      "priceCents": "5999",
      "filename": "hoodie.png",
      "description": "Stay warm with this hoodie",
      "stock": 3
    },
    {
      "id": 5,
      "name": "New Balance Sneakers",
      "price": "$109.99",
      "priceCents": "10999",
      "filename": "sneakers.png",
      "description": "best sneakers for walking around in",
      "stock": 3
    },
    {
      "id": 6,
      "name": "Headphones",
      "price": "$109.99",
      "priceCents": "10999",
      "filename": "headphones.png",
      "description": "Noise cancelling, and they count as a fashion accessory",
      "stock": 3
    }
  ],
  "cat3": [
    {
      "id": 7,
      "name": "Soylent",
      "price": "$4.99",
      "priceCents": "499",
      "filename": "soylent.png",
      "description": "This is what peak performance looks like",
      "stock": 3
    },
    {
      "id": 8,
      "name": "Carpal Tunnel Aid",
      "filename": "carpal.png",
      "price": "$0.99",
      "priceCents": "99",
      "description": "So you failed your Code Platoon assessment and now you're doing 2 assessments back to back? Try this!",
      "stock": 0
    },
    {
      "id": 9,
      "name": "Coconut Oil",
      "filename": "oil.png",
      "price": "$9.99",
      "priceCents": "999",
      "description": "Apply to fingers for fast coding abilities",
      "stock": 0
    }
  ]
};

user_cart = []

def home(request):
    return render(request, 'ecomm_app/home.html')

def cat1(request):
    category_data = { 'data': data['cat1']}
    return render(request, 'ecomm_app/cat1.html', context=category_data)

def cat2(request):
    category_data = { "data": data['cat2'] }
    return render(request, 'ecomm_app/cat2.html', context=category_data)

def cat3(request):
    category_data= { "data": data['cat3'] }
    return render(request, 'ecomm_app/cat3.html', context=category_data)

@csrf_exempt
def cart(request):
    if(request.method == 'POST'):
        body = json.loads(request.body)
        user_cart.append(body)
        return JsonResponse({})
    if(request.method == 'GET'):
        if(len(user_cart) > 0):
            print(user_cart)
            total = 0
            for item in user_cart:
                if(bool(item)):
                    item['subtotal'] = (item['priceCents'] * item['quantity'])/100
                    total += item['priceCents'] * item['quantity']
                else:
                    messages.add_message(request, messages.ERROR, 'please select a quantity')
                    return redirect(request.META.get('HTTP_REFERER'))
            return render(request, 'ecomm_app/cart.html', context={ 'user_cart': user_cart, 'cart_total': total/100 })
        else:
            return render(request, 'ecomm_app/cart.html')
sendProduct = {}

@csrf_exempt
def search(request):
    context = { 'product' : None }
    queriedProduct = (request.GET.get('query'))
    for category in data:
        for product in data[category]:
            if product['name'] == queriedProduct:
                sendProduct = product
                return JsonResponse(sendProduct)
    if(queriedProduct):
        endpoint = f"http://api.thenounproject.com/icon/{queriedProduct}"
        API_response = requests.get(endpoint, auth=auth)
        JSON_API_response = json.loads(API_response.content)
        image_url = JSON_API_response['icon']['preview_url']
        print(image_url)
        return(JsonResponse({ 'url': image_url }))
    return render(request, 'ecomm_app/search.html', context)
