from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.username = data.get('username')
        user.name = data.get('name')
        # user.gender = data.get('gender')
        # user.age = data.get('age')
        user.save()
        return user