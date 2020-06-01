from django.shortcuts import render, redirect

from django.http import HttpResponse,HttpResponseRedirect
from foodwagon_backend.models import Venues, Trucks, Chef, Ordered_Venue, Ordered_Chef

from django.http import HttpResponse
from foodwagon_backend.models import Venues, Trucks, Chef, Ordered_Venue, Ordered_Chef,ReviewIndex,ReviewTruck,ReviewChef,ReviewOutlet,ReviewVenue,ReviewVenueID,ReviewChefID,ReviewTruckID

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .models import *
 
cart_item = 0

def review_venueID(request,id):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewVenueID(venue_id = id ,Name = Name , Review = review)
        Data.save()
    return redirect('/venue/{}'.format(id))

def review_chefID(request,id):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewChefID(chef_id = id ,Name = Name , Review = review)
        Data.save()
    return redirect('/catering/{}'.format(id))

def review_truckID(request,id):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewTruckID(truck_id = id ,Name = Name , Review = review)
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
        Data = ReviewTruck(Name = Name , Review = review)
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
                return redirect('index')
            else:
                messages.info(request, 'Username or Password is incorrect')

    return render(request, 'FoodWagon/login.html')


def logoutUser(request):
    logout(request)
    return redirect('index')


def chefbyid(request, id):
    chef_list = Chef.objects.get(id=id)
    reviews = ReviewChefID.objects.raw('select * from foodwagon_backend_reviewchefid where chef_id = %s order by id desc',[id])
    chef_dict = {'chef': chef_list,'reviews':reviews,'badge_value':cart_item}
    return render(request, 'FoodWagon/chefbyid.html', context=chef_dict)


def venuebyid(request, id):
    venue_list = Venues.objects.get(id=id)
    reviews = ReviewVenueID.objects.raw('select * from foodwagon_backend_reviewvenueid where venue_id = %s order by id desc',[id])
    venue_dict = {'venue': venue_list , 'reviews':reviews,'badge_value':cart_item}
    return render(request, 'FoodWagon/venuebyid.html', context=venue_dict)


def truckbyid(request, id):
    truck_list = Trucks.objects.get(id=id)
    reviews = ReviewTruckID.objects.raw('select * from foodwagon_backend_reviewtruckid where truck_id = %s order by id desc',[id])
    truck_dict = {'truck': truck_list,'reviews':reviews,'badge_value':cart_item}
    return render(request, 'FoodWagon/truckbyid.html', context=truck_dict)


def service(request):
    if request.method == "POST":
        city = request.POST['city']
        service = request.POST['service']
        print(city,service)
        if service == "None":
            return render(request, 'FoodWagon/index.html')
        if service == "venue":
            if city == "None":
                venue_list = Venues.objects.all()
                return render(request, 'FoodWagon/venue.html', {'venues': venue_list,'badge_value':cart_item})
            venue_list = Venues.objects.filter(City=city)
            return render(request, 'FoodWagon/venue.html', {'venues': venue_list,'badge_value':cart_item})
        if service == "foodtruck":
            truck_list = Trucks.objects.all()
            return render(request, 'FoodWagon/foodtruck.html', {'trucks': truck_list,'badge_value':cart_item})
        if service == "restaurent":
            return render(request, 'FoodWagon/restaurant.html')
        chef_list = Chef.objects.filter(City=city)
        if city == "None": 
            chef_list = Chef.objects.all()
        return render(request, 'FoodWagon/catering.html' , {'chefs':chef_list,'badge_value':cart_item})
    return redirect('/',{'badge_value':cart_item})

