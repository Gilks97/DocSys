from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

from docSys_app.forms import AddMemberForm, EditMemberForm
from docSys_app.models import CustomUser, Staffs, Houses, Voices, Members


def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_house(request):
    return render(request,"hod_template/add_house_template.html")

def add_house_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        house=request.POST.get("house")
        try:
            house_model=Houses(house_name=house)
            house_model.save()
            messages.success(request,"Successfully Added House")
            return HttpResponseRedirect(reverse("add_house"))
        except:
            messages.error(request,"Failed To Add House")
            return HttpResponseRedirect(reverse("add_house"))

def add_member(request):
    form=AddMemberForm()
    return render(request,"hod_template/add_member_template.html",{"form":form})

def add_member_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddMemberForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract fields from form
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_start = form.cleaned_data["session_start"]
            house_id = form.cleaned_data["house"]
            voice_id = form.cleaned_data["voice"]   # ✅ new field
            sex = form.cleaned_data["sex"]

            # Save profile picture
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                # Create custom user of type 3 (Member)
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    last_name=last_name,
                    first_name=first_name,
                    user_type= 3   # ✅ stored as string
                )

                # Fill extra details in Member profile
                user.members.address = address
                user.members.session_start_year = session_start
                user.members.gender = sex
                user.members.profile_pic = profile_pic_url

                # Assign House
                house_obj = Houses.objects.get(id=house_id)
                user.members.house_id = house_obj

                # Assign Voice ✅
                voice_obj = Voices.objects.get(id=voice_id)
                user.members.voice_id = voice_obj

                # Save user + member
                user.save()

                messages.success(request, "Successfully Added Member")
                return HttpResponseRedirect(reverse("add_member"))
            except Exception as e:
                print("❌ Error Adding Member:", e)  # helpful for debugging
                messages.error(request, "Failed to Add Member")
                return HttpResponseRedirect(reverse("add_member"))
        else:
            # Reload form with validation errors
            return render(
                request,
                "hod_template/add_member_template.html",
                {"form": form}
            )



def add_voice(request):
    return render(request, "hod_template/add_voice_template.html")


def add_voice_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        voice_name = request.POST.get("voice_name")

        try:
            voice = Voices(voice_name=voice_name)
            voice.save()
            messages.success(request, "Successfully Added Voice")
            return HttpResponseRedirect(reverse("add_voice"))
        except Exception as e:
            messages.error(request, f"Failed to Add Voice: {str(e)}")
            return HttpResponseRedirect(reverse("add_voice"))


def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_member(request):
    members=Members.objects.all()
    return render(request,"hod_template/manage_member_template.html",{"members":members})

def manage_house(request):
    houses=Houses.objects.all()
    return render(request,"hod_template/manage_house_template.html",{"houses":houses})

def manage_voice(request):
    voices=Voices.objects.all()
    return render(request,"hod_template/manage_voice_template.html",{"voices":voices})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def delete_staff(request, staff_id):
    try:
        user = CustomUser.objects.get(id=staff_id)

        # Safety check: only allow deleting staff
        if user.user_type != 2:
            messages.error(request, "Cannot delete. Selected user is not a staff member.")
            return HttpResponseRedirect(reverse("manage_staff"))

        user.delete()  # Deletes staff + linked profile
        messages.success(request, "Staff deleted successfully.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Staff does not exist.")
    except Exception as e:
        messages.error(request, f"Error deleting staff: {str(e)}")

    return HttpResponseRedirect(reverse("manage_staff"))


def edit_member(request,member_id):
    request.session['member_id']=member_id
    member=Members.objects.get(admin=member_id)
    form=EditMemberForm()
    form.fields['email'].initial=member.admin.email
    form.fields['first_name'].initial=member.admin.first_name
    form.fields['last_name'].initial=member.admin.last_name
    form.fields['username'].initial=member.admin.username
    form.fields['address'].initial=member.address
    form.fields['house'].initial=member.house_id.id
    form.fields['sex'].initial=member.gender
    form.fields['session_start'].initial=member.session_start_year
    return render(request,"hod_template/edit_member_template.html",{"form":form,"id":member_id,"username":member.admin.username})

