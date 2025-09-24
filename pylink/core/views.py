from django.shortcuts import render, redirect, get_object_or_404
from .models import Link, QRCode
from .forms import NewLinkForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import Http404
from django.db.models import Q

import qrcode
from io import BytesIO

from django.core.mail import EmailMessage

import os

import random
import string


import cloudinary
import cloudinary.uploader
from django.views.decorators.http import require_http_methods
from django.conf import settings
import base64

from dotenv import load_dotenv


load_dotenv()


def generate_short_url(length=7):
    chars = string.digits + string.ascii_letters
    short_url = "".join(random.choice(chars) for x in range(length))

    return short_url


def index(request):
    shortened_url = ""
    long_url = ""
    host = request.build_absolute_uri()
    if "?" in host:
        host = host.split("?")[0]
    query = ""
    linky = ""

    if request.user.is_authenticated:
        my_urls = Link.objects.filter(user_id=request.user)
    else:
        my_urls = ""

    links = Link.objects.all()

    if request.method == "POST":
        if request.POST["concern"] == "url_shortener":
            long_url = request.POST.get("long_url")
            short_url = generate_short_url()

            while True:
                try:
                    link_instance = get_object_or_404(Link, short_url=short_url)
                    short_url = generate_short_url()
                except:
                    break

            form = NewLinkForm(request.POST)

            if form.is_valid():
                link = form.save(commit=False)
                link.short_url = short_url
                if request.user.is_authenticated:
                    link.user_id = request.user
                else:
                    link.user_id = User.objects.get(username=os.getenv("USUARIO"))

                link.save()

                qr_data = long_url
                size = int(request.POST.get("size", 300))
                fill_color = request.POST.get("fill_color", "black")
                back_color = request.POST.get("back_color", "white")

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)

                img = qr.make_image(fill_color=fill_color, back_color=back_color)

                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)

                public_id = f"qr_{hash(qr_data)}_{size}"

                upload_result = cloudinary.uploader.upload(
                    buffer,
                    folder="qr_codes/",
                    public_id=public_id,
                    overwrite=True,
                    resource_type="image",
                )

                qr_instance = QRCode.objects.create(
                    link_id=link,
                    public_id=upload_result["public_id"],
                    size=size,
                    fill_color=fill_color,
                    back_color=back_color,
                )

                qr_instance.qr_image = upload_result["public_id"]
                qr_instance.save()

                linky = link

            shortened_url = f"{host}{short_url}"

        elif request.POST["concern"] == "contact":
            name = request.POST["name"]
            sender = (request.POST["email"],)
            subject = request.POST["subject"]
            message = request.POST["message"]
            receiver = (os.environ.get("CONTACT_EMAIL"),)

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=receiver[0],
                to=receiver,
                reply_to=sender,
            )

            email.send()

            return redirect("core:index")

        elif request.POST["concern"] == "my_urls_form":
            query_btn = request.POST["btn"].split()

            if query_btn[0] == "delete":
                linky = get_object_or_404(Link, id=query_btn[1])
                linky.delete()

            elif query_btn[0] == "edit":
                input_short_url = request.POST[f"input_short_url {query_btn[1]}"]
                input_long_url = request.POST[f"input_long_url {query_btn[1]}"]
                linky = get_object_or_404(Link, id=query_btn[1])

                while True:
                    try:
                        link_instance = get_object_or_404(
                            Link, short_url=input_short_url
                        )

                        if link_instance == linky:
                            raise Http404

                        print("error")

                        return redirect("core:index")
                    except Http404:
                        linky.short_url = input_short_url
                        linky.long_url = input_long_url

                        linky.save()

                        break

            elif query_btn[0] == "btn_qr_code":
                link_instance = Link.objects.get(id=query_btn[1])

                qr_data = link_instance.long_url
                size = int(request.POST.get("size", 300))
                fill_color = request.POST.get("fill_color", "black")
                back_color = request.POST.get("back_color", "white")

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)

                img = qr.make_image(fill_color=fill_color, back_color=back_color)

                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)

                public_id = f"qr_{hash(qr_data)}_{size}"

                upload_result = cloudinary.uploader.upload(
                    buffer,
                    folder="qr_codes/",
                    public_id=public_id,
                    overwrite=True,
                    resource_type="image",
                )

                qr_instance = QRCode.objects.create(
                    link_id=link_instance,
                    public_id=upload_result["public_id"],
                    size=size,
                    fill_color=fill_color,
                    back_color=back_color,
                )

                qr_instance.qr_image = upload_result["public_id"]
                qr_instance.save()

            return redirect("core:index")

        elif request.POST["concern"] == "btn_group":
            form = ""
            linky_id = request.POST["linky"]
            link_instance = Link.objects.get(id=linky_id)

            qr_data = link_instance.long_url
            size = int(request.POST.get("size", 300))
            fill_color = request.POST.get("fill_color", "black")
            back_color = request.POST.get("back_color", "white")

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=fill_color, back_color=back_color)

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            public_id = f"qr_{hash(qr_data)}_{size}"

            upload_result = cloudinary.uploader.upload(
                buffer,
                folder="qr_codes/",
                public_id=public_id,
                overwrite=True,
                resource_type="image",
            )

            qr_instance = QRCode.objects.create(
                link_id=link_instance,
                public_id=upload_result["public_id"],
                size=size,
                fill_color=fill_color,
                back_color=back_color,
            )

            qr_instance.qr_image = upload_result["public_id"]
            qr_instance.save()

    else:
        form = NewLinkForm()
        query = request.GET.get("query", "")

        if query:
            my_urls = my_urls.filter(
                Q(short_url__icontains=query) | Q(long_url__icontains=query)
            )

    if linky:
        linky_qr_code = QRCode.objects.get(link_id=linky)

    else:
        linky_qr_code = ""

    context = {
        "shortened_url": shortened_url,
        "long_url": long_url,
        "form": form,
        "my_urls": my_urls,
        "host": host,
        "query": query,
        "linky": linky,
        "linky_qr_code": linky_qr_code,
    }

    return render(request, "core/index.html", context)
    # return render(request, "core/index_2.html", context)


