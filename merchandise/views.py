from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from merchandise.models import Item, Bundle, ItemOrder, BundleOrder
from merchandise.forms import ItemOrderForm, BundleOrderForm


def main(request):
    bundles = Bundle.objects.all()
    items = Item.objects.all()

    context = {
        'bundles': bundles,
        'items': items,
        'title': 'Merchandise',
    }
    return render(request, 'merchandise.html', context)


@login_required
def order(request):
    # Improve this one day
    schools = request.user.registeredschool_set.filter(is_approved=True)
    if len(schools) == 0:
        return redirect(main) # TODO: show an error message of some sort

    school = schools[0]
    submit = request.GET.get('submit')

    bundles = []
    for bundle in Bundle.objects.all():
        orders = bundle.orders.filter(school=school)
        form = BundleOrderForm(initial={
            'bundle': bundle,
            'school': school,
        })
        bundles.append((bundle, orders, form))

    items = []
    for item in Item.objects.all():
        orders = item.orders.filter(school=school, bundle_order=None)
        form = ItemOrderForm(initial={
            'item': item,
            'school': school,
        })
        items.append((item, orders, form))

    context = {
        'final': school.merch_order_final,
        'submit': submit,
        'bundles': bundles,
        'items': items,
        'title': 'Order merchandise',
    }

    return render(request, 'merchandise-order.html', context)


@login_required
def submit(request):
    if request.method != 'POST':
        return order(request)

    # Improve this one day
    schools = request.user.registeredschool_set.filter(is_approved=True)
    if len(schools) == 0:
        return redirect(main) # TODO: show an error message of some sort

    school = schools[0]

    # Just finalising the order
    if request.POST.get('finalise'):
        school.merch_order_final = True
        school.save()
        return redirect('/merchandise-order?submit=1')

    merch_type = request.POST.get('merch_type')
    delete_id = request.POST.get('delete')
    slug = request.POST.get('slug')

    if merch_type == 'item':
        merch_model = Item
        order_model = ItemOrder
        form_type = ItemOrderForm
    elif merch_type == 'bundle':
        merch_model = Bundle
        order_model = BundleOrder
        form_type = BundleOrderForm
    else:
        return redirect(main)

    if delete_id:
        order_obj = get_object_or_404(order_model, id=delete_id)
        order_obj.delete()
        return redirect('/merchandise-order?submit=1')

    merch = get_object_or_404(merch_model, slug=slug)
    form = form_type(request.POST, initial={
        merch_type: merch,
        'school': school,
    })

    if form.is_valid():
        order_obj = form.save(commit=False)
        order_obj.school = school
        setattr(order_obj, merch_type, merch)
        order_obj.save()

        if merch_type == 'bundle':
            order_obj.create_item_orders(form.cleaned_data['size'])

    return redirect('/merchandise-order?submit=1')
