from frugal.models import Favorite, Product
from django.utils import timezone


def favorite_products(request) -> Favorite:
    favorite_name = request.POST["favorite-name"]
    favorite = Favorite(
        user_id=request.user.id,
        favorite_name=favorite_name,
        date_created=timezone.now(),
    )
    favorite.save()

    if request.POST.get("meijer"):
        data = eval(request.POST["meijer"])
        product = Product(
            user_id=request.user.id,
            favorite=favorite,
            store_name=data["store"],
            product_name=data["name"],
            product_store_id=int(data["store_id"]),
            product_img_url=data["image_url"],
            product_price=float(data["price"]),
            date_created=timezone.now(),
            date_updated=timezone.now(),
        )

        if "sale_price" in data:
            product.set_product_sale_price(float(data["sale_price"]))

        product.save()
    if request.POST.get("kroger"):
        data = eval(request.POST["kroger"])
        product = Product(
            user_id=request.user.id,
            favorite=favorite,
            store_name=data["store"],
            product_name=data["name"],
            product_store_id=int(data["store_id"]),
            product_img_url=data["image_url"],
            product_price=float(data["price"]),
            date_created=timezone.now(),
            date_updated=timezone.now(),
        )

        if "sale_price" in data:
            product.set_product_sale_price(float(data["sale_price"]))

        product.save()
    if request.POST.get("walmart"):
        data = eval(request.POST["walmart"])
        product = Product(
            user_id=request.user.id,
            favorite=favorite,
            store_name=data["store"],
            product_name=data["name"],
            product_store_id=int(data["store_id"]),
            product_img_url=data["image_url"],
            product_price=float(data["price"]),
            date_created=timezone.now(),
            date_updated=timezone.now(),
        )

        if "sale_price" in data:
            product.set_product_sale_price(float(data["sale_price"]))

        product.save()

    return favorite