from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from testingformapp.models import Menu, Option
from testingformapp.forms import OptionFormSet, MenuForm, OrderForm


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        has_daily_menu = Menu.objects.has_daily_menu()
        daily_menu = Menu.objects.get_daily_menu()

        context = {
            'has_daily_menu': has_daily_menu,
            'daily_menu': daily_menu,
        }
        return render(request, 'testingformapp/home.html', context)


class MenuListView(LoginRequiredMixin, View):
    def get(self, request):
        list = Menu.objects.order_by('-day')
        context = { 'list': list }
        return render(request, 'testingformapp/menu_list.html', context)


class MenuCreateView(LoginRequiredMixin, View):
    def get(self, request):
        menu_form = MenuForm()
        options_form = OptionFormSet()

        context = {
            'menu_form': menu_form,
            'options_form': options_form,
        }

        return render(request, 'testingformapp/menu_create.html', context)

    def post(self, request):
        menu_form = MenuForm(request.POST)
        options_form = OptionFormSet(request.POST)

        if menu_form.is_valid():
            menu = menu_form.save()
            options_form = OptionFormSet(request.POST, instance=menu)

            if options_form.is_valid():
                options_form.save()

                return redirect('menu_detail', menu_id=menu.id)
        
        context = {
            'menu_form': menu_form,
            'options_form': options_form,
        }

        return render(request, 'testingformapp/menu_create.html', context)


class MenuUpdateView(LoginRequiredMixin, View):
    def get(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        menu_form = MenuForm(instance=menu)
        options_form = OptionFormSet(instance=menu)

        context = {
            'menu_form': menu_form,
            'options_form': options_form,
        }

        return render(request, 'testingformapp/menu_create.html', context)

    def post(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        menu_form = MenuForm(request.POST, instance=menu)

        if menu_form.is_valid():
            menu = menu_form.save()
            options_form = OptionFormSet(request.POST, instance=menu)

            if options_form.is_valid():
                options_form.save()

                return redirect('menu_detail', menu_id=menu.id)
        
        context = {
            'menu_form': menu_form,
            'options_form': options_form,
        }

        return render(request, 'testingformapp/menu_create.html', context)


class MenuDetailView(LoginRequiredMixin, View):
    def get(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        context = { 'menu': menu }
        return render(request, 'testingformapp/menu_detail.html', context)


class OrderCreateView(View):
    def get(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        form = OrderForm(menu=menu)
        context = {
            'menu': menu,
            'form': form,
        }
        return render(request, 'testingformapp/order_create.html', context)
    
    def post(self, request, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id)
        form = OrderForm(request.POST, menu=menu)

        if form.is_valid():
            order = form.save()

            context = {
                'menu': menu,
                'order': order,
            }

            return render(request, 'testingformapp/order_create_success.html', context)

        context = {
            'menu': menu,
            'form': form,
        }
        return render(request, 'testingformapp/order_create.html', context)