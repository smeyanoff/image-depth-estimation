import os

import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
from PIL import Image
import re

import settings
# from depth_estimator.glpn import glpn_model
from depth_estimator.midas import midas_estimator


def depth_visualization_save(image, depth, img_name, save_path):

    """
    Save .jpg files illustrated depth estimation
    """

    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(image)
    ax[0].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    ax[1].imshow(depth, cmap="plasma")
    ax[1].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    plt.tight_layout()

    plt.savefig(os.path.join(save_path, img_name))


def depth_object_save(image, depth, img_name, save_path):

    """
    Save mesh objects
    """

    image = Image.open(image)

    width, height = image.size

    depth_image = (depth * 255 / np.max(depth)).astype("uint8")
    image = np.array(image)

    # create rgbd image
    depth_o3d = o3d.geometry.Image(depth_image)
    image_o3d = o3d.geometry.Image(image)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        image_o3d, depth_o3d, convert_rgb_to_intensity=False
    )

    # camera settings
    camera_intrinsic = o3d.camera.PinholeCameraIntrinsic()
    camera_intrinsic.set_intrinsics(width, height, 500, 500, width / 2, height / 2)

    # create point cloud
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic)

    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=20.0)
    pcd = pcd.select_by_index(ind)

    # estimate normals
    pcd.estimate_normals()
    pcd.orient_normals_to_align_with_direction()

    # surface reconstruction
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=10, n_threads=1
    )[0]

    # rotate the mesh
    rotation = mesh.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    mesh.rotate(rotation, center=(0, 0, 0))

    # save the mesh
    o3d.io.write_triangle_mesh(
        os.path.join(save_path, img_name.replace("jpg", "obj").replace("png", "obj")), mesh
    )


def main(
    photo_dir, photo_save_path, object_save_path, depth_estimator_weights_path, device
):

    photo_dir = photo_dir
    dir_files = os.listdir(photo_dir)

    depth_estimator = midas_estimator("DPT_Large", device)

    for photo_file_name in dir_files:

        if re.match('.+depth.+', photo_file_name) is not None:
            continue

        stock_image = os.path.join(photo_dir, photo_file_name)

        image = depth_estimator.image_prepare(stock_image)
        depth = depth_estimator.predict_depth(image)

        depth_visualization_save(image, depth, photo_file_name, photo_save_path)

        depth_object_save(stock_image, depth, photo_file_name, object_save_path)


if __name__ == "__main__":

    main(
        settings.PHOTO_DIR,
        settings.SAVE_DEPTH_PRED_PATH,
        settings.SAVE_OBJ_PATH,
        settings.DEPTH_ESTIMATOR_WEIGHTS_PATH,
        settings.DEVICE,
    )
