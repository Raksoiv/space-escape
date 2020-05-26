from os import listdir
import os.path


ASSETS_BASEPATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)),
    'assets'
)


def get_asset_path(asset_path):
    return os.path.join(ASSETS_BASEPATH, asset_path)


def get_assets_path_folder(assets_folder):
    return [
        os.path.join(ASSETS_BASEPATH, assets_folder, asset_path)
        for asset_path in listdir(os.path.join(ASSETS_BASEPATH, assets_folder))
    ]
