from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import SearchForm, UploadFileForm, searchFormByUploader, searchFormByUploadDate
from .models import File, FileBlob
from commonClasses.resultMessages import ResultMessage
import datetime, os, mimetypes


# Create your views here.

def downloadFile_view(request, oid):
    #saving file from blob dat
    fileDetails = File.objects.get(id = oid )
    fileContext = FileBlob.objects.get(id = oid)
    fileContent = fileContext.fileBlob
    fileExtention = fileContext.fileExtention
    filePath = str(fileDetails.fileContent)
    fileWrite = open(filePath, 'wb')
    fileWrite.write(fileContent)

    #Sending Download Request
    filename = str(fileDetails.fileName)
    fl = open(filePath, 'rb')
    mime_type, _ = mimetypes.guess_type(filePath)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment ; filename = %s" % filename
    return response

def searchFile_view(request, *args, **kwargs):
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
    form = SearchForm(request.POST or None)
    searchByName = searchFormByUploader(request.POST or None)
    searchByDate = searchFormByUploadDate(request.POST or None)
    fileNameForm = request.POST.get('fileName')
    fileUploaderNameForm = request.POST.get('lastUploadBy')
    fileUploadDateForm = request.POST.get('uploadDate')
    fileQuery = None
    show = setShow(False)

    #message for show results
    resultMessage = ResultMessage(None,"resultMessage Not Working")

    #evaluation of form
    #Using try to find files with provided informations from forms
    #if it finds put it into a list and return that list 
    #exept cant find the file in database.
    if form.is_valid():#validation of FileName form
        try:
            fileQuery = File.objects.filter(fileName = fileNameForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('fileName')
            form = SearchForm(None)
        except:    
            fileQuery = None
        
        #the if statement to manage display(hide or show it) value of result div
        show = setShow(True)

    if searchByName.is_valid():#validation of SearchByNameForm
        try:
            fileQuery = File.objects.filter(lastUploadBy = fileUploaderNameForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('fileName')
            searchByName = searchFormByUploader(None)
        except:
            fileQuery = None
        
        #the if statement to manage display(hide or show it) value of result div
        show = setShow(True)

    if searchByDate.is_valid():#validation of SearchByDateForm
        try:
            fileQuery = File.objects.filter(uploadDate = fileUploadDateForm).values('id', 'fileName', 'uploadDate', 'fileDescription' , 'lastUploadBy').order_by('fileName')
            searchByDate = searchFormByUploadDate(None)
        except:
            fileQuery = None

        #the if statement to manage display(hide or show it) value of result div
        show = setShow(True)
    
    #if statement to manage resultMessage
    if not fileQuery:
        resultMessage = ResultMessage(False, 'There is no such a file')
        

    #variables to send template for rendering
    context = {
        'form': form,
        'searchByDate': searchByDate,
        'searchByName': searchByName,
        'resultMessage': resultMessage,
        'fileQuery': fileQuery,
        'show': show
    }

    #if statement to return result on search result template
    if  resultTemplate:
        return render(request, 'searchResults.html', context)
    else:
        None

    return render(request, 'searchFile.html', context)
        

#Funchtion to set result divs css id
def setShow(x):
    if x:
        return 'searchResultsDivision'
    else:
        return 'searchResultsDivisionHide'


def uploadFile_view(request, *args, **kwargs):
    if request.session.get('username') == None:
        return redirect('login')
    else:
        None
    form = UploadFileForm(request.POST, request.FILES or None)
    resultMessage = None

    if form.is_valid():
        fileNameForm = request.POST.get('fileName')
        fileDescriptionForm = request.POST.get('fileDescription')
        fileContentForm = request.FILES.get('fileContent')
        lastUploadByForm = (request.session.get('name') + " " + request.session.get('surname'))
        uploadDateForm = datetime.datetime.today().strftime('%Y-%m-%d')
        #print(request.FILES['fileContent'].path)
        try:
            if File.objects.get(fileName = fileNameForm):
                form = UploadFileForm(None)
                resultMessage = ResultMessage(False, "There is already a file with this name!")
        except:
            newFile = File(fileName = fileNameForm, fileDescription = fileDescriptionForm, lastUploadBy = lastUploadByForm, uploadDate = uploadDateForm, fileContent = fileContentForm )
            newFile.save()
            #saving blob
            uploadedFilePath = ('UploadedFile/'+request.FILES.get('fileContent').name)
            uploadedFileBlob = open(uploadedFilePath,'rb').read()
            splitedFileName, fileExtentionForm = os.path.splitext(uploadedFilePath)
            fileBlob = FileBlob(fileBlob = uploadedFileBlob, fileExtention = fileExtentionForm)
            fileBlob.save()
            #----------
            resultMessage = ResultMessage(True, "File is uploaded successfuly!")
            form = UploadFileForm(None)
    context = {
        'form': form,
        'resultMessage': resultMessage,
    }
    return render(request, 'uploadFile.html', context)
