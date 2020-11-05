#Pytorch
import torch
import torchvision
from torchvision import transforms
#ML net
from ml_models.net import Net
#image Managment
from PIL import Image
import requests
from io import BytesIO

def load_model():
    #pretrained model path
    PATH = 'ml_models/model.pth'
    # Initializate model
    model = Net(64)
    #Call pretrained model from path
    model.load_state_dict(torch.load(PATH))
    model.eval()
    return model


def transform_image(path):
    '''
    Make specific tranformations to an image
    in order to pass through the net.
    '''
    #Trasnformations
    preprocess = transforms.Compose ([
                                    transforms.Resize(64),
                                    transforms.CenterCrop(64),
                                    transforms.ToTensor(),
                                    transforms.Normalize(
                                        mean = [0.485, 0.456, 0.406],
                                        std = [0.229, 0.224, 0.225]
                                    )])
    #get response from url
    response = requests.get(path)
    #Open image & convert to rgb
    img = Image.open(BytesIO(response.content)).convert('RGB')
    #Pass through preprocess
    img_t = preprocess(img)
    #Flat tensor
    processed_img = torch.unsqueeze(img_t, 0)

    return processed_img

def predict(img, model):
    #Stablishing all Moto cathegories
    CATHEGORIES = ['off_road',
                    'naked',
                    'scooter',
                    'scrambler',
                    'cafe_racer',
                    'cruiser',
                    'sport',
                    'touring',
                    'bike',
                    'quad']
    #Call prediciton from model
    outputs = model(img)
    _, predicted = torch.max(outputs, 1)

    return CATHEGORIES[predicted]
