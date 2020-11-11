import os
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt


def getPathSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
            # print(f)
    return size

# def getPathName(path):
#     path_cur_list = os.listdir(path)
#     for path_cur in path_cur_list:
#         path_full = os.path.join(path, path_cur)
#         if(os.path.isdir(path_full)):
#             getPathName(path_full)
#         else:
#             print(path_full)

pure_path_list = []
pure_path_size_list = []
def getPurePath(path):
    '''
    Get pure path and size.
    '''
    global pure_path_list, pure_path_size_list
    path_cur_list = os.listdir(path)
    for path_cur in path_cur_list:
        path_full = os.path.join(path, path_cur)
        if(os.path.isdir(path_full)):
            path_down_list = os.listdir(path_full)
            down_dir_exist_flag = 0
            for path_down in path_down_list:
                path_down_full = os.path.join(path_full, path_down)
                if(os.path.isdir(path_down_full)):
                    down_dir_exist_flag = 1
                    break
            if(down_dir_exist_flag == 1):
                getPurePath(path_full)
            else:
                pure_path_list.append(path_full)
                pure_path_size_list.append(getPathSize(path_full))
                

def fixCtSliceType(slicePath, savePath):
    slice_reader = sitk.ImageSeriesReader()
    slice_file_names = slice_reader.GetGDCMSeriesFileNames(slicePath)
    slice_reader.SetFileNames(slice_file_names)
    input_ct_image = slice_reader.Execute()
    input_ct_array = sitk.GetArrayFromImage(input_ct_image)
    print("max:", np.max(input_ct_array))
    plt.imshow(np.squeeze(np.mean(input_ct_array, axis=1)))
    plt.savefig("/home/leko/Desktop/tmp/{}.png".format(item))
    plt.clf()

    output_ct_array = input_ct_array.astype(np.int16)
    output_ct_image = sitk.GetImageFromArray(output_ct_array)
    output_ct_image.SetOrigin(input_ct_image.GetOrigin())
    output_ct_image.SetSpacing(input_ct_image.GetSpacing())
    print(output_ct_image.GetOrigin(), output_ct_image.GetSpacing(), input_ct_array.dtype, output_ct_array.dtype)
    sitk.WriteImage(output_ct_image, savePath)


if __name__ == '__main__':
    root_path = "/media/leko/Elements SE/LIDC-IDRI"
    item_list = os.listdir(root_path)
    for item in item_list:
        item_path = os.path.join(root_path, item)
        pure_path_list = []
        pure_path_size_list = []
        getPurePath(item_path)
        ct_slice_path = pure_path_list[np.argmax(pure_path_size_list)]
        print(pure_path_list)
        print(pure_path_size_list)
        print(np.argmax(pure_path_size_list))
        print(ct_slice_path)

        fixCtSliceType(ct_slice_path, "/media/leko/Elements SE/LIDC-IDRI-CT/{}.nii.gz".format(item))
