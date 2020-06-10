from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect
from foodwagon_backend.models import *

from django.http import HttpResponse
from foodwagon_backend.models import Venues, Trucks, Chef, Ordered_Venue, Ordered_Chef, ReviewIndex, ReviewTruck, ReviewChef, ReviewOutlet, ReviewVenue, ReviewVenueID, ReviewChefID, ReviewTruckID

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
import datetime
from .models import *


def error_404_view(request, exception):
    return render(request, 'FoodWagon/404.html')


def error_500_view(request):
    return render(request, 'FoodWagon/500.html')

from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Transactions
from .paytm import generate_checksum, verify_checksum

def cart_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        truck_items = order.orderitemtruck_set.all()
        venue_items = order.orderitemvenue_set.all()
        chef_items = order.orderitemchef_set.all()
        return (len(truck_items) + len(venue_items) + len(chef_items))
    else:
        return 0


def review_venueID(request, id):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewVenueID(venue_id=id, Name=Name, Review=review)
        Data.save()
    return redirect('/venue/{}'.format(id))


def review_chefID(request, id):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewChefID(chef_id=id, Name=Name, Review=review)
        Data.save()
    return redirect('/catering/{}'.format(id))


def review_truckID(request, id):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewTruckID(truck_id=id, Name=Name, Review=review)
        Data.save()
    return redirect('/foodtruck/{}'.format(id))


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                firstName = form.cleaned_data.get('first_name')
                lastName = form.cleaned_data.get('last_name')
                messages.success(request, 'Account created for ' +
                                 firstName + ' ' + lastName + '!')
                return redirect('login')
        context = {'form': form}
        return render(request, 'FoodWagon/register.html', context)