def edit_member_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        member_id = request.session.get("member_id")
        if member_id is None:
            return HttpResponseRedirect(reverse("manage_member"))

        form = EditMemberForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_start = form.cleaned_data["session_start"]
            house_id = form.cleaned_data["house"]
            sex = form.cleaned_data["sex"]
            voice_id = form.cleaned_data["voice"]  # ✅ new field for voices

            # Handle profile picture
            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # Update user details
                user = CustomUser.objects.get(id=member_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                # Update member details
                member = Members.objects.get(admin=member_id)
                member.address = address
                member.session_start_year = session_start
                member.gender = sex

                # Assign house
                house = Houses.objects.get(id=house_id)
                member.house_id = house

                # ✅ Assign voice
                voice = Voices.objects.get(id=voice_id)
                member.voice_id = voice

                if profile_pic_url is not None:
                    member.profile_pic = profile_pic_url

                member.save()

                del request.session['member_id']
                messages.success(request, "Successfully Edited Member")
                return HttpResponseRedirect(reverse("edit_member", kwargs={"member_id": member_id}))

            except Exception as e:
                messages.error(request, f"Failed to Edit Member: {e}")
                return HttpResponseRedirect(reverse("edit_member", kwargs={"member_id": member_id}))
        else:
            form = EditMemberForm(request.POST)
            member = Members.objects.get(admin=member_id)
            return render(request, "hod_template/edit_member_template.html", {
                "form": form,
                "id": member_id,
                "username": member.admin.username
            })


def delete_member(request, member_id):
    try:
        user = CustomUser.objects.get(id=member_id)

        # Safety check: only allow deleting members
        if user.user_type != 3:
            messages.error(request, "Cannot delete. Selected user is not a member.")
            return HttpResponseRedirect(reverse("manage_member"))

        user.delete()  # Cascades & deletes linked Member profile
        messages.success(request, "Member deleted successfully.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Member does not exist.")
    except Exception as e:
        messages.error(request, f"Error deleting member: {str(e)}")

    return HttpResponseRedirect(reverse("manage_member"))

def edit_voice(request, voice_id):
    voice = Voices.objects.get(id=voice_id)
    return render(request, "hod_template/edit_voice_template.html", {"voice": voice, "id": voice_id})


def edit_voice_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        voice_id = request.POST.get("voice_id")
        voice_name = request.POST.get("voice_name")

        try:
            voice = Voices.objects.get(id=voice_id)
            voice.voice_name = voice_name
            voice.save()

            messages.success(request, "Successfully Edited Voice")
            return HttpResponseRedirect(reverse("edit_voice", kwargs={"voice_id": voice_id}))
        except Exception as e:
            messages.error(request, f"Failed to Edit Voice: {str(e)}")
            return HttpResponseRedirect(reverse("edit_voice", kwargs={"voice_id": voice_id}))


def delete_voice(request, voice_id):
    try:
        voice = Voices.objects.get(id=voice_id)
        
        # Check if members are assigned to this voice
        if Members.objects.filter(voice_id=voice).exists():
            messages.error(request, "Cannot delete voice. It has members assigned.")
            return HttpResponseRedirect(reverse("manage_voice"))
            
        # If no members, safe to delete
        voice.delete()
        messages.success(request, "Voice deleted successfully.")
    except Voices.DoesNotExist:
        messages.error(request, "Voice does not exist.")
    except Exception as e:
        messages.error(request, f"Error deleting voice: {str(e)}")
    
    return HttpResponseRedirect(reverse("manage_voice"))


def edit_house(request,house_id):
    house=Houses.objects.get(id=house_id)
    return render(request,"hod_template/edit_house_template.html",{"house":house,"id":house_id})

def edit_house_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        house_id=request.POST.get("house_id")
        house_name=request.POST.get("house")

        try:
            house=Houses.objects.get(id=house_id)
            house.house_name=house_name
            house.save()
            messages.success(request,"Successfully Edited House")
            return HttpResponseRedirect(reverse("edit_house",kwargs={"house_id":house_id}))
        except:
            messages.error(request,"Failed to Edit House")
            return HttpResponseRedirect(reverse("edit_house",kwargs={"house_id":house_id}))
        
def delete_house(request, house_id):
    try:
        house = Houses.objects.get(id=house_id)

        # Check if the house is referenced by Members before deleting
        if Members.objects.filter(house_id=house).exists():
            messages.error(request, "Cannot delete house. It has members assigned.")
            return HttpResponseRedirect(reverse("manage_house"))

        house.delete()
        messages.success(request, "House deleted successfully.")
    except Houses.DoesNotExist:
        messages.error(request, "House does not exist.")
    except Exception as e:
        messages.error(request, f"Error deleting house: {str(e)}")

    return HttpResponseRedirect(reverse("manage_house"))


