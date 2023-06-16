#!/bin/bash
screen -dmS training_screen bash -c 'cd $HOME/pytorch-cifar;$HOME/anaconda3/bin/serve run cifar_inference:image_model'
