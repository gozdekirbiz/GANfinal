import torch
import torch.nn as nn
import numpy as np  # linear algebra
import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms
from io import BytesIO
from django.core.files.base import ContentFile
import cv2
import matplotlib.pyplot as plt


class ConvBlock(torch.nn.Module):
    def __init__(
        self,
        input_size,
        output_size,
        kernel_size=3,
        stride=2,
        padding=1,
        activation="relu",
        batch_norm=True,
    ):
        super(ConvBlock, self).__init__()
        self.conv = torch.nn.Conv2d(
            input_size, output_size, kernel_size, stride, padding
        )
        self.batch_norm = batch_norm
        self.bn = torch.nn.InstanceNorm2d(output_size)
        self.activation = activation
        self.relu = torch.nn.ReLU(True)
        self.lrelu = torch.nn.LeakyReLU(0.2, True)
        self.tanh = torch.nn.Tanh()

    def forward(self, x):
        if self.batch_norm:
            out = self.bn(self.conv(x))
        else:
            out = self.conv(x)

        if self.activation == "relu":
            return self.relu(out)
        elif self.activation == "lrelu":
            return self.lrelu(out)
        elif self.activation == "tanh":
            return self.tanh(out)
        elif self.activation == "no_act":
            return out


class DeconvBlock(torch.nn.Module):
    def __init__(
        self,
        input_size,
        output_size,
        kernel_size=3,
        stride=2,
        padding=1,
        output_padding=1,
        activation="relu",
        batch_norm=True,
    ):
        super(DeconvBlock, self).__init__()
        self.deconv = torch.nn.ConvTranspose2d(
            input_size, output_size, kernel_size, stride, padding, output_padding
        )
        self.batch_norm = batch_norm
        self.bn = torch.nn.InstanceNorm2d(output_size)
        self.activation = activation
        self.relu = torch.nn.ReLU(True)

    def forward(self, x):
        if self.batch_norm:
            out = self.bn(self.deconv(x))
        else:
            out = self.deconv(x)
        if self.activation == "relu":
            return self.relu(out)
        elif self.activation == "lrelu":
            return self.lrelu(out)
        elif self.activation == "tanh":
            return self.tanh(out)
        elif self.activation == "no_act":
            return out


class ResnetBlock(torch.nn.Module):
    def __init__(self, num_filter, kernel_size=3, stride=1, padding=0):
        super(ResnetBlock, self).__init__()
        conv1 = torch.nn.Conv2d(num_filter, num_filter, kernel_size, stride, padding)
        conv2 = torch.nn.Conv2d(num_filter, num_filter, kernel_size, stride, padding)
        bn = torch.nn.InstanceNorm2d(num_filter)
        relu = torch.nn.ReLU(True)
        pad = torch.nn.ReflectionPad2d(1)

        self.resnet_block = torch.nn.Sequential(pad, conv1, bn, relu, pad, conv2, bn)

    def forward(self, x):
        out = self.resnet_block(x)
        return out


class Generator(torch.nn.Module):
    def __init__(self, input_dim, num_filter, output_dim, num_resnet):
        super(Generator, self).__init__()

        # Reflection padding
        self.pad = torch.nn.ReflectionPad2d(3)
        # Encoder
        self.conv1 = ConvBlock(
            input_dim, num_filter, kernel_size=7, stride=1, padding=0
        )
        self.conv2 = ConvBlock(num_filter, num_filter * 2)
        self.conv3 = ConvBlock(num_filter * 2, num_filter * 4)
        # Resnet blocks
        self.resnet_blocks = []
        for i in range(num_resnet):
            self.resnet_blocks.append(ResnetBlock(num_filter * 4))
        self.resnet_blocks = torch.nn.Sequential(*self.resnet_blocks)
        # Decoder
        self.deconv1 = DeconvBlock(num_filter * 4, num_filter * 2)
        self.deconv2 = DeconvBlock(num_filter * 2, num_filter)
        self.deconv3 = ConvBlock(
            num_filter,
            output_dim,
            kernel_size=7,
            stride=1,
            padding=0,
            activation="tanh",
            batch_norm=False,
        )

    def forward(self, x):
        # Encoder
        enc1 = self.conv1(self.pad(x))
        enc2 = self.conv2(enc1)
        enc3 = self.conv3(enc2)
        # Resnet blocks
        res = self.resnet_blocks(enc3)
        # Decoder
        dec1 = self.deconv1(res)
        dec2 = self.deconv2(dec1)
        out = self.deconv3(self.pad(dec2))
        return out

    def normal_weight_init(self, mean=0.0, std=0.02):
        for m in self.children():
            if isinstance(m, ConvBlock):
                torch.nn.init.normal_(m.conv.weight, mean, std)
            if isinstance(m, DeconvBlock):
                torch.nn.init.normal_(m.deconv.weight, mean, std)
            if isinstance(m, ResnetBlock):
                torch.nn.init.normal_(m.conv.weight, mean, std)
                torch.nn.init.constant_(m.conv.bias, 0)


class CycleGANGenerator:
    def __init__(self, type):
        if type == "monet":
            path = "ganapp/static/monetb.pth"
        if type == "cezanne":
            path = "ganapp/static/cezanneb.pth"
        if type == "ukiyoe":
            path = "ganapp/static/ukiyoeb.pth"
        if type == "vangogh":
            path = "ganapp/static/vangoghb.pth"

        self.device = torch.device("cpu")
        self.generator = Generator(3, 32, 3, 6)

        print(path)
        # Load the whole state_dict
        loaded_state = torch.load(path, map_location=self.device)
        self.generator.load_state_dict(loaded_state)
        self.generator = self.generator.to(self.device)
        self.generator.eval()

    def forward(self, image_path):
        image = Image.open(image_path)

        transform = transforms.Compose(
            [
                # transforms.Resize((256, 256)),  # Modelin giriş boyutuna göre yeniden boyutlandırma
                transforms.ToTensor(),  # Tensor formatına dönüştürme
                # transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Normalizasyon
            ]
        )
        processed_image = transform(image).unsqueeze(0)

        with torch.no_grad():
            generated_image = self.generator(processed_image)

        generated_image = generated_image.squeeze(0)  # Batch boyutunu kaldırın
        generated_image = (
            generated_image.detach().cpu().numpy()
        )  # Tensor'ı NumPy dizisine dönüştürün
        generated_image = (
            generated_image + 1
        ) / 2  # [0, 1] aralığına getirin (0 ile 1 arasında normalize edilmiş)
        generated_image = generated_image.transpose(1, 2, 0)
        generated_image = (generated_image * 255).astype(
            np.uint8
        )  # uint8 veri tipine dönüştürün
        print(generated_image)
        cv2.imwrite("kaydedilen_gorsel.jpg", generated_image)

        result_image_pil = Image.fromarray(generated_image)
        output_io = BytesIO()
        result_image_pil.save(output_io, format="PNG")
        return ContentFile(output_io.getvalue(), "cartoonized.png")
