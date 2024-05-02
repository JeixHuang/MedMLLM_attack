import pydicom
import numpy as np
import os
import cv2


def getCtHU(dicm):
    '''直接传入dicm文件/IMA文件'''
    img = np.array(dicm.pixel_array).astype('int32')
    img[img == -2000.0] = 0
    Hu = np.array(img).astype('float64')
    
    # 检查RescaleIntercept和RescaleSlope是否存在
    RescaleIntercept = dicm.RescaleIntercept if hasattr(dicm, 'RescaleIntercept') else 0
    RescaleSlope = dicm.RescaleSlope if hasattr(dicm, 'RescaleSlope') else 1
    
    if RescaleSlope != 1:
        Hu = Hu * RescaleSlope
    Hu += RescaleIntercept
    return Hu



# 下面的windowsLevelTransform()是将上面的HU转为numpy形式
def windowsLevelTransform(Hu, window, level):
    img = Hu
    min = level - float(window) * 0.5;
    max = level + float(window) * 0.5;  # 这个是CT窗口设置，相关问题百度或评论。下面调用这个函数时候，我拟定拟定窗口[-160,240]
    img[img < min] = min
    img[img > max] = max
    norm_ = (img - min) / window
    norm_.astype('float32')
    return norm_


root = r'new_imgs/Lumbar'  # 这是每个病例的路径
savepath = r'new_imgs/Lumbar1'  # 之后保存图片的路径

# # 下面遍历每个切片
# i = 0
# for filename in os.listdir(root):
#     img = pydicom.read_file(os.path.join(root, filename))  # .IMA文件
#     img_hu = getCtHU(img)  # 由.IMA文件转换成HU形式的
#     img_np = windowsLevelTransform(Hu=img_hu, window=400, level=40)  # 再由HU形式的转成.numpy形式的
#     cv2.imwrite(savepath + '\%d.png' % i, img_np * 255)  # 注意这里img_np要乘上255即img_np*255，不然保存起来的图片看起来不爽，一片黑
#
i = 0
for filename in os.listdir(root):
    img = pydicom.read_file(os.path.join(root, filename))  # .IMA文件
    img_hu = getCtHU(img)  # 由.IMA文件转换成HU形式的
    img_np = windowsLevelTransform(Hu=img_hu, window=400, level=40)  # 再由HU形式的转成.numpy形式的
    output_filename = os.path.join(savepath, '008-'+f'{i}.png')  # Use f-string to create unique filenames
    cv2.imwrite(output_filename, img_np * 255)
    i += 1  # Increment i for the next iteration
    print(f'{i}.png'+'已生成')
# ...
print('------------已生成完毕---------')
# ...


