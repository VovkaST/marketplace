from django.views import generic

from app_orders.forms import (
    OrderStep1AuthorizedForm,
    OrderStep1NotAuthorizedForm,
)


class OrderCreateView(generic.FormView):
    template_name = 'app_orders/order_create.html'

    @property
    def step(self):
        return self.request.GET.get('step')

    def get_initial(self):
        obj = self.request.user
        initial = dict()
        if self.request.user.is_authenticated:
            initial.update({
                'phone': obj.profile.phone_number,
                'patronymic': obj.profile.patronymic,
                'avatar': obj.profile.avatar,
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({
                'instance': self.request.user,
            })
        return kwargs

    def get_form_class(self):
        if not self.step:
            if self.request.user.is_authenticated:
                return OrderStep1AuthorizedForm
            return OrderStep1NotAuthorizedForm
