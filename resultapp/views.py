from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404 




# Create your views here.


def index(request):
      return render(request , 'index.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')  # Safely using .get() method
        password = request.POST.get('password')  # Safely using .get() method

        if username and password:  # Ensure both fields are provided
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                error = "Invalid credentials or not authorized."
        else:
            error = "Both fields are required."
    
    return render(request, 'admin_login.html', {'error': error})


def admin_dashboard(request):
      if not request.user.is_authenticated:
        return redirect('admin-login')
      return render(request,"admin_dashboard.html" )


def admin_logout(request):
      logout(request)
      return redirect('admin-login')


@login_required
def create_class(request):
      if request.method == 'POST':
            try:
             class_name = request.POST.get('classname')
             class_numeric = request.POST.get('classnamenumberic')
             section= request.POST.get('section')
             Class.objects.create(class_name=class_name,class_numeric=class_numeric,section=section)
             messages.success(request,"Class Created Successfully ")
             return redirect('create_class') 
            except Exception as e:
                  messages.error(request,f"Something went wrong:{str(e)}")
                  return redirect('create_class') 
      return render(request ,"create_class.html")




@login_required
# def manage_classes(request):
#       classes=Class.objects.all()
#       return render(request ,"manage_classes.html",locals())
# def manage_classes(request):
#     classes = ClassModel.objects.all()
#     return render(request, 'manage_classes.html', locals())  # ✅ calls the function and returns a dict


@login_required
def manage_classes(request):
    classes = Class.objects.all()
    if request.GET.get('delete'):
         try:
            class_id = request.GET.get('delete')
            class_obj= get_object_or_404(Class ,id=class_id)
            class_obj.delete()
            messages.success(request , "Class deleted succsessfully")
            return redirect('manage_classes')
         except Exception as e:
           messages.error(request, f"Something went wrong:{str(e)}")
           return redirect('manage_classes')
    return render(request, "manage_classes.html", locals())  # ✅ now you're passing a dict



@login_required
def edit_class(request , class_id):
      class_obj = get_object_or_404(Class, id=class_id)
      if request.method == 'POST':
          
            class_name = request.POST.get('classname')
            class_numeric = request.POST.get('classnamenumberic')
            section= request.POST.get('section')
           
            try:
             class_obj.class_name = class_name
             class_obj.class_numeric = class_numeric
             class_obj.section = section
            
             class_obj.save()
 
             messages.success(request,"Class update Successfully ")
             return redirect('manage_classes') 
            except Exception as e:
                  messages.error(request,f"Something went wrong:{str(e)}")
                  return redirect('edit_class') 
      return render(request ,"edit_class.html" , locals())

@login_required
def create_subject(request):
      if request.method == 'POST':
            try:
             subject_name = request.POST.get('subjectname')
             subject_code = request.POST.get('subjectcode')
             Subject.objects.create(subject_name=subject_name,
             subject_code=subject_code)
             messages.success(request,"subject Created Successfully ")
             return redirect('create_subject') 
            except Exception as e:
                  messages.error(request,f"Something went wrong:{str(e)}")
                  return redirect('create_subject') 
      return render(request ,"create_subject.html")


@login_required
def manage_subject(request):
    classes = Subject.objects.all()
    if request.GET.get('delete'):
         try:
            subject_id = request.GET.get('delete')
            subject_obj= get_object_or_404(Subject ,id=subject_id)
            subject_obj.delete()
            messages.success(request , "subject deleted succsessfully")
            return redirect('manage_subject')
         except Exception as e:
           messages.error(request, f"Something went wrong:{str(e)}")
           return redirect('manage_subject')
    return render(request, "manage_subject.html", locals())


@login_required
def edit_subject(request , subject_id):
      subject_obj = get_object_or_404(Subject, id=subject_id)
      if request.method == 'POST':
          
            subject_name = request.POST.get('subjectname')
            subject_code = request.POST.get('subjectcode')
            
           
            try:
             subject_obj.class_name = subject_name
             subject_obj.class_numeric = subject_code
             subject_obj.save()
 
             messages.success(request,"Subject update Successfully ")
             return redirect('manage_classes') 
            except Exception as e:
                  messages.error(request,f"Something went wrong:{str(e)}")
                  return redirect('edit_class') 
      return render(request ,"edit_subject.html" , locals())


@login_required
def add_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            subject_id = request.POST.get('subject')

            # ✅ Correct field name used: 'student_class_id'
            StudentCombination.objects.create(
                student_class_id=class_id,
                subject_id=subject_id,
                status=1
            )

            messages.success(request, "Subject combination added successfully!")
            return redirect('create_subject')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('add_subject_combination')

    return render(request, "add_subject_combination.html", {
        'classes': classes,
        'subjects': subjects
    })



@login_required
def manage_subject_combination(request):
    combinations = StudentCombination.objects.all()
    aid = request.GET.get('aid')
    if request.GET.get('aid'):
         try:
            StudentCombination.objects.filter(id=aid).update(status = 1)
         
            messages.success(request , "subject combination activated succsessfully")
            return redirect('manage_subject')
         except Exception as e:
           messages.error(request, f"Something went wrong:{str(e)}")
           return redirect('manage_subject_combination')
         
    did = request.GET.get('aid')
    if request.GET.get('did'):
         try:
            StudentCombination.objects.filter(id=did).update(status = 0)
         
            messages.success(request , "subject combination deactivated succsessfully")
            return redirect('manage_subject')
         except Exception as e:
           messages.error(request, f"Something went wrong:{str(e)}")
           return redirect('manage_subject_combination')



    return render(request, "manage_subject_combination.html", locals())






@login_required
def add_student(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        try:
            name = request.POST.get('fullname')
            roll_id = request.POST.get('rollid')
            email_id = request.POST.get('emailid')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            class_id = request.POST.get('class')
            
            student_class = Class.objects.get(id=class_id)

            # ✅ Correct field name used: 'student_class_id'
            Student.objects.create(
                name=name,
                roll_id=roll_id,
                gender=gender,
                dob=dob,
                student_class=student_class,
               
            )

            messages.success(request, "student added successfully!")
            return redirect('create_subject')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('add_subject_combination')

    return render(request, "add_student.html", {
        'classes': classes,
        'subjects': subjects
    })





@login_required
def manage_students(request):
    students = Student.objects.all()
    
    return render(request, "manage_students.html", locals())



@login_required
def edit_student(request , student_id):
      student_obj = get_object_or_404(Student, id=student_id)
      if request.method == 'POST':
           
            try:
             
             
             student_obj.name = request.POST.get('fullname')
             student_obj.roll_id = request.POST.get('rollid')
             student_obj.email = request.POST.get('emailid')
             student_obj.gender = request.POST.get('gender')
             student_obj.dob = request.POST.get('dob')
             student_obj.status = request.POST.get('status')
 
             messages.success(request,"student update Successfully ")
             return redirect('manage_classes') 
            except Exception as e:
                  messages.error(request,f"Something went wrong:{str(e)}")
                  return redirect('manage_student') 
      return render(request ,"edit_student.html" , locals())