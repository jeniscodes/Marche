from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User,Listing,Bid,Comment,Watchlist

#index page
def index(request):
    items=Listing.objects.filter(status="Open")
    return render(request, "auctions/index.html",{
    "items":items
    })

#login page view function
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        next=request.POST.get("next")
        item=next.split('/')

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            try:
                itemid=item[2]
                return redirect(f'/{itemid}')
            except:

                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "  Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        title=request.POST["title"]
        description=request.POST["description"]
        bid=request.POST["bid"]
        category=request.POST["category"]
        url=request.POST    ["url"]
        #check whether title , description or bid is empty

        if title =='' or description == '' or bid == '':
            return render(request, "auctions/create.html",{"message":"You have to enter title, bid and description of item"})
        else:
            if category=='':
                #default value when category is not provided
                category="No Category"
                if url == '':
                    #default value when image is not provided
                    url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png'
                    item=Listing(title=title,description=description,price=bid,category=category,Image=url,owner=request.user,status="Open")
                    item.save()
                    return render(request,"auctions/status.html",{
                    "item":item,"bids":item.lbids.all().order_by('-bid'),
                    "comments":item.comments.all()})
                else:
                    item=Listing(title=title,description=description,price=bid,category=category,Image=url,owner=request.user,status="Open")
                    item.save()
                    return render(request,"auctions/status.html",{
                    "item":item,"bids":item.lbids.all().order_by('-bid'),
                    "comments":item.comments.all()})
            else:
                if url == '':
                    url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png'
                    item=Listing(title=title,description=description,price=bid,category=category,Image=url,owner=request.user,status="Open")
                    item.save()
                    return render(request,"auctions/status.html",{
                    "item":item,"bids":item.lbids.all().order_by('-bid'),
                    "comments":item.comments.all()})
                else:
                    item=Listing(title=title,description=description,price=bid,category=category,Image=url,owner=request.user,status="Open")
                    item.save()
                    return render(request,"auctions/status.html",{
                    "item":item,"bids":item.lbids.all().order_by('-bid'),
                    "comments":item.comments.all()})

    else:
        return render(request, "auctions/create.html")

#item details page view function
def item(request,id):
    item=Listing.objects.get(pk=id)
    status=item.status
    comments=item.comments.all()
    #check whether listing is open or  not
    if status=="Open":
        #check whether owner is checking his listig
        if request.user==item.owner:
            if request.method=="POST":
                status=request.POST.get("status")
                item.status=status
                item.save()
                #get highestbid
                highestbid= item.lbids.all().order_by('-bid').first()
      #if no bid has been done
                if highestbid is None:
                    return render(request,"auctions/status.html",{
                    "item":item,"hmessage":"closed","hbid": highestbid
                    })
                else:


                    return render(request,"auctions/status.html",{
                    "item":item,"message":"closed","hbid": highestbid
                    })




            else:
                return render(request,"auctions/status.html",{
                "item":item,"bids":item.lbids.all().order_by('-bid'),
                "comments":comments})





        else:
                return render(request,"auctions/item.html",{
                "item":item,"bids":item.lbids.all().order_by('-bid'),
                "comments":comments
                })
    else:
        highestbid= item.lbids.all().order_by('-bid').first()
        if highestbid is None:
            return render(request,"auctions/status.html",{
            "item":item,"hmessage":"closed","hbid":highestbid,"status":"closed"
            })
        else:


            return render(request,"auctions/status.html",{
            "item":item,"message":"closed","hbid":highestbid,"status":"closed"
            })


#view function to add item in the watchlist
@login_required(login_url='/login')
def add(request,id):
    item=Listing.objects.get(pk=id)


    comments=item.comments.all()

    check=Watchlist.objects.filter(litem=item)
    print(check)
    #whether item is in watchlist or not
    if len(check) == 0:

        wlist=Watchlist(litem=item,luser=request.user)
        wlist.save()
        return render(request,"auctions/item.html",{
        "item":item,"message":"Added to watchlist","bids":item.lbids.all().order_by('-bid'),
        "comments":comments
        })
    else:
        return render(request,"auctions/item.html",{
        "item":item,"wmessage":"The item is already in your watchlist","bids":item.lbids.all().order_by('-bid'),
        "comments":comments})

