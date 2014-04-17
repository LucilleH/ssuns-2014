from django.db import models

from mcmun.constants import MAX_NUM_DELEGATES
from mcmun.models import RegisteredSchool


SIZE_CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XX', 'XXL'),
)


class PriceField(models.DecimalField):
    description = 'Exactly what it says on the tin'

    def __init__(self, *args, **kwargs):
        kwargs['decimal_places'] = 2
        kwargs['max_digits'] = 5
        models.DecimalField.__init__(self, *args, **kwargs)


class QuantityField(models.IntegerField):
    description = 'Between 1 and MAX_NUM_DELEGATES'

    def __init__(self, *args, **kwargs):
        kwargs['default'] = 1
        kwargs['choices'] = ((n, n) for n in xrange(1, MAX_NUM_DELEGATES + 1))
        models.IntegerField.__init__(self, *args, **kwargs)


class Item(models.Model):
    name = models.CharField(max_length=50)
    online_price = PriceField()
    retail_price = PriceField()
    description = models.TextField()
    slug = models.SlugField()
    is_limited = models.BooleanField()
    # This is a lot less fun than the abstractified monstrosity I was going to
    # go with but honestly, it's probably easier to work with in the long run.
    has_size = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Bundle(models.Model):
    """A collection of items."""
    name = models.CharField(max_length=50)
    online_price = PriceField()
    retail_price = PriceField()
    description = models.TextField()
    slug = models.SlugField()
    items = models.ManyToManyField(Item)

    def __unicode__(self):
        return self.name

    def get_amount_saved(self):
        """I could have just made this a field whose value must be input by the
        user, but where's the fun in that?"""
        expected_price = sum(item.online_price for item in self.items.all())
        return expected_price - self.online_price

    def has_size(self):
        return self.items.filter(has_size=True).exists()


class ItemOrder(models.Model):
    school = models.ForeignKey(RegisteredSchool)
    item = models.ForeignKey(Item, related_name='orders')
    quantity = QuantityField()
    comment = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, null=True,
                            blank=True)
    bundle_order = models.ForeignKey('BundleOrder', null=True, blank=True,
                                     related_name='item_orders')


    class Meta:
        ordering = ('item', 'school')

    def __unicode__(self):
        return '%s x %d - %s' % (self.item, self.quantity, self.school)

    def get_description(self):
        """Used by the __unicode__ method on BundleOrder."""
        return '%s (%s)' % (self.name, self.size) if self.size else self.name

    def total_cost(self):
        if self.bundle_order is not None:
            cost = self.bundle_order.bundle.online_price * self.quantity
            return '%s (part of %s)' % (cost, self.bundle_order.bundle)
        else:
            cost = self.item.online_price * self.quantity
            return '%s (%s per item)' % (cost, self.item.online_price)

    def total_owed_by_school(self):
        return self.school.get_merch_total_owed()

    def is_finalised(self):
        return self.school.merch_order_final


class BundleOrder(models.Model):
    """Creating a BundleOrder also creates the necessary ItemOrders."""
    school = models.ForeignKey(RegisteredSchool)
    bundle = models.ForeignKey(Bundle, related_name='orders')
    quantity = QuantityField()
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('bundle', 'school')

    def __unicode__(self):
        return self.bundle.name

    def get_size_display(self):
        for item_order in self.item_orders.filter(item__has_size=True):
            return item_order.get_size_display()

    def create_item_orders(self, size):
        for item in self.bundle.items.all():
            self.item_orders.create(school=self.school, item=item,
                                    quantity=self.quantity, size=size)
