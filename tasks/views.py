from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from rest_framework import viewsets, serializers, filters
from .models import Task
from .forms import TaskForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Account created. Please sign in.')
        return redirect('login')
    return render(request, 'form.html', {'form':form,'heading':'Create your account','button':'Create account'})

@login_required
def dashboard(request):
    all_tasks = Task.objects.filter(owner=request.user)
    tasks = all_tasks
    q = request.GET.get('q','').strip()
    status = request.GET.get('status','')
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status:
        tasks = tasks.filter(status=status)
    page = Paginator(tasks, 8).get_page(request.GET.get('page'))
    return render(request, 'dashboard.html', {'page':page,'q':q,'status':status,'statuses':Task.Status.choices,'total':all_tasks.count(),'progress':all_tasks.filter(status='progress').count(),'done':all_tasks.filter(status='done').count()})

class OwnedMixin(LoginRequiredMixin):
    model = Task
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

class TaskCreate(OwnedMixin, CreateView):
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'heading':'Create a task','button':'Save task'}
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Task created.')
        return super().form_valid(form)

class TaskUpdate(OwnedMixin, UpdateView):
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'heading':'Edit task','button':'Save changes'}
    def form_valid(self, form):
        messages.success(self.request, 'Changes saved.')
        return super().form_valid(form)

class TaskDetail(OwnedMixin, DetailView):
    template_name = 'detail.html'

class TaskDelete(OwnedMixin, DeleteView):
    template_name = 'delete.html'
    success_url = reverse_lazy('dashboard')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title','description','status','priority','due_date','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title','description']
    ordering_fields = ['created_at','due_date','title']
    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user)
        status = self.request.query_params.get('status')
        return qs.filter(status=status) if status else qs
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