def review_truck(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewTruck(Name=Name, Review=review)
        Data.save()
    return redirect('/foodtruck')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                try:
                    # print("try kiya")
                    customer = request.user.customer
                except:
                    # print("nhi tha ")
                    customer1 = Customer(
                        user=request.user, name=request.user.username, email=request.user.email)
                    customer1.save()
                return redirect('index')
            else:
                messages.info(request, 'Username or Password is incorrect')

    return render(request, 'FoodWagon/login.html')


def logoutUser(request):
    logout(request)
    return redirect('index')


def chefbyid(request, id):
    items = cart_items(request)
    chef_list = Chef.objects.get(id=id)
    reviews = ReviewChefID.objects.raw(
        'select * from foodwagon_backend_reviewchefid where chef_id = %s order by id desc', [id])
    chef_dict = {'chef': chef_list, 'reviews': reviews, 'badge_value': items}
    return render(request, 'FoodWagon/chefbyid.html', context=chef_dict)


def venuebyid(request, id):
    items = cart_items(request)
    venue_list = Venues.objects.get(id=id)
    reviews = ReviewVenueID.objects.raw(
        'select * from foodwagon_backend_reviewvenueid where venue_id = %s order by id desc', [id])
    venue_dict = {'venue': venue_list,
                  'reviews': reviews, 'badge_value': items}
    return render(request, 'FoodWagon/venuebyid.html', context=venue_dict)


def truckbyid(request, id):
    items = cart_items(request)
    truck_list = Trucks.objects.get(id=id)
    reviews = ReviewTruckID.objects.raw(
        'select * from foodwagon_backend_reviewtruckid where truck_id = %s order by id desc', [id])
    truck_dict = {'truck': truck_list,
                  'reviews': reviews, 'badge_value': items}
    return render(request, 'FoodWagon/truckbyid.html', context=truck_dict)


def service(request):
    if request.method == "POST":
        city = request.POST['city']
        service = request.POST['service']
        # print(city,service)
        items = cart_items(request)
        if service == "None":
            return render(request, 'FoodWagon/index.html', {'badge_value': items})
        if service == "venue":
            if city == "None":
                venue_list = Venues.objects.all()
                return render(request, 'FoodWagon/venue.html', {'venues': venue_list, 'badge_value': items})
            venue_list = Venues.objects.filter(City=city)
            return render(request, 'FoodWagon/venue.html', {'venues': venue_list, 'badge_value': items})
        if service == "foodtruck":
            truck_list = Trucks.objects.all()
            return render(request, 'FoodWagon/foodtruck.html', {'trucks': truck_list, 'badge_value': items})
        if service == "restaurent":
            return render(request, 'FoodWagon/restaurant.html')
        chef_list = Chef.objects.filter(City=city)
        if city == "None":
            chef_list = Chef.objects.all()
        return render(request, 'FoodWagon/catering.html', {'chefs': chef_list, 'badge_value': items})
    return redirect('/', {'badge_value': items})


def review_index(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewIndex(Name=Name, Review=review)
        Data.save()
    return redirect('/')


def review_venue(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewVenue(Name=Name, Review=review)
        Data.save()
    return redirect('/venue')


def review_restaurent(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewOutlet(Name=Name, Review=review)
        Data.save()
    return redirect('/restaurent')


def review_catering(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewChef(Name=Name, Review=review)
        Data.save()
    return redirect('/catering')


def index(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        message = request.POST['message']
        body = "Name: " + first_name + " " + last_name + "\n" + "\nMessage: " + message
        send_mail(
            'Message from ' + first_name + " " + last_name,
            body,
            email,
            ["yashparmar157000@gmail.com"],
            fail_silently=False
        )
        items = cart_items(request)

        return render(request, 'FoodWagon/index.html', {'name': first_name + " " + last_name, 'badge_value': items})
    venue_list = Venues.objects.all()
    chef_list = Chef.objects.all()
    list_of_cities = []
    for j in venue_list:
        list_of_cities.append(j.City)
    for j in chef_list:
        list_of_cities.append(j.City)
    list_of_cities = set(list_of_cities)
    truck_list = Trucks.objects.all()
    reviews = ReviewIndex.objects.all()
    if request.user.is_authenticated:
        try:
            # print("try kiya")
            customer = request.user.customer
        except:
            # print("nhi tha ")
            customer1 = Customer(
                user=request.user, name=request.user.username, email=request.user.email)
            customer1.save()
    items = cart_items(request)
    return render(request, 'FoodWagon/index.html', {'venuess': list_of_cities, 'truckss': truck_list, 'reviews': reviews, 'badge_value': items})


def adminlogin(request):
    return render(request, 'FoodWagon/adminlogin.html')


def chef(request):
    return render(request, 'FoodWagon/formcatering.html')


def cart(request):
    if request.user.is_authenticated:
        custmores = Customer.objects.all()
        # print(custmores)
        customer = request.user.customer

        # print(customer.email)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        truck_items = order.orderitemtruck_set.all()
        venue_items = order.orderitemvenue_set.all()
        chef_items = order.orderitemchef_set.all()

        # print(created)
        # print(truck_items)
        # print(venue_items)
        # print(chef_items)
    else:
        items = []

    items = cart_items(request)
    context = {
        'truck_items': truck_items,
        'venue_items': venue_items,
        'chef_items': chef_items,
        'order': order,
        'badge_value': items

    }

    return render(request, 'FoodWagon/cart.html', context)


def add_to_cart_truck(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        truck = Trucks.objects.get(id=id)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        curr_truck = OrderItemTruck(truck=truck, order=order, quantity=1)
        curr_truck.save()
        items = cart_items(request)
    

    messages.success(request, 'Successfully Added to Cart.')
    return redirect('/foodtruck/{}'.format(id),{'badge_value':items})

def add_to_cart_venue(request, id):
    if request.user.is_authenticated:
        start = request.POST['start']
        end = request.POST['end']
        venues_available = Venues.objects.raw(
            'select id from foodwagon_backend_venues where id not in (select venue_id from foodwagon_backend_ordered_venue where not("end" < %s or start > %s))', [start, end])
        flag = False
        for venue in venues_available:
            if venue.id == id:
                flag = True
        if flag:
            customer = request.user.customer
            venue = Venues.objects.get(id=id)
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            curr_venue = OrderItemVenue(venue=venue, order=order, quantity=1)
            curr_venue.save()
            message = 'Succussfully added to cart'
            messages.success(request, 'Successfully Added to Cart.')
            items = cart_items(request)
        else:
            message = "Can't add to cart"
            items = cart_items(request)
            essages.warning(request, 'Sorry Venue is Booked in Specified Date')
        return redirect('/venue/{}'.format(id), {'badge_value': items, 'message': "Hello"})


def add_to_cart_chef(request, id):
    if request.user.is_authenticated:
        start = request.POST['start']
        end = request.POST['end']
        chefs_available = Chef.objects.raw(
            'select id from foodwagon_backend_chef where id not in (select chef_id from foodwagon_backend_ordered_chef where not("end" < %s or start > %s))', [start, end])
        flag = False
        for chef in chefs_available:
            if chef.id == id:
                flag = True
        if flag:
            customer = request.user.customer
            chef = Chef.objects.get(id=id)
            # print(chef)
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            curr_chef = OrderItemChef(chef=chef, order=order, quantity=1)
            curr_chef.save()
            message = 'Succussfully added to cart'
            items = cart_items(request)
            messages.success(request, 'Successfully Added to Cart.')

        else:
            message = 'Cant add to cart'
            items = cart_items(request)
            messages.warning(request, 'Sorry Chef is Booked in Specified Date')
        return redirect('/catering/{}'.format(id), {'badge_value': items, 'message': message})


def delete_item_cart_truck(request, id):
    if request.user.is_authenticated:
        items = cart_items(request)
        OrderItemTruck.objects.filter(id=id).delete()
        items -= 1
    return redirect('/cart', {'badge_value': items})


def delete_item_cart_venue(request, id):
    if request.user.is_authenticated:
        items = cart_items(request)
        OrderItemVenue.objects.filter(id=id).delete()
    return redirect('/cart', {'badge_value': items})


def delete_item_cart_chef(request, id):
    if request.user.is_authenticated:
        items = cart_items(request)
        OrderItemChef.objects.filter(id=id).delete()
        items -= 1
    return redirect('/cart', {'badge_value': items})


def is_valid_query_param(param):
    return param != '' and param is not None


def catering(request):
    items = cart_items(request)

    if request.method == 'POST':
        work = request.POST.getlist('work[]')
        name = request.POST['full_name']
        mobile = request.POST['mobile_number']
        email = request.POST['email']
        stipend = request.POST['stipend']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        area = request.POST['area']
        address = request.POST['address']
        north = request.POST.get('north')
        south = request.POST.get('south')
        gujarati = request.POST.get('gujarati')
        punjabi = request.POST.get('punjabi')
        rajasthani = request.POST.get('rajasthani')
        jain = request.POST.get('jain')
        bengali = request.POST.get('bengali')
        marathi = request.POST.get('marathi')
        continental = request.POST.get('continental')
        bakery = request.POST.get('bakery')
        other = request.POST.get('other')
        work_type = request.POST['work_type']
        expert = request.POST['food_type_id']
        lic = request.POST['is_license']
        customer = request.POST['customer_strength']
        employee = request.POST['employee_id']
        image = request.FILES['image']
        if customer == '':
            customer = 0
        Data = Chef(Work_As=work, Name=name, Phone=mobile, Email=email, Stipend=stipend, Country=country, State=state,
                    City=city, Area=area, Address=address, Type=work_type, ExpertIn=expert, License=lic,
                    Base=customer, EmployeeID=employee, Image=image)
        Data.save()

        if is_valid_query_param(north):
            s1 = Data.Speciality.create(speciality=north)
        if is_valid_query_param(south):
            s2 = Data.Speciality.create(speciality=south)
        if is_valid_query_param(gujarati):
            s3 = Data.Speciality.create(speciality=gujarati)
        if is_valid_query_param(punjabi):
            s4 = Data.Speciality.create(speciality=punjabi)
        if is_valid_query_param(jain):
            s5 = Data.Speciality.create(speciality=jain)
        if is_valid_query_param(bakery):
            s6 = Data.Speciality.create(speciality=bakery)
        if is_valid_query_param(continental):
            s7 = Data.Speciality.create(speciality=continental)
        if is_valid_query_param(rajasthani):
            s8 = Data.Speciality.create(speciality=rajasthani)
        if is_valid_query_param(bengali):
            s9 = Data.Speciality.create(speciality=bengali)
        if is_valid_query_param(marathi):
            s10 = Data.Speciality.create(speciality=marathi)
        if is_valid_query_param(other):
            s10 = Data.Speciality.create(speciality=other)

        return redirect('catering')

    reviews = ReviewChef.objects.all().order_by('id').reverse()
    special = Special.objects.all().order_by('speciality')

    name_contains_query = request.GET.get('name_contains')
    state_query = request.GET.get('state')
    city_query = request.GET.get('city')
    state = request.GET.get('state')
    city = request.GET.get('city')
    expertin = request.GET.get('expertin')
    start = request.GET.get('start')
    end = request.GET.get('end')
    north = request.GET.get('North Indian')
    south = request.GET.get('South Indian')
    gujarati = request.GET.get('Gujarati')
    punjabi = request.GET.get('Punjabi')
    bakery = request.GET.get('Bakery')
    rajasthani = request.GET.get('Rajasthani')
    continental = request.GET.get('Continental')
    bengali = request.GET.get('Bengali')
    marathi = request.GET.get('Marathi')
    jain = request.GET.get('Jain Food')
    other = request.GET.get('Other')
    start = request.GET.get('start')
    end = request.GET.get('end')
    allchefs = Chef.objects.all()
    chefs = Chef.objects.all()
    main1 = Chef.objects.all()

    ordered_chef = Ordered_Chef.objects.all()

    format = "%Y-%m-%d"
    if is_valid_query_param(start) and is_valid_query_param(end):
        start = datetime.datetime.strptime(start, format)
        end = datetime.datetime.strptime(end, format)
        start = start.date()
        end = end.date()
        ids_ordered_chef = []
        for i in ordered_chef:
            if i.start <= start <= i.end or i.start <= end <= i.end:
                ids_ordered_chef.append(i.chef_id)
        ids_allchefs = []
        for i in allchefs:
            if i.id not in ids_ordered_chef:
                ids_allchefs.append(i.id)

        allchefs = allchefs.filter(id__in=ids_allchefs)

    if is_valid_query_param(name_contains_query):
        allchefs = allchefs.filter(Name__icontains=name_contains_query)
    if is_valid_query_param(state_query) and state != 'Search':
        allchefs = allchefs.filter(State=state_query)
    if is_valid_query_param(city_query) and city != 'Search':
        allchefs = allchefs.filter(City=city_query)
    if is_valid_query_param(expertin):
        allchefs = allchefs.filter(ExpertIn=expertin)

    if is_valid_query_param(south):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=south))
    if is_valid_query_param(north):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=north))
    if is_valid_query_param(gujarati):
        allchefs = allchefs.filter(
            Q(Speciality__speciality__contains=gujarati))
    if is_valid_query_param(marathi):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=marathi))
    if is_valid_query_param(bengali):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=bengali))
    if is_valid_query_param(continental):
        allchefs = allchefs.filter(
            Q(Speciality__speciality__contains=continental))
    if is_valid_query_param(bakery):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=bakery))
    if is_valid_query_param(rajasthani):
        allchefs = allchefs.filter(
            Q(Speciality__speciality__contains=rajasthani))
    if is_valid_query_param(punjabi):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=punjabi))
    if is_valid_query_param(jain):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=jain))
    if is_valid_query_param(other):
        allchefs = allchefs.filter(Q(Speciality__speciality__contains=other))
    cities = []
    states = []
    for i in main1:
        cities.append(i.City)
        states.append(i.State)

    cities = list(set(cities))
    states = list(set(states))
    speciality_choices = ["North Indian", "South Indian", "Gujarati", "Bengali",
                          "Rajasthani", "Marathi", "Continental", "Punjabi", "Jain Food", "Bakery", "Other"]
    if start == None:
        if end == None:
            return render(request, 'FoodWagon/catering.html', {'chefs': chefs, 'main': main1, 'reviews': reviews, 'badge_value': items, 'allchefs': allchefs, 'special': special, 'speciality_choices': speciality_choices, 'cities': cities, 'states': states})

    return render(request, 'FoodWagon/catering.html', {'chefs': chefs, 'main': main1, 'reviews': reviews, 'badge_value': items, 'allchefs': allchefs, 'special': special, 'speciality_choices': speciality_choices, 'cities': cities, 'states': states})


