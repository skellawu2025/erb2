from django.shortcuts import render, HttpResponse
from .models import Student



# Create your views here.
def home(request):
    return render(request, 'home.html')

# view all
def students(request):
    if request.method == 'GET':
        students = Student.objects.all()

    if request.method == "POST":
        student = Student()
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.about = request.POST.get("about")
        student.pub_date = request.POST.get("pub_date")

        student.save()
        return HttpResponse("<h1>upload Successfully</h1>")

    return render(request, 'students.html', {'students': students})

def student(request, pk):
    student = Student.objects.get(pk=pk)

    if request.method == "GET":
        return render(request, 'student.html', {'student': student})

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.about = request.POST.get("about")
        student.pub_date = request.POST.get("pub_date")

        student.save()
        return HttpResponse("<h1>Student Update Successfully</h1>")

def student_delete(request):
     if request.method == "POST":
        name = request.POST.get("name")
        student = Student.objects.get(name=name)
        student.delete()
        return render(request, 'student_delete.html')

    # return HttpResponse("<h1>Student Delete Successfully</h1>")