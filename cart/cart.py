from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from store.models import Product

class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # salva um carrinho vazio na sessao
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, action=None):
        """
        Adiciona um produto ao carrinho, ou atualiza sua quantidade.
        """
        id = product.id
        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                "userid": self.request.user.id,
                "product_id": id,
                "name": product.name,
                "quantity": 1,
                "price": str(product.price),
                "image": product.image.url,
            }
        else:
            # newItem=True
            for k, v in self.cart.items():
                if k == str(product.id):
                    v["quantity"] = v["quantity"] + 1
                    # newItem=False
                    self.save()
                    break
        self.save()

    def save(self):
        # atualiza a sessao do carrinho
        self.session[settings.CART_SESSION_ID] = self.cart
        # marca a sessao como modificado para ter certeza que esta salvo.
        self.session.modified = True

    def remove(self, product):
        """
        Remove um produto do carrinho
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        for k, v in self.cart.items():
            if k == str(product.id):
                v["quantity"] = v["quantity"] - 1
                if v["quantity"] >= 1:
                    return redirect("cart_detail")
                else:
                    self.remove(product)
                self.save()
                break
            else:
                print("Something's Wrong")

    def clear(self):
        # limpa o carrinho
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
