from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from django.contrib import messages
from .forms import UploadFileForm
from django.conf import settings # A.settings.py
import os

class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': products})

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/detail.html', {'product': product})

class BucketHome(View):
    template_name = 'home/bucket.html'
    
    def get(self, request):
        form = UploadFileForm()
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects, 'form': form})
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            filename = file.name
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            path = os.path.join(settings.MEDIA_ROOT, "uploads", filename)

            with open(path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            tasks.upload_object_task.delay(path, filename)
            messages.success(request, f"Uploading {filename} ...", 'info')
            return redirect('home:bucket')

class DeleteBucketObject(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, f"your object {key} will be deleted soon.", 'info')
        return redirect('home:bucket')
    
class DownloadBucketObject(View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, f"your object {key} will be downloaded soon.", 'info')
        return redirect('home:bucket')