from hrapp.models import Worker


def role(request):
    if request.user.is_authenticated:
        if Worker.objects.filter(user=request.user).exists():
            work = Worker.objects.get(user=request.user)
            return {'role': work.role}
        else:
            return {'role': 'unk'}
    else:
        return {'role': 'unk'}
