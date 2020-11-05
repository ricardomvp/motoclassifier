#Standard libraries
import os
import hashlib
from datetime import datetime
#django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
#apps
from apps.home.models import Image
#ml functions
from utils.moto_clf import load_model, transform_image, predict
#utilities
from utils.utilities import pagination
#aws
from utils.upload import upload_to_aws

# /home
def home(request,page):

    page = int(page)
    #How many elements to display
    elements_to_display = 10
    #Return how many pages and which images will be displayed
    pages, images = pagination(page, elements_to_display)

    if request.method == 'POST':
        #Create a random string to rename the picture
        string = str(datetime.now())
        new_string = hashlib.sha256(string.encode()).hexdigest()
        # Get image name
        img = request.FILES['image']
        #split image name in name & extension
        complement, ext = img.name.split('.')
        #Change image name to a new string & extension
        img.name = new_string + '.' + ext

        # storage image to aws
        upload_to_aws(img)

        #Create new object in db Image
        new_image = Image.objects.create()
        # Get aws bucket url
        BUCKET_URL = os.environ.get('BUCKET_URL')
        '''
        Call image-processing to transform image with required characteristics
        for model
        '''
        processed_img =  transform_image(BUCKET_URL + img.name)
        #Call ML model
        model = load_model()
        #Call prediction from the ML net
        prediction = predict(processed_img, model)
        #title of new image
        bucket_url = BUCKET_URL + img.name
        #set title
        new_image.bucket_url = bucket_url
        #Set prediction into db from net prediction
        new_image.cathegory = prediction
        #Save the new object
        new_image.save()

        context = {'images' : images,
                    'pages' : pages,
                    'success' : 'Image was succesfully upload'}
        return redirect('/')
    else:
        context = {'images' : images,
                    'pages' : pages}
        return render(request, 'base/home.html', context)

# /home/process_all_images
def process_all_images(request):
    '''
    when home/process_all_images is called
    all images are pased through ml net again
    in order to set a new pred from the image.
    That's useful when a new ML model is charged.
    '''
    #Call all images from db
    images = Image.objects.all()
    #sort images
    images = images.order_by('-image_id')
    #Call ml model
    model = load_model()

    for image in images:
        # set img as object from Image db
        img = Image.objects.get(image_id = image.image_id)
        #transform image
        processed_img =  transform_image(img.bucket_url)
        #Call prediciton
        prediction = predict(processed_img, model)
        #set new pred in prediction fiel from db
        img.cathegory = prediction
        #Save object
        img.save()
    #Return to home
    return redirect('/')