#view function to bid on the item
@login_required(login_url='/login')
def bid(request,id):
    item=Listing.objects.get(pk=id)
    comments=item.comments.all()
    bid=request.POST.get("bid")
    #convert bid into  float value
    try:
        bid=float(bid)
        #check whether bid is higher than starting bid or not
        if bid<item.price:

            return render(request,"auctions/item.html",{
            "item":item,"message":"Bid should be higher than starting bid.", "bids":item.lbids.all().order_by('-bid'),
            "comments":comments})
        else:
            highestbid= item.lbids.all().order_by('-bid').first()
            if highestbid is None :

                bid=Bid(bid=bid,item=item,bidder=request.user)
                bid.save()
                return render(request,"auctions/item.html",{
                "item":item,"message":"Your bid is submitted.","bids":item.lbids.all().order_by('-bid'),
                "comments":comments
                })
            else:
                if bid>highestbid.bid:

                    bid=Bid(bid=bid,item=item,bidder=request.user)
                    bid.save()
                    return render(request,"auctions/item.html",{
                    "item":item,"message":"Your bid is submitted.","bids":item.lbids.all().order_by('-bid'),
                    "comments":comments})
                else:
                    return render(request,"auctions/item.html",{
                    "item":item,"message":"Bid should be higher than highest bid.","bids":item.lbids.all().order_by('-bid'),
                    "comments":comments
                    })


    except:

        return render(request,"auctions/item.html",{
        "item":item,"message":"Please nter a numerical value.","bids":item.lbids.all().order_by('-bid'),
        "comments":comments
        })

#view function to add comment on the listing
@login_required(login_url='/login')
def comment(request,id):
    item=Listing.objects.get(pk=id)
    comments=item.comments.all()
    bid=item.lbids.all().order_by('-bid')
    text=request.POST.get("review")

# check whether comment is at least 10 characters long
    if len(text)>10:

        text=Comment(comment=text,item=item,commenter=request.user)
        text.save()
        comments=item.comments.all()
        return render(request,"auctions/item.html",{
       "item":item,"bids":bid,
       "comments":comments})
    else:
        return render(request,"auctions/item.html",{
        "item":item,"message":"Comment should be at least 10 characters long", "bids":bid,
        "comments":comments

        })

#view function for watchlist page

@login_required(login_url='/login')
def watchlist(request):
    #to remove from the watchlist
    if request.method=="POST":
        id=request.POST.get("remove")
        listitem=Watchlist.objects.get(pk=id)
        listitem.delete()
        wlist=request.user.wuser.all()
        return render(request,"auctions/watchlist.html",{
        "wlist":wlist})
    else:
        wlist=request.user.wuser.all()
        return render(request,"auctions/watchlist.html",{
        "wlist":wlist})

#my created listings page view function
@login_required(login_url='/login')
def mylist(request):
    mylist=request.user.items.all()
    return render(request,"auctions/mylist.html",{
    "mylist":mylist})

#view function to remove an item from watchlist if its already there
def remove(request,id):
    item=Listing.objects.get(pk=id)


    comments=item.comments.all()

    listitem=Watchlist.objects.get(litem=id)
    listitem.delete()

    return render(request,"auctions/item.html",{
    "item":item,"message":"Item removed from your watchlist","bids":item.lbids.all().order_by('-bid'),
    "comments":comments
    })

#view function for sorting itmes with unique categories
def categories(request):


    items=Listing.objects.all().values('category').distinct()


    return render(request,"auctions/categories.html",{
    "items":items
    })

#active items in each distinct category

def clisting(request,category):



    items=Listing.objects.filter(category=category,status="Open")



    return render(request,"auctions/clisting.html",{
    "items":items
    })
