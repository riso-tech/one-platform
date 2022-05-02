def site_images_directory_path(instance, filename):
    """Site images directory"""
    return "site_{0}/images/{1}".format(instance.id, filename)


def setting_images_directory_path(instance, filename):
    """Setting images directory"""
    return "setting_{0}/images/{1}".format(instance.site.id, filename)
