from django.shortcuts import render, redirect

from django.views import View

from django.core.paginator import Paginator

from ecommerce.models import Category, Product, Cart

from cms.models import Banner, Page, Brand

from .forms import SignUpForm, CommentForm

from django.http import JsonResponse

from .serializers import CategorySerializer

from django.contrib.auth.mixins import LoginRequiredMixin


# function based view parameters: request, slug
# class based view: two functions generally: get and post these are two built in functions, we should give same name


class BaseView(View):
    template_context = {
        'categories': Category.objects.order_by('title').all(),
        # here if we give Category.objects.all() it will load but without ordering by title
        'navbar_pages': Page.objects.filter(navbar=True)
    }


class Homepage(BaseView):
    def get(self, request):
        if request.session.get('show_ad', 1) == 1:  # here close_ad is name from urls
            request.session['show_ad'] = True

        self.template_context['banners'] = Banner.objects.filter(published=True).order_by(
            '-weight')  # here published field ko naam ho, weight pani feild ko naam ho jasko weight badi xa tei dekinxa suru ma
        self.template_context['latest_products'] = Product.objects.order_by('-pub_date')[:10]
        self.template_context['top_sellers'] = Product.objects.order_by('?')[:3]  # here ? means random
        self.template_context['recently_viewed'] = Product.objects.order_by('?')[:3]
        self.template_context['top_new_products'] = Product.objects.order_by('-id')[:3]

        self.template_context['brands'] = Brand.objects.all()

        print('I am from session', request.session['show_ad'])

        return render(request, 'index.html', self.template_context)


class CategoryWise(BaseView):
    def get(self, request, category_slug):
        print(category_slug)
        self.template_context['category'] = Category.objects.get(slug=category_slug)
        category_product_list = Category.objects.get(slug=category_slug).product_set.all()
        paginator = Paginator(category_product_list, 4)
        page = request.GET.get('page', 1)
        self.template_context['category_pages'] = paginator.get_page(page)
        print(paginator.page_range)
        self.template_context['paginator'] = paginator
        return render(request, 'category-wise.html', self.template_context)


class ProductView(BaseView):

    def get(self, request, product_slug):
        print(product_slug)
        product = Product.objects.get(slug=product_slug)
        self.template_context['product'] = product  # check out mathi ko line
        self.template_context['related_products'] = product.category.product_set.all()[
                                                    :5]  # here small p product as we are using object of above line
        # self.template_context['related_products'] = Product.objects.get(slug=product_slug).category.product_set.all()[:5]
        # print(product.image()) #for testing
        self.template_context['latest_products'] = Product.objects.order_by('-id')[:5]
        return render(request, 'single-product.html', self.template_context)

    def post(self, request, product_slug):  # this is for saving comment
        form = CommentForm(request.POST)
        if form.is_valid():
            product_review = form.save(
                commit=False)  # save le database ma save garxa, commit le directly database ma save gardaina
            product_review.user = request.user
            product_review.product = Product.objects.get(slug=product_slug)
            product_review.save()

        return redirect('/product/' + product_slug)


class SearchView(BaseView):

    def get(self, request):
        q = request.GET.get('q', None)
        if not q:
            return redirect('/home')

        self.template_context['search_results'] = Product.objects.filter(
            title__icontains=q)  # __icontains means case insensitive, and filter returns a new QuerySet containing objects that match the given lookup parameters
        return render(request, 'search-results.html', self.template_context)


class SignUpView(BaseView):
    def get(self, request):
        self.template_context['form'] = SignUpForm()
        return render(request, 'registration/register.html', self.template_context)  # here now while

    # submitting we get 405 error ie. method not allowed as we only have get method in this class

    def post(self, request):  # now when method is post this is executed
        form = SignUpForm(request.POST)
        if not form.is_valid():
            self.template_context[
                'form'] = form  # this provides our form that we populated with error message, if we provide SignUp() then we get no prepopulated form
            return render(request, 'registration/register.html', self.template_context)

        form.save()
        return redirect('/accounts/login')


class CategoryApiView(View):
    def get(self, request):
        return JsonResponse(CategorySerializer(Category.objects.all(), many=True).data,
                            safe=False)  # here many means more than one so array/list of category


class CartView(LoginRequiredMixin,
               BaseView):  # yo view ma jana login chainxa, keep LoginMixin before base view other base view overrides it

    def get(self, request):
        self.template_context['cart_items'] = Cart.objects.filter(user=request.user).order_by('-id')
        self.template_context['latest_products'] = Product.objects.order_by('-id')[:5]
        self.template_context['intrested_products'] = Product.objects.order_by('?')[:2]

        total_amount = 0

        for cart_item in self.template_context['cart_items']:
            total_amount += cart_item.total()
        self.template_context['total_amount'] = total_amount
        return render(request, 'cart.html', self.template_context)

    def post(self, request):
        item = Cart()
        product = Product.objects.get(pk=request.POST.get('product_id'))
        item.product = product
        item.qty = request.POST.get('qty')
        item.user = request.user
        item.save()
        return redirect('/cart')


class CloseAdView(View):
    def post(self, request):
        request.session['show_ad'] = False
        return redirect('/')
