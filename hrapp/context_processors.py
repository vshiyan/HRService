from hrapp.models import Worker


def role(request):
    if request.user.is_authenticated:
        work = Worker.objects.get(user=request.user)
        return {'role': work.role}
    else:
        return {'role': 'unk'}
