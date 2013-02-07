from django.shortcuts import render

def search(request):
    if 'q' not in request.GET:
        return _show_search(request)
    else:
        return _show_results(request)

def _show_search(request):
    data = None

    return render(request, 'search.html', data)

def _show_results(request):
    return render(request, 'results.html')
