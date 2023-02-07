import os

from django.views.generic.edit import FormView

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Audio
from .forms import PdfForm

from PyPDF2 import PdfReader, PdfFileReader
import pyttsx3
import multiprocessing
import keyboard
import pathlib

import time
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage

paused = False
myfile = ''

#settings variable
voice = 0
volume = 0.6
rate = 250

def change_settings(request):
    data = request.POST
    global voice, volume, rate
    voice = int(data['voice'])
    volume = float(data['volume'])
    rate = float(data['rate'])
    return HttpResponseRedirect('/audios')

# Create your views here.
def index(request):
    audios = Audio.objects.all()
    return render(request, 'index.html', {'audios':audios})

def play_audio(request, fl, i):
    global paused
    global myfile

    print(voice, volume, rate)

    # url = "http://127.0.0.1:8000/audios"+static('uploads/'+fl)
    url = staticfiles_storage.url('uploads/'+fl)
    url = "CrazyAudios"+url
    myfile = fl
    # print("Before Init", paused)
    # return HttpResponse(url)
    # reader = PdfReader(url+fl)
    # pdfFileObj = open(url, 'r')
    # pdfreader = PdfFileReader(pdfFileObj)
    # return HttpResponse(pdfFileObj)
    url = url.replace('%20', ' ')
    pdfreader = PdfReader(url)
    no_of_pgs = len(pdfreader.pages)
    # no_of_words = len(pdfreader)
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)

    paused = False

    # print("After Init", paused)

    content = []

    if (i == 1):
        no_of_words = 0
        for i in range(no_of_pgs):
            page = pdfreader.pages[i]
            text = page.extract_text()
            words = text.split()
            content.extend(words)
            no_of_words += len(text.split())
        # print(content)

        for n in range(0, no_of_words):
            # print("After", content[n], paused)
            if not paused:
                engine.say(content[n])
                # engine.runAndWait()
                engine.runAndWait()

        engine.stop()
    # if (i == 0):
    #     # close the original pdf file object
    #     global term
    #     term = True
    #     t.join()
        # return HttpResponse(no_of_pgs)
    # engine = pyttsx3.init()
    # for p in range(0, no_of_pgs):
    #     page = reader.pages[p]
    #     text = page.extract_text()
    #     engine.say(text)
    #     engine.runAndWait()
    return HttpResponseRedirect('/audios')

def pause_audio(request, fl, i):
    global paused
    # print("Before Init", paused)
    # print("myfile", myfile)
    # print("current file", fl)
    if myfile==fl:
        paused = True
    # print("After Paused", paused)
    return HttpResponseRedirect('/audios')
# def say(phrase):
# 	if __name__ == "__main__":
# 		p = multiprocessing.Process(target=play_audio, args=(phrase,))
# 		p.start()
# 		while p.is_alive():
# 			if keyboard.is_pressed('q'):
# 				p.terminate()
# 			else:
# 				continue
# 		p.join()


# Add new Audio

# class PdfFormView(FormView):
#     form_class = PdfForm
#     template_name = 'add-pdf.html'

def add_new_audio(request):
    pdf_form = PdfForm()
    return render(request, 'add-pdf.html', {'pdf_form': pdf_form.as_div()})

def upload_pdf(request):
    files = request.FILES.getlist('name')
    pdf_form = PdfForm(request.POST, request.FILES)
    if pdf_form.is_valid():
        for file in files:
            extn = pathlib.Path(file.name).suffix
            print('extn '+extn)
            if extn == '.pdf':
                if Audio.objects.filter(name=file.name).exists():
                    raise Exception("File already uploaded.")
                else:
                    audio = Audio()
                    audio.name = file
                    audio.save()
                    saveFile(file)
            else:
                raise Exception("File must be a pdf file!")
        return HttpResponseRedirect('/audios')
    else:
        raise Exception("Form is not valid!")

def saveFile(f):

    url = staticfiles_storage.url('uploads/')
    url = "CrazyAudios" + url
    url = url.replace('%20', ' ')
    with open(url+f.name, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

# delete single or multiple files
def delete_files(request):
    file_ids = request.POST['ids']
    ids = file_ids.split(',')
    for id in ids:
        audio = Audio.objects.get(id=id)
        url = staticfiles_storage.url('uploads/')
        audio_name = audio.name.replace('%20', ' ')
        url = "CrazyAudios" + url + audio_name
        os.remove(url)
        audio.delete()
    return HttpResponseRedirect("/audios")


