from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabaled"),
    ("rejected", "Rejected"),
    ("in_review", "In_Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

def user_directory_image(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length = 10, max_length=20, prefix="cat", alphabet = "abcdef12345")
    title = models.CharField(max_length=100, default="Fruits")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)
    
    def __str__(self) -> str:
        return self.title
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length = 10, max_length=20, prefix="ven", alphabet = "abcdef12345")
    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to=user_directory_image, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_image, default="vendor.jpg")
    description = RichTextUploadingField(max_length=100, default="I'm the Best Vendor!")
    address = models.CharField(max_length=100, default="123 Main Street London!")
    date = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=100, default="+123 (456) 789")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendors"
    
    def vendor_image(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)
    
    def __str__(self) -> str:
        return self.title
    

    pass
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length = 10, max_length=20, alphabet = "abcdef12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null = True, related_name="vendor")
    

    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(upload_to=user_directory_image, default="product.jpg")
    description = RichTextUploadingField(max_length=10000, default="This is the Vendor!")

    price = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=999999999, decimal_places=2, default="2.99")

    specifications = RichTextUploadingField(null=True, blank=True)
    type = models.CharField(max_length=100, default="Organic", null=True, blank=True) 
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True) 
    life = models.CharField(max_length=100, default="100 Days", null=True, blank=True) 
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    tags = TaggableManager(blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default= False)

    sku = ShortUUIDField(unique=True, length =4, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"
    
    def product_image(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)
    
    def __str__(self) -> str:
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_image", default="product_image.jpg")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"



"""    ********************** CART,ORDER,ORDERITEMS *********************************   """
"""    ********************** CART,ORDER,ORDERITEMS *********************************   """

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices = STATUS_CHOICE, max_length=50, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.CharField(max_length = 100, default = 0)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def cart_order_image(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % self.image.url)
    
    def product_image(self):
        return mark_safe("<img src='/media/%s' width='50' height='50' />" % self.image)
    

"""    **********************ADDRESS REVIEW AND WISHLIST*********************************   """


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) 
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True, related_name="reviews") 
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def _str_(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) 
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True) 
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "WishLists"

    def _str_(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) 
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=1024, default="+123 456 789")
    state = models.CharField(max_length=100, default="NYC")
    city = models.CharField(max_length=100, default="City")
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"    