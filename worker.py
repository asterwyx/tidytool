import os
import shutil


class Worker(object):
    def __init__(self, working_directory: str, copy: bool = False):
        super().__init__()
        self.working_directory = working_directory
        self.groups = {}
        self.images = []
        self.copy = copy
        os.chdir(self.working_directory)

    def get_images(self, files):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext == ".tif":
                self.images.append(file)
        print(self.images)

    def get_groups(self):
        for image in self.images:
            group = image.split('_')[0]
            if group in self.groups:
                self.groups[group].append(image)
            else:
                self.groups[group] = [image]

        for k in self.groups:
            if not os.access(k, os.F_OK):
                os.mkdir(k)
        print(self.groups)

    def group(self):
        for k, v in self.groups.items():
            for image in v:
                if self.copy:
                    shutil.copy(image, k)
                else:
                    shutil.move(image, k)

    def start(self):
        files = os.listdir(self.working_directory)
        self.get_images(files)
        self.get_groups()
        self.group()

    def start_detached(self):
        pass
