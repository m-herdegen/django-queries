from .models import Product 
from django.db.models import Q, Max, Avg
from django.db.models.functions import Length

class ProductCrud:
    @classmethod
    def get_all_products(cls):
       return Product.objects.all() 

    @classmethod
    def find_by_model(cls, model):
        return Product.objects.get(model = model)

    @classmethod 
    def last_record(cls):
        return Product.objects.latest('id')

    @classmethod 
    def by_rating(cls, rating):
        return Product.objects.filter(rating = rating)

    @classmethod 
    def by_rating_range(cls, low, high):
        return Product.objects.filter(rating__range = (low, high))

    @classmethod 
    def by_rating_and_color(cls, rating, color):
        return Product.objects.filter(rating = rating, color = color)

    @classmethod
    def by_rating_or_color(cls, rating, color):
        return Product.objects.filter(Q(rating = rating) | Q(color = color))

    @classmethod 
    def no_color_count(cls):
        return Product.objects.filter(color__isnull = True).count()

    @classmethod 
    def below_price_or_above_rating(cls, price, rating):
        return Product.objects.filter(Q(price_cents__lte = price) | Q(rating__gte = rating))

    @classmethod 
    def ordered_by_category_alphabetical_order_and_then_price_descending(cls):
        return Product.objects.order_by('category', '-price_cents')

    @classmethod
    def products_by_manufacturer_with_name_like(cls, manufacturer):
        return Product.objects.filter(manufacturer__icontains=manufacturer)

    @classmethod 
    def manufacturer_names_for_query(cls, string):
        man_list = []
        for item in Product.objects.filter(manufacturer__icontains=string).values('manufacturer'):
            man_list.append(item['manufacturer'])
        return man_list

    @classmethod 
    def not_in_a_category(cls, string):
        return Product.objects.exclude(category__contains=string)

    @classmethod 
    def limited_not_in_a_category(cls, string, num):
        return Product.objects.exclude(category__contains=string)[:num]

    @classmethod
    def category_manufacturers(cls, category):
        man_list = []
        for item in Product.objects.filter(category__icontains=category).values('manufacturer'):
            man_list.append(item['manufacturer'])
        return man_list

    @classmethod 
    def average_category_rating(cls, category):
        return Product.objects.filter(category = category).aggregate(Avg("rating")) 

    @classmethod 
    def greatest_price(cls):
        return Product.objects.aggregate(Max('price_cents'))

    @classmethod 
    def longest_model_name(cls):
        return Product.objects.all().annotate(field_len=Length('model')).order_by('-field_len')[0].id


    @classmethod 
    def ordered_by_model_length(cls):
        return Product.objects.all().annotate(field_len=Length('model')).order_by('field_len')
        
