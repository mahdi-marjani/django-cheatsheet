from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
import requests
import json
from django.utils import timezone
from django.contrib import messages

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})

class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')

class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')

class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)

MERCHANT = '952f160c-0747-4f49-8b44-840d3f0ac8bf'
ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"
description = "shop description"  # Required
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "description": description,
            "callback_url": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
            print('-'*10)
            print(3)
            print(response.text)
            print('-'*10)

            if response.status_code == 200:
                response = response.json()
                if response['data']['code'] == 100:
                    return redirect(ZP_API_STARTPAY + str(response['data']['authority']))
                else:
                    err_data = {'status': False, 'code': str(response['data']['code'])}
                    return HttpResponse(f'err: {err_data}')
            return HttpResponse(f'status code: {response.status_code}')
        
        except requests.exceptions.Timeout:
            err_data = {'status': False, 'code': 'timeout'}
            return HttpResponse(f'err: {err_data}')
        except requests.exceptions.ConnectionError:
            err_data = {'status': False, 'code': 'connection error'}
            return HttpResponse(f'err: {err_data}')

class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "authority": request.GET['Authority'],
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)
        print('-'*10)
        print(4)
        print(response.text)
        print('-'*10)
        if response.status_code == 200:
            response = response.json()
            if response['data']['code'] == 100:
                order.paid = True
                order.save()
                data = {'status': True, 'RefID': response['data']['ref_id']}
                return HttpResponse(f'data: {data}')
            else:
                data = {'status': False, 'code': str(response['data']['code'])}
                return HttpResponse(f'data: {data}')
        return HttpResponse(response)
    
class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    def post(self, request, order_id):
        now = timezone.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon does not exist', 'danger')
                return redirect('orders:order_detail', order_id)
            
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)