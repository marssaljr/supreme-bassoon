def cart_total_amount(request):
    if request.user.is_authenticated:
        total_bill = 0.0
        for k, v in request.session["cart"].items():
            total_bill = total_bill + (float(v["price"]) * v["quantity"])
        return {"cart_total_amount": total_bill}
    else:
        return {"cart_total_amount": 0}
