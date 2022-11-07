from depth_estimator.glpn import glpn_model
import os
import matplotlib.pyplot as plt
import settings

def depth_visualization_save(
    image, 
    depth, 
    img_name, 
    save_path
):

    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(image)
    ax[0].tick_params(
        left=False, 
        bottom=False, 
        labelleft=False, 
        labelbottom=False
    )
    ax[1].imshow(
        depth, 
        cmap='plasma'
    )
    ax[1].tick_params(
        left=False, 
        bottom=False, 
        labelleft=False, 
        labelbottom=False
    )
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            save_path, 
            img_name
        )
    )


def main(
    photo_dir,
    save_path,
    depth_estimator_weights_path
):

    photo_dir = photo_dir
    dir_files = os.listdir(photo_dir)

    depth_estimator = glpn_model(
        depth_estimator_weights_path
    )

    for photo_file_name in dir_files:

        stock_image = os.path.join(
            photo_dir,
            photo_file_name 
        )

        image = depth_estimator.image_prepare(stock_image)
        depth = depth_estimator.predict_depth(image)

        depth_visualization_save(
            image, 
            depth, 
            photo_file_name,
            save_path
        )


if __name__ == "__main__":

    main(
        settings.PHOTO_DIR,
        settings.SAVE_PATH,
        settings.DEPTH_ESTIMATOR_WEIGHTS_PATH
    )