from ray import serve

from io import BytesIO
from PIL import Image
from starlette.requests import Request
from typing import Dict

import torch
from torchvision import transforms
from torchvision.models import resnet50

from models import *
import os

@serve.deployment
class ImageModel:
    def __init__(self):
        self.model = ResNet50()
        print('==> Resuming from checkpoint..')
        assert os.path.isdir('checkpoint'), 'Error: no checkpoint directory found!'
        checkpoint = torch.load('./checkpoint/ckpt.pth')
        self.model.load_state_dict(checkpoint['net'])
        self.model.eval()

        #self.preprocessor = transforms.Compose(
        #    [
        #        transforms.Resize(224),
        #        transforms.CenterCrop(224),
        #        transforms.ToTensor(),
        #        transforms.Lambda(lambda t: t[:3, ...]),  # remove alpha channel
        #        transforms.Normalize(
        #            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        #        ),
        #    ]
        #)
        self.preprocessor = transforms.Compose([
            transforms.Resize(32),
            transforms.CenterCrop(32),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ])

    async def __call__(self, starlette_request: Request) -> Dict:
        image_payload_bytes = await starlette_request.body()
        pil_image = Image.open(BytesIO(image_payload_bytes))
        print("[1/3] Parsed image data: {}".format(pil_image))

        pil_images = [pil_image]  # Our current batch size is one
        input_tensor = torch.cat(
            [self.preprocessor(i).unsqueeze(0) for i in pil_images]
        )
        print("[2/3] Images transformed, tensor shape {}".format(input_tensor.shape))

        with torch.no_grad():
            output_tensor = self.model(input_tensor)
        print("[3/3] Inference done!")
        return {"class_index": int(torch.argmax(output_tensor[0]))}

image_model = ImageModel.bind()