def restaurent(request):
    items = cart_items(request)

    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        message = request.POST['message']
        body = "Name: " + first_name + " " + last_name + \
            "\nPhone number: " + phone_number + "\nMessage: " + message
        send_mail(
            'Message from ' + first_name + " " + last_name,
            body,
            email,
            ["yashparmar157000@gmail.com"],
            fail_silently=False
        )
        return render(request, 'FoodWagon/restaurent.html', {'name': first_name + " " + last_name, 'badge_value': items})
    reviews = ReviewOutlet.objects.all().order_by('id').reverse()
    return render(request, 'FoodWagon/restaurent.html', {'reviews': reviews, 'badge_value': items})


def venue(request):
    venue_list_distint_city = Venues.objects.values('City').distinct()
    items = cart_items(request)

    if request.method == "POST":
        city = request.POST['city']
        Sor = request.POST['sort']
        start = request.POST['start']
        end = request.POST['end']
        # print(start, end)
        if city != "None":
            if Sor == "lowtohigh":

                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where id not in (select venue_id from foodwagon_backend_ordered_venue where not("end" < %s or start > %s)) and "City" = %s order by "Price_per_Day"', [start, end, city])
            else:
                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where id not in (select venue_id from foodwagon_backend_ordered_venue where not("end" < %s or start > %s)) and "City" = %s order by "Price_per_Day" desc', [start, end, city])
        else:
            if Sor == "lowtohigh":
                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where id not in (select venue_id from foodwagon_backend_ordered_venue where not("end" < %s or start > %s)) order by "Price_per_Day"', [start, end])
            else:
                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where id not in (select venue_id from foodwagon_backend_ordered_venue where not("end" < %s or start > %s))  order by "Price_per_Day" desc', [start, end])
        if len(venue_list) == 0:
            paginator = Paginator(venue_list, 1)
        else:
            paginator = Paginator(venue_list, len(venue_list))
        page = request.GET.get('page')
        # print(page)
        try:
            venues = paginator.page(page)
        except PageNotAnInteger:
            venues = paginator.page(1)
        except EmptyPage:
            venues = paginator.page(paginator.num_pages)
    else:
        venue_list = Venues.objects.all()
        paginator = Paginator(venue_list, 3)
        page = request.GET.get('page')
        # print(page)
        try:
            venues = paginator.page(page)
        except PageNotAnInteger:
            venues = paginator.page(1)
        except EmptyPage:
            venues = paginator.page(paginator.num_pages)
    reviews = ReviewVenue.objects.all().order_by('id').reverse()
    venue_dict = {
        'venues': venues, 'venues_list': venue_list_distint_city, 'reviews': reviews, 'badge_value': items
    }

    return render(request, 'FoodWagon/venue.html', context=venue_dict)