def review_index(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewIndex(Name = Name , Review = review)
        Data.save()
    return redirect('/')

def review_venue(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewVenue(Name = Name , Review = review)
        Data.save()
    return redirect('/venue')

def review_restaurent(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewOutlet(Name = Name , Review = review)
        Data.save()
    return redirect('/restaurent')

def review_catering(request):
    if request.method == 'POST':
        fname = request.user.first_name
        lname = request.user.last_name
        Name = fname + " " + lname
        review = request.POST['review']
        Data = ReviewChef(Name = Name , Review = review)
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
        return render(request, 'FoodWagon/index.html', {'name': first_name + " " + last_name,'badge_value':cart_item})
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
    return render(request, 'FoodWagon/index.html', {'venuess': list_of_cities, 'truckss': truck_list ,'reviews':reviews,'badge_value':cart_item})


def adminlogin(request):
    return render(request, 'FoodWagon/adminlogin.html')


def chef(request):
    return render(request, 'FoodWagon/formcatering.html')


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer.email)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        truck_items = order.orderitemtruck_set.all()
        venue_items = order.orderitemvenue_set.all()
        chef_items = order.orderitemchef_set.all()
        print(created)
        print(truck_items)
        print(venue_items)
        print(chef_items)
    else:
        items = []
    context = {
        'truck_items': truck_items,
        'venue_items': venue_items,
        'chef_items': chef_items,
        'order': order,
        'badge_value':cart_item
        }

    return render(request, 'FoodWagon/cart.html',context)

def add_to_cart_truck(request,id):
    if request.user.is_authenticated:
        global cart_item
        cart_item += 1
        customer = request.user.customer
        truck = Trucks.objects.get(id = id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        curr_truck = OrderItemTruck(truck = truck, order= order, quantity =1)
        curr_truck.save()
        print(cart_item)
    return redirect('/foodtruck/{}'.format(id),{'badge_value':cart_item})

def add_to_cart_venue(request,id):
    if request.user.is_authenticated:
        global cart_item
        cart_item += 1
        customer = request.user.customer
        venue = Venues.objects.get(id = id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        curr_venue = OrderItemVenue(venue = venue, order= order, quantity =1)
        curr_venue.save()
        print(cart_item)
    return redirect('/venue/{}'.format(id),{'badge_value':cart_item})


def add_to_cart_chef(request,id):
    if request.user.is_authenticated:
        global cart_item
        cart_item += 1
        customer = request.user.customer
        chef = Chef.objects.get(id= id)
        print(chef)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        curr_chef = OrderItemChef(chef = chef, order= order, quantity =1)
        curr_chef.save()
    return redirect('/catering/{}'.format(id),{'badge_value':cart_item})

    





def is_valid_query_param(param):
    return param != '' and param is not None


def catering(request):
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
        spe = request.POST.getlist('special[]')
        work_type = request.POST['work_type']
        expert = request.POST['food_type_id']
        lic = request.POST['is_license']
        customer = request.POST['customer_strength']
        employee = request.POST['employee_id']
        image = request.FILES['image']
        if customer == '':
            customer = 0
        Data = Chef(Work_As=work, Name=name, Phone=mobile, Email=email, Stipend=stipend, Country=country, State=state,
                    City=city, Area=area, Address=address, Speciality=spe, Type=work_type, ExpertIn=expert, License=lic,
                    Base=customer, EmployeeID=employee, Image=image)
        Data.save()
        chefs = Chef.objects.all()
        main1 = Chef.objects.all()
        name_contains_query = request.GET.get('name_contains')

        city_query = request.GET.get('city')
        state_query = request.GET.get('state')

        if is_valid_query_param(name_contains_query):
            chefs = chefs.filter(Name=name_contains_query)
        if is_valid_query_param(state_query) and state != 'Search':
            chefs = chefs.filter(State=state_query)
        if is_valid_query_param(city_query) and city != 'Search':
            chefs = chefs.filter(City=city_query)
        reviews = ReviewChef.objects.all().order_by('id').reverse()
        return render(request, 'FoodWagon/catering.html', {'chefs': chefs, "main": main1,'reviews':reviews})
    reviews = ReviewChef.objects.all().order_by('id').reverse()
    name_contains_query = request.GET.get('name_contains')
    state_query = request.GET.get('state')
    city_query = request.GET.get('city')
    state = request.GET.get('state')
    city = request.GET.get('city')
    expertin = request.GET.get('expertin')
    start = request.GET.get('start')
    end = request.GET.get('end')
    chefs = Chef.objects.all()
    main1 = Chef.objects.all()
    if start == None:
        if end == None:
            return render(request, 'FoodWagon/catering.html', {'chefs': chefs, 'main': main1,'reviews':reviews,'badge_value':cart_item})
    chefs = Chef.objects.raw(
                    'select * from foodwagon_backend_chef where (id in (select distinct chef_id from foodwagon_backend_ordered_chef where not exists ( select chef_id from foodwagon_backend_ordered_chef where %s between start and "end" or %s between start and "end")) or id not in (select distinct chef_id from foodwagon_backend_ordered_chef))', [start, end])
    
    

    main1 = Chef.objects.all()

    if is_valid_query_param(name_contains_query):
        chefs = Chef.objects.raw(
                    'select * from foodwagon_backend_chef where (id in (select distinct chef_id from foodwagon_backend_ordered_chef where not exists ( select chef_id from foodwagon_backend_ordered_chef where %s between start and "end" or %s between start and "end")) or id not in (select distinct chef_id from foodwagon_backend_ordered_chef)) and "Name" = %s', [start, end,name_contains_query])
    if is_valid_query_param(state_query) and state != 'Search':
        chefs = Chef.objects.raw(
                    'select * from foodwagon_backend_chef where (id in (select distinct chef_id from foodwagon_backend_ordered_chef where not exists ( select chef_id from foodwagon_backend_ordered_chef where %s between start and "end" or %s between start and "end")) or id not in (select distinct chef_id from foodwagon_backend_ordered_chef)) and "State" = %s', [start, end,state_query])
    if is_valid_query_param(city_query) and city != 'Search':
        chefs = Chef.objects.raw(
                    'select * from foodwagon_backend_chef where (id in (select distinct chef_id from foodwagon_backend_ordered_chef where not exists ( select chef_id from foodwagon_backend_ordered_chef where %s between start and "end" or %s between start and "end")) or id not in (select distinct chef_id from foodwagon_backend_ordered_chef)) and "City" = %s', [start, end,city_query])
    
    if is_valid_query_param(expertin):
       chefs = Chef.objects.raw(
                    'select * from foodwagon_backend_chef where (id in (select distinct chef_id from foodwagon_backend_ordered_chef where not exists ( select chef_id from foodwagon_backend_ordered_chef where %s between start and "end" or %s between start and "end")) or id not in (select distinct chef_id from foodwagon_backend_ordered_chef)) and "ExpertIn" = %s', [start, end,expertin])
    return render(request, 'FoodWagon/catering.html', {'chefs': chefs, 'main': main1,'reviews':reviews,'badge_value':cart_item})



def restaurent(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        message = request.POST['message']
        body = "Name: " + first_name + " " + last_name + \
            "\nPhone number: " + phone_number + "\nMassage: " + message
        send_mail(
            'Message from ' + first_name + " " + last_name,
            body,
            email,
            ["yashparmar157000@gmail.com"],
            fail_silently=False
        )
        return render(request, 'FoodWagon/restaurent.html', {'name': first_name + " " + last_name,'badge_value':cart_item})
    reviews = ReviewOutlet.objects.all().order_by('id').reverse()
    return render(request, 'FoodWagon/restaurent.html',{'reviews':reviews,'badge_value':cart_item})


def venue(request):
    venue_list_distint_city = Venues.objects.values('City').distinct()

    if request.method == "POST":
        city = request.POST['city']
        Sor = request.POST['sort']
        start = request.POST['start']
        end = request.POST['end']
        print(start, end)
        if city != "None":
            if Sor == "lowtohigh":
                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where (id in (select distinct venue_id from foodwagon_backend_ordered_venue where not exists ( select venue_id from foodwagon_backend_ordered_venue where %s between start and "end" or %s between start and "end")) or id not in (select distinct venue_id from foodwagon_backend_ordered_venue)) and "City" = %s order by "Price_per_Day"', [start, end, city])
            else:
                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where (id in (select distinct venue_id from foodwagon_backend_ordered_venue where not exists ( select venue_id from foodwagon_backend_ordered_venue where %s between start and "end" or %s between start and "end")) or id not in (select distinct venue_id from foodwagon_backend_ordered_venue)) and "City" = %s order by "Price_per_Day" desc', [start, end, city])

        else:
            if Sor == "lowtohigh":
                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where (id in (select distinct venue_id from foodwagon_backend_ordered_venue where not exists ( select venue_id from foodwagon_backend_ordered_venue where %s between start and "end" or %s between start and "end")) or id not in (select distinct venue_id from foodwagon_backend_ordered_venue))  order by "Price_per_Day"', [start, end])

            else:
                venue_list = Venues.objects.raw(
                    'select * from foodwagon_backend_venues where (id in (select distinct venue_id from foodwagon_backend_ordered_venue where not exists ( select venue_id from foodwagon_backend_ordered_venue where %s between start and "end" or %s between start and "end")) or id not in (select distinct venue_id from foodwagon_backend_ordered_venue)) order by "Price_per_Day" desc', [start, end])
        print(venue_list)
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
        'venues': venues, 'venues_list': venue_list_distint_city,'reviews':reviews,'badge_value':cart_item
    }

    return render(request, 'FoodWagon/venue.html', context=venue_dict)


def foodtruck(request):
    truck_list = Trucks.objects.all()
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
    return render(request, 'FoodWagon/foodtruck.html', {'trucks': trucks, 'reviews':reviews,'badge_value':cart_item})