def redirect_url(request, short_url):
    link = Link.objects.get(short_url=short_url)
    long_url = link.long_url

    if long_url:
        return redirect(long_url)
    else:
        error = "URL not found 404"
        return redirect(index, error)

    return redirect(index)


def signout(request):
    logout(request)
    return redirect("core:index")


def quick_login(request, guest=True):
    if guest:
        user = authenticate(
            request,
            username=os.getenv("USUARIO"),
            password=os.getenv("PASSWORD"),
        )

    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST.get("password1"),
        )

    login(request, user)
    return redirect("core:index")


def signup(request):
    if request.method == "POST":
        if request.POST["guest"] == "true":
            return quick_login(request)

        else:
            form = UserCreationForm(request.POST)

            if form.is_valid():
                form.save()
                return quick_login(request, False)

            else:
                context = {}
                return render(request, "core/signup.html", context)

    else:
        context = {}

        return render(request, "core/signup.html", context)


def signin(request):
    if request.method == "GET":
        context = {}

        return render(request, "core/signin.html", context)

    else:
        if request.POST["guest"] == "true":
            return quick_login(request)

        else:
            form = AuthenticationForm(request.POST)
            error = ""

            try:
                user = get_object_or_404(User, username=request.POST["username"])

                user = authenticate(
                    request,
                    username=user.username,
                    password=request.POST["password"],
                )

                if user:
                    login(request, user)
                    return redirect("core:index")

                else:
                    error = "Sorry, your password was incorrect. Please double-check your password."

            except Http404:
                error = "There is no user registered with that username."

            context = {"error": error}
            return render(request, "core/signin.html", context)


def profile(request):
    pass
