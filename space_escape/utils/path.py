import os.path


ASSETS_BASEPATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)),
    'assets'
)


def get_asset_path(asset_path):
    return os.path.join(ASSETS_BASEPATH, asset_path)
