import os
import torch
os.chdir("/project/segmentation/smcho1201/segmentation_project/web_segmentation")

def create_model(model_name):
    if model_name == "colonsegnet":
        from models.pop_medical_seg_models.ColonSegNet import CompNet as ColonSegNet
        model = ColonSegNet()
        return model
    
    if model_name == "deeplabv3":
        from models.pop_seg_models.DeepLab_V3_p.model import DeepLab as DeepLab_V3_p
        model = DeepLab_V3_p(backbone = 'resnet', num_classes = 1)   # backbone : 선택 (resnet, xception, mobilenet)
#         check_points_dict = torch.load('pth')
#         weights = check_points_dict['weight']
#         model.weights(
        return model
        
    if model_name == "esfpnet":
        from models.sotor_medical_seg_models.ESFPNet.ESFPmodel import ESFPNetStructure
        model = ESFPNetStructure(embedding_dim = 224)
        return model
    
    if model_name == "fcbformer":
        from models.sotor_medical_seg_models.FCBformer.FCBmodels import FCBFormer
        model = FCBFormer(size=224)
        return model
        
    if model_name == "fcn":
        from models.pop_seg_models.FCN.models.segmentation.fcn import fcn_resnet101
        model = fcn_resnet101(num_classes = 1)
        return model
        
#     if model_name == "segnet":
#         from models.pop_seg_models.SegNet.models.segnet import SegResNet
#         model = SegResNet(num_classes = 1)
#         return model
    
    if model_name == "unet":
        from models.pop_medical_seg_models.unet import UNet
        model = UNet(n_channels=3, n_classes=1, pretrained = True)
        path = './models/pop_medical_seg_models/unet_carvana_scale0.5_epoch2.pth'
        device = torch.device('cpu')
        
        state_dict = torch.load(path, map_location=device)
        state_dict.popitem()
        state_dict.popitem()
        model.load_state_dict(state_dict)
        
        model.add_output_layer()
        
        return model
    
    if model_name == "unet++":
        from models.pop_medical_seg_models.nnunet import Nested_UNet as UNet_2p
        model = UNet_2p(1,3)
        return model
    
        
    
    ### 보류
    if model_name == "colonformer":
        os.chdir('models/sotor_medical_seg_models/ColonFormer')
        from colon_lib.models.segmentors.colonformer import ColonFormer
        from colon_lib.models.decode_heads.uper_head import UPerHead
        
        backbone=dict(type='mit_b3',style='pythorch')

        decode_head=dict(type='UPerHead', in_channels=[64], in_index=[0], channels=128, dropout_ratio=0.1,
                            num_classes=1, norm_cfg=dict(type='BN', requires_grad=True), align_corners=False,decoder_params=dict(embed_dim=768),
                            loss_decode=dict(type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0))


        model = ColonFormer(backbone,decode_head = decode_head,
                        neck=None,
                        auxiliary_head=None,
                        train_cfg=dict(),
                        test_cfg=dict(mode='whole'),
                        pretrained='colon_lib/pretrained/mit_b3.pth')
        return model
    
    