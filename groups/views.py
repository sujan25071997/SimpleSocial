from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionsRequiredMixin)
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from groups.models import Group,GroupMember

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group.slug=self.kwargs.get('slug'))

        try:
            GroupMember.Objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'warning already a member!')
        else:
            messages.success(self.request,'You are now a member!')

        return super().get(request,*args,**kwargs)
