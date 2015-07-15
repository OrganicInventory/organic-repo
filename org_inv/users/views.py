from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView, View
from .forms import UserForm, ProfileForm
from inventory.views import get_prod_data, get_all_service_data
from .models import Profile, get_profile

# Create your views here.

class AddUserView(View):

    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, "register.html", {"form1": user_form, "form2": profile_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            password = user.password
            user.set_password(password)
            user.save()

            user = authenticate(username=user.username,
                                password=password)

            login(self.request, user)
            return redirect("all_products")
        else:
            return render(request, "register.html", {"form1": user_form, "form2": profile_form})


class ShowUserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'show_user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@login_required
def edit_profile(request):
    profile = get_profile(request.user)
    if request.method == "GET":
        profile_form = ProfileForm(instance=profile)
    elif request.method == "POST":
        profile_form = ProfileForm(instance=profile, data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
    product_data = get_prod_data(request)
    service_data = get_all_service_data(request)
    return render(request, "edit_profile.html", {"form": profile_form, 'data1': product_data, 'data2': service_data})


