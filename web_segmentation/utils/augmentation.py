from torchvision import transforms

def augmentation_train():
    _size = 224, 224
    resize = transforms.Resize(_size, interpolation=0)

    # set your transforms 
    train_transforms = transforms.Compose([
                               transforms.Resize(_size, interpolation=0),
                               transforms.RandomRotation(180),
                               transforms.RandomHorizontalFlip(0.5),
                               transforms.RandomCrop(_size, padding = 10), # needed after rotation (with original size)
                           ])
    return train_transforms




def augmentation_test():
    _size = 224, 224
    test_transforms = transforms.Compose([
                               transforms.Resize(_size, interpolation=0),
                           ])
    return test_transforms
    