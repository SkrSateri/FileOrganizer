from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import UploadFileForm, searchFormByAllInfo
from .models import File, FileBlob
from commonClasses.resultMessages import ResultMessage
import datetime, os, mimetypes


# Create your views here.

def deleteFileResults_view(request, otdid):#view to delete file from database
    fileToDelete = File.objects.get(id = otdid)
    fileBlobToDelete = FileBlob.objects.get(id = otdid)
    fileToDelete.delete()
    fileBlobToDelete.delete()
    return redirect('searchFile')#deleteFileResults_view
        
def downloadFile_view(request, oid):#view to download file
    #geting selected objects from file database
    fileDetails = File.objects.get(id = oid)
    fileContext = FileBlob.objects.get(id = oid)

    #declaring blobdata, file extention and file name to variables
    fileContent = fileContext.fileBlob
    fileExtention = fileContext.fileExtention
    fileName = str(fileDetails.fileName) + str(fileDetails.fileContent)

    #preparing file and responsing with it
    response = HttpResponse(fileContent, content_type=fileExtention)
    response['Content-Disposition'] = "attachment ; filename = %s" % fileName
    return response#downloadFile_view

def searchFile_view(request, *args, **kwargs):#To search file on database and send data to template
    #sessionCheck
    if request.session.get('username') == None:
        return redirect('login')
    else:
        None

    #if statement to check if there is a request or not
    #if there is a request return result on searchResults
    if request.POST:
        resultTemplate = True
    else:
        resultTemplate = False

    #Getting the post requests from forms sepereatly asssigning them to variable 
    form = searchFormByAllInfo(request.POST or None, use_required_attribute=False)
    fileNameForm = request.POST.get('fileName')
    fileUploaderNameForm = request.POST.get('lastUploadBy')
    fileUploadDateForm = request.POST.get('uploadDate')
    fileQuery = None
    show = setShow(False)

    #message for show results
    resultMessage = ResultMessage(None,"resultMessage  somehow not Working")

    #evaluation of form
    #Using try to find files with provided informations from forms
    #if it finds put it into a list and return that list 
    #exept cant find the file in database.
    
    #if begin-------------------------
    
    if str(fileNameForm) == "" and str(fileUploaderNameForm) == "":#search by date 
        try:
            fileQuery = File.objects.filter(uploadDate = fileUploadDateForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('lastUploadBy')
            form = searchFormByAllInfo(None, use_required_attribute=False)
        except:    
            fileQuery = None
    elif str(fileNameForm) == "" and str(fileUploadDateForm) == "":#search by uploader name
        try:
            fileQuery = File.objects.filter(lastUploadBy = fileUploaderNameForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('lastUploadBy')
            form = searchFormByAllInfo(None, use_required_attribute=False)
        except:    
            fileQuery = None
    elif str(fileUploaderNameForm) == "" and str(fileUploadDateForm) == "":# search by filename
        try:
            fileQuery = File.objects.filter(fileName = fileNameForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('lastUploadBy')
            form = searchFormByAllInfo(None, use_required_attribute=False)
        except:    
            fileQuery = None
    elif str(fileNameForm) == "":# search by uploader name and date
        try:
            fileQuery = File.objects.filter(lastUploadBy = fileUploaderNameForm, uploadDate = fileUploadDateForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('lastUploadBy')
            form = searchFormByAllInfo(None, use_required_attribute=False)
        except:    
            fileQuery = None
    elif str(fileUploaderNameForm) == "":# search by uploader filename and date
        try:
            fileQuery = File.objects.filter(fileName = fileNameForm, uploadDate = fileUploadDateForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('lastUploadBy')
            form = searchFormByAllInfo(None, use_required_attribute=False)
        except:    
            fileQuery = None
    elif str(fileUploadDateForm) == "":#search by uploader name and file name
        try:
            fileQuery = File.objects.filter(lastUploadBy = fileUploaderNameForm, fileName = fileNameForm,).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('lastUploadBy')
            form = searchFormByAllInfo(None, use_required_attribute=False)
        except:    
            fileQuery = None
    elif str(fileUploaderNameForm) != "" and str(fileUploadDateForm) != "" and str(fileNameForm) != "":
        try:
            fileQuery = File.objects.filter(fileName = fileNameForm, uploadDate = fileUploadDateForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('lastUploadBy')
            form = searchFormByAllInfo(None, use_required_attribute=False)
        except:    
            fileQuery = None
    #if end----------------------------
    
    #the if statement to manage display(hide or show it) value of result div
    show = setShow(True)
    
    #if statement to manage resultMessage
    if not fileQuery:
        resultMessage = ResultMessage(False, 'There is no such a file')
        

    #variables to send template for rendering
    context = {
        'form': form,
        'resultMessage': resultMessage,
        'fileQuery': fileQuery,
        'show': show
    }

    #if statement to return result on search result template
    if  resultTemplate:
        return render(request, 'searchResults.html', context)
    else:
        None

    return render(request, 'searchFile.html', context)#searchFile_view
        
        
#Funchtion to set result divs css id
def setShow(x):
    if x:
        return 'searchResultsDivision'
    else:
        return 'searchResultsDivisionHide'#setShow


def uploadFile_view(request, *args, **kwargs):#Upload file to database
    #session check
    if request.session.get('username') == None:
        return redirect('login')
    else:
        None
    
    #assigning form
    form = UploadFileForm(request.POST, request.FILES or None)
    resultMessage = None

    #if the form is valid and useable, app gets all the data from request and assign to variables
    #trys to get file with same name to see if its already exist or not
    #if there is return reject message and form with current post
    #if its not exist saves the data to sql database
    if form.is_valid():
        fileNameForm = request.POST.get('fileName')
        fileDescriptionForm = request.POST.get('fileDescription')
        fileContentForm = request.FILES.get('fileContent')
        lastUploadByForm = (request.session.get('name') + " " + request.session.get('surname'))
        uploadDateForm = datetime.datetime.today().strftime('%Y-%m-%d')
        fileNameWizard = str(fileContentForm.name)
        split_tup = os.path.splitext(fileNameWizard)
        try:
            if File.objects.get(fileName = fileNameForm):
                form = UploadFileForm(request.POST)
                resultMessage = ResultMessage(False, "There is already a file with this name!")
        except:
            try:
                #saving file details
                newFile = File(fileName = fileNameForm, fileDescription = fileDescriptionForm, lastUploadBy = lastUploadByForm, uploadDate = uploadDateForm, fileContent = split_tup[1])
                newFile.save()

                #saving blob
                mime_type, _ = mimetypes.guess_type(request.FILES['fileContent'].name)
                fileBlob = FileBlob(fileBlob = request.FILES['fileContent'].read(), fileExtention = mime_type)
                fileBlob.save()
                #----------

                resultMessage = ResultMessage(True, "File is uploaded successfuly!")
                form = UploadFileForm(None)
            except:
                resultMessage = ResultMessage(False, "An error occured, please try again.")
    context = {
        'form': form,
        'resultMessage': resultMessage,
    }
    return render(request, 'uploadFile.html', context)#UploadFile_view
