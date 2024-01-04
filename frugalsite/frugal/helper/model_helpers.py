from frugal.models import Favorite, Product
from django.utils import timezone
from .meijer import meijer_product_id_lookup
from .kroger import kroger_product_id_lookup
from .walmart import walmart_product_id_lookup


def save_to_favorite_and_products(request) -> Favorite:
    prices = list()

    favorite_name = request.POST["favorite-name"]

    favorite = Favorite(
        user_id=request.user.id,
        name=favorite_name,
        date_created=timezone.now(),
        date_updated=timezone.now(),
    )

    favorite.save()

    if request.POST.get("meijer"):
        data = eval(request.POST["meijer"])
        product = Product(
            user_id=request.user.id,
            favorite=favorite,
            store_name=data["store"],
            name=data["name"],
            store_id=data["store_id"],
            imgage_url=data["image_url"],
            price=float(data["price"]),
            date_created=timezone.now(),
            date_updated=timezone.now(),
        )

        if "sale_price" in data:
            product.set_sale_price(float(data["sale_price"]))

        product.save()

        prices.append(float(data["price"]))

    if request.POST.get("kroger"):
        data = eval(request.POST["kroger"])
        product = Product(
            user_id=request.user.id,
            favorite=favorite,
            store_name=data["store"],
            name=data["name"],
            store_id=data["store_id"],
            imgage_url=data["image_url"],
            price=float(data["price"]),
            date_created=timezone.now(),
            date_updated=timezone.now(),
        )

        if "sale_price" in data:
            product.set_sale_price(float(data["sale_price"]))

        product.save()

        prices.append(float(data["price"]))

    if request.POST.get("walmart"):
        data = eval(request.POST["walmart"])
        product = Product(
            user_id=request.user.id,
            favorite=favorite,
            store_name=data["store"],
            name=data["name"],
            store_id=data["store_id"],
            imgage_url=data["image_url"],
            price=float(data["price"]),
            date_created=timezone.now(),
            date_updated=timezone.now(),
        )

        if "sale_price" in data:
            product.set_sale_price(float(data["sale_price"]))

        product.save()

        prices.append(float(data["price"]))

    favorite.set_average_price(prices=prices)

    favorite.save()

    return favorite


def update_product_prices(favorite, products):
    prices = list()

    for product in products:
        match product.store_name:
            case "meijer":
                current_prices = meijer_product_id_lookup(product_id=product.store_id)
                if "price" in current_prices:
                    product.set_price(current_prices["price"])
                    prices.append(current_prices["price"])
                if "sale_price" in current_prices:
                    product.set_sale_price(current_prices["sale_price"])
                product.save()
            case "kroger":
                current_prices = kroger_product_id_lookup(product_id=product.store_id)
                if "price" in current_prices:
                    product.set_price(current_prices["price"])
                    prices.append(current_prices["price"])
                if "sale_price" in current_prices:
                    product.set_sale_price(current_prices["sale_price"])
                product.save()
            case "walmart":
                current_prices = walmart_product_id_lookup(product_id=product.store_id)
                if "price" in current_prices:
                    product.set_price(current_prices["price"])
                    prices.append(current_prices["price"])
                if "sale_price" in current_prices:
                    product.set_sale_price(current_prices["sale_price"])
                product.save()

    favorite.set_average_price(prices)
    favorite.save()
