from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DigitalBook
from django.http import FileResponse, Http404

@login_required
def library_list(request):
    ebooks = DigitalBook.objects.all().order_by('-uploaded_at')
    return render(request, 'library/list.html', {'ebooks': ebooks})

@login_required
def library_download(request, pk):
    ebook = get_object_or_404(DigitalBook, pk=pk)
    try:
        return FileResponse(
            ebook.file.open('rb'),
            content_type='application/pdf',
            as_attachment=False,  # True = force download, False = open in browser
            filename=ebook.filename()
        )
    except FileNotFoundError:
        raise Http404("File not found")