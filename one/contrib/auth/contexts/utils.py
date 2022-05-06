def group_images_directory_path(instance, filename):
    """Group images directory"""
    return "group_{0}/images/{1}".format(instance.id, filename)


def group_context_images_directory_path(instance, filename):
    """Group context images directory"""
    return "group_context_{0}/images/{1}".format(instance.group.id, filename)
