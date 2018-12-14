from django.shortcuts import redirect
from django.urls import reverse_lazy

def home(request):
    return redirect(reverse_lazy('admin:index'))
    # return render(request, 'core/index.html')
