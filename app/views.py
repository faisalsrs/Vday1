from django.shortcuts import render, redirect
from .models import *
import bcrypt
import http.client
import json

conn = http.client.HTTPSConnection("camelcamelcamel1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "camelcamelcamel1.p.rapidapi.com",
    'x-rapidapi-key': "f651328bf4msh41fb0bac893f844p1a9f0djsn31dfbfbc30d3"
}

# conn.request("GET", "/priceReport?marketplace=US&asin=B0020MMD4W", headers=headers)

# res = conn.getresponse()
# data = res.read()


def index(request):
    return render(request, 'index.html')


def logout(request):
    request.session.clear()
    return redirect('/')


def register(request):
    return render(request, 'new_account.html')


def new_account(request):
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    user_in_db = User.objects.filter(email=request.POST['email']).first()

    if user_in_db:
        messages.error(request, "User already exists. Please login")
        return redirect('/')

    hashed_password = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name=request.POST['fname'],
        last_name=request.POST['lname'],
        email=request.POST['email'],
        password=hashed_password
    )

    request.session['user_id'] = new_user.id

    return redirect('/giftwall')


def login(request):
    found_user = User.objects.filter(email=request.POST['email'])
    print('&'*100)
    print(found_user)
    if len(found_user) > 0:
        user_from_db = found_user[0]

        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(),
            user_from_db.password.encode()
        )
        if not is_pw_correct:
            messages.error(request, "Invalid credentials")
            return redirect('/register')
    request.session['user_id'] = user_from_db.id
    return redirect('/giftwall')


def grantor_login(request):
    found_user = Gift.objects.filter(email2=request.POST['email2'])
    if len(found_user) > 0:
        messages.error(request, "No Sugar For You")

    return redirect('/grantor_page')


def giftwall(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        print("HERE!!!!")
        messages.error(request, "Please log in or register")
        return redirect('/')
    user_logged = User.objects.get(id=user_id)
    context = {
        "user": User.objects.get(id=user_id),
        "my_gifts": user_logged.gifts.all()
    }
    return render(request, 'gift_wall.html', context)


def grantor_page(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')

    context = {
        "user": User.objects.all(),
        "all_gifts": Gift.objects.all()
    }
    return render(request, 'grantor_page.html', context)


def new_gift(request):
    return render(request, 'new_gift.html')


def findAsin(str):
    index = str.index("dp/")
    asin = str[index+3:(index+13)]
    return asin


def submit_a_new_gift(request):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect("/")

    errors = Gift.objects.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new_gift')

    user_submitted = User.objects.get(id=user_id)
    asin = findAsin(request.POST['item_url'])
    conn.request(
        "GET", f'/priceReport?marketplace=US&asin={asin}', headers=headers)

    res = conn.getresponse()
    # data = res.read()
    data = json.load(res)
    print(data)
    if(data['prices'].get('priceAmazon')):
        price = (data["prices"].get("priceAmazon"))/100
    elif data['prices'].get("priceNew"):
        price = (data["prices"].get("priceNew"))/100

    newest_gift = Gift.objects.create(
        item=request.POST['item'],
        item_url=request.POST['item_url'],
        description=request.POST['description'],
        email2=request.POST['email2'],
        price=price,
        submitted_by=user_submitted
    )
    return redirect('/giftwall')


def unique(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')

    context = {
        "user": User.objects.get(id=user_id),
        "all_gifts": Gift.objects.get(id=user_id),
    }
    return render(request, 'unique.html')


def works(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')

    context = {
        "user": User.objects.get(id=user_id),
        "all_gifts": Gift.objects.get(id=user_id),
    }
    return render(request, 'works.html')


def edit_gift(request, id):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect("/")
    edit_wish = Gift.objects.filter(id=id).first
    context = {
        "Gift": edit_wish
    }
    return render(request, 'edit.html', context)


def update_gift(request, id):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect("/")

    errors = Gift.objects.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/Gift/edit/{id}')

    gifts_from_db = Gift.objects.get(id=id)

    gifts_from_db.item_url = request.POST['item_url']
    gifts_from_db.item = request.POST['item']
    gifts_from_db.description = request.POST['description']
    gifts_from_db.email2 = request.POST['email2']
    gifts_from_db.save()
    return redirect('/gift')


def delete(request, id):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect("/")

    delete_gift = Gift.objects.get(id=id)
    delete_gift.delete()
    return redirect('/giftwall')
