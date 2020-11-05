#Model
from apps.home.models import Image
#ml functions
from utils.moto_clf import load_model, transform_image, predict

def process_all_images():
    #Get all images from db
    images = Image.objects.all()
    #Sort images
    images = images.order_by('-image_id')
    #Load ml model
    model = load_model()

    for image in images:
        #get image
        img = Image.objects.get(image_id = image.image_id)
        #Make image transformations to load into the model
        processed_img =  transform_image(img.cover)
        #Make prediction with the tranformed image
        prediction = predict(processed_img, model)
        #Set new prediction into cathegory
        img.cathegory = prediction
        #Save changes in the model
        img.save()


import math
#Return how many pages and which images will be displayed
def pagination(page, elements_to_display):
    #Call all element from DB
    elements = Image.objects.all()
    total_elements = elements.count()
    #Calculus num of pages
    num_pages = math.ceil(total_elements/elements_to_display)
    pages = []
    for i in range(0,num_pages):
        pages.append(i+1)

    if elements_to_display*page >= total_elements:
        if total_elements > elements_to_display:
            start =elements_to_display*(num_pages-1)
        else:
            start = 0
        end = total_elements
    else:
        start=page*elements_to_display-elements_to_display
        end = page*elements_to_display

    #Call all element from DB
    elements = Image.objects.all()

    #Sort all database by image_id
    elements = elements.order_by('-image_id')
    #Split element to display
    elements = elements[start:end]
    return pages, elements