def foodtruck(request):
    items = cart_items(request)
    truck_list = Trucks.objects.all()
    if request.method == 'POST':
        sor = request.POST['sort']
        if sor == "lowtohigh":
            truck_list = Trucks.objects.all().order_by('Price')
        else:
            truck_list = Trucks.objects.all().order_by('Price').reverse()
    paginator = Paginator(truck_list, 3)
    page = request.GET.get('page')
    try:
        trucks = paginator.page(page)
    except PageNotAnInteger:
        trucks = paginator.page(1)
    except EmptyPage:
        trucks = paginator.page(paginator.num_pages)
    truck_dict = {
        'trucks': trucks,
    }
    reviews = ReviewTruck.objects.all().order_by('id').reverse()
    return render(request, 'FoodWagon/foodtruck.html', {'trucks': trucks, 'reviews':reviews,'badge_value':items})

def payment(request):
    if request.method == "POST":
        amount = request.POST['totalamount']
        return render(request,'FoodWagon/pay.html',{'amount':amount})
    return redirect('/cart')

def initiate_payment(request):
    
    try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'FoodWagon/pay.html', context={'error': 'Wrong Account Details or amount','amount':amount})
    
    transaction = Transactions.objects.create(CustomerID = request.user.id , amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.CustomerID)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO')
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)
    
    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    # print('SENT: ', checksum)
    return render(request, 'FoodWagon/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        # print(request.body)
        # print(request.POST)
        received_data = dict(request.POST)
        # print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        return render(request, 'FoodWagon/callback.html', context=received_data)

