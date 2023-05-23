import ruamel.yaml
import os
from abc import abstractmethod

# the latest tag is: the latest language version + the latest os version, usually the last indices

###############################
#            Config           #
###############################
dragonwell8_latest_version  = ["8.15.6", "ga"]
dragonwell11_latest_version = ["11.0.19.15", "ga"]
dragonwell17_latest_version = ["17.0.7.0.7+7", "ga"]

os__versions = {
    "anolis": ["8.6", "8.8"],
    "alinux": ["3"],
    "centos": ["7"],
    "ubuntu": ["20.04"],
    "alpine": ["3.16"],
}

def is_latest_os_version(os_name, os_version):
    return os__versions[os_name][-1] == os_version


registry_config = {
    "anolis": ["dragonwell", "anolis"],
    "alinux": ["dragonwell", "alinux"],
    "centos": ["dragonwell"],
    "ubuntu": ["dragonwell"],
    "alpine": ["dragonwell"],
}

tags_basic = [
    "{FULL_VERSION}-{EDITION}-{GA}-{OS}{OS_VERSION}{SLIM}",   # e.g. 8.14.15-(extended/standard)-ga-anolis(-8.6)(-slim)
    "{MAJOR_VERSION}-{EDITION}-{GA}-{OS}{OS_VERSION}{SLIM}",  # e.g. 8-(extended/standard)-ga-anolis(-8.6)(-slim)
]

tag_major_version_os_alias = "{MAJOR_VERSION}-{OS}{SLIM}"     # e.g. 8-anolis(-slim)
tag_major_version_alias = "{MAJOR_VERSION}{SLIM}"             # e.g. 8(-slim)
tag_latest = "latest"

###############################
#           Generator         #
###############################

TYPE = "configs"
IMAGES = "images"
FOLDER = "folder"
DOCKERFILE = "dockerfile"
BUILDS = "builds"
ARGS = "args"
TAGS = "tags"
REGISTRIES = "registries"

# class hierarchy:
#
# Dragonwell
#   |
#   ---> Dragonwell8
#   |       |
#   |       --->  Dragonwell8_Standard
#   |       |
#   |       --->  Dragonwell8_Extended
#   |
#   ---> Dragonwell11
#   |       |
#   |       --->  Dragonwell11_Standard
#   |       |
#   |       --->  Dragonwell11_Extended
#   |
#   ---> Dragonwell17
#           |
#           --->  Dragonwell17_Standard

class Dockerfile:
    def __init__(self, name, is_slim):
        self.name = name
        self.is_slim = is_slim


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class Dragonwell():
    def __init__(self):
        pass

    @abstractmethod
    def major_version(self):
        pass

    @abstractmethod
    def latest_full_version(self):
        pass

    @abstractmethod
    def edition(self):
        pass

    def major_version_edition(self):
        return self.major_version() + "-" + self.edition()   # e.g. 8-extended

    def folder(self):
        return self.major_version_edition()

    def os_versions(self):
        return os__versions

    def registries(self):
        return registry_config

    @abstractmethod
    def dockerfiles(self, os_name):
        pass

    def tag_patterns(self, os_name, os_version, is_slim):
        return tags_basic


class Dragonwell8(Dragonwell):
    def major_version(self):
        return "8"

    def latest_full_version(self):
        return dragonwell8_latest_version

    def dockerfiles(self, os_name):
        list = [Dockerfile("Dockerfile", False)]
        # currently only anolis images have slim versions
        if os_name == "anolis":
            list.append(Dockerfile("Dockerfile.slim", True))
        return list

    def os_versions(self):
        os_versions = os__versions.copy()
        # JDK8 does not have alpine
        os_versions.pop("alpine")
        return os_versions


class Dragonwell11(Dragonwell):
    def major_version(self):
        return "11"

    def latest_full_version(self):
        return dragonwell11_latest_version

    def dockerfiles(self, os_name):
        list = [Dockerfile("Dockerfile", False)]
        # currently only anolis images have slim versions
        if os_name == "anolis":
            list.append(Dockerfile("Dockerfile.slim", True))
        return list


class Dragonwell17(Dragonwell):
    def major_version(self):
        return "17"

    def latest_full_version(self):
        return dragonwell17_latest_version

    def dockerfiles(self, os_name):
        # JDK17 currently does not have slim versions
        return [Dockerfile("Dockerfile", False)]


###############################
# Concrete classes

class Dragonwell8_Standard(Dragonwell8):
    def edition(self):
        return "standard"


class Dragonwell8_Extended(Dragonwell8):
    def edition(self):
        return "extended"

    def tag_patterns(self, os_name, os_version, is_slim):
        tags = super().tag_patterns(os_name, os_version, is_slim).copy()
        if is_latest_os_version(os_name, os_version):
            tags.append(tag_major_version_os_alias)
            if os_name == "anolis":
                tags.append(tag_major_version_alias)
        return tags


class Dragonwell11_Standard(Dragonwell11):
    def edition(self):
        return "standard"


class Dragonwell11_Extended(Dragonwell11):
    def edition(self):
        return "extended"

    def tag_patterns(self, os_name, os_version, is_slim):
        tags = super().tag_patterns(os_name, os_version, is_slim).copy()
        if is_latest_os_version(os_name, os_version):
            tags.append(tag_major_version_os_alias)
            if os_name == "anolis":
                tags.append(tag_major_version_alias)
                if is_slim == False:
                    tags.append(tag_latest)
        return tags


class Dragonwell17_Standard(Dragonwell17):
    def edition(self):
        return "standard"

    def tag_patterns(self, os_name, os_version, is_slim):
        tags = super().tag_patterns(os_name, os_version, is_slim).copy()
        if is_latest_os_version(os_name, os_version):
            tags.append(tag_major_version_os_alias)
            if os_name == "anolis":
                tags.append(tag_major_version_alias)
        return tags

###############################

class NoAliasDumper(ruamel.yaml.representer.RoundTripRepresenter):
    def ignore_aliases(self, data):
        return True


class ConfigGenerator:
    def __init__(self, dw):
        self.dw = dw

    def generate_object(self):
        dw = self.dw
        object = {}
        for os_name in dw.os_versions():          # e.g. anolis/alinux
            images = []
            object[os_name] = {
                REGISTRIES: dw.registries()[os_name],
                IMAGES: images
            }
            for os_version_idx in range(len(dw.os_versions()[os_name])):
                os_version = dw.os_versions()[os_name][os_version_idx]         # e.g. 8.6 (for anolis)
                mangled_os_version = "-" + os_version
                folder = os.path.join(dw.folder(), os_name + os_version)       # e.g. 8-standard/anolis8.6
                for dockerfile in dw.dockerfiles(os_name):                     # e.g. Dockerfile
                    dockefile_name = dockerfile.name
                    slim_postfix = ""
                    if dockerfile.is_slim:
                        slim_postfix = "-slim"
                    # fill dockerfile info
                    dockerfile_path = os.path.join(folder, dockefile_name)
                    assert os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), dockerfile_path)), (dockerfile_path + " doesn't exist!")
                    dockerfile_object = {
                        DOCKERFILE: dockerfile_path,
                        BUILDS: []
                    }
                    images.append(dockerfile_object)
                    # fill tag info
                    tags = []
                    for tag_pattern in dw.tag_patterns(os_name, os_version, dockerfile.is_slim):
                        tags.append(tag_pattern.format_map(SafeDict(MAJOR_VERSION=dw.major_version(),
                                                                    FULL_VERSION=dw.latest_full_version()[0],
                                                                    EDITION=dw.edition(),
                                                                    GA=dw.latest_full_version()[1],
                                                                    OS=os_name,
                                                                    OS_VERSION=mangled_os_version,
                                                                    SLIM=slim_postfix)))
                    # append tags
                    dockerfile_object[BUILDS].append({
                        TAGS: tags
                    })
        return object


class Assembler:
    def __init__(self, array):
        self.root = {
            "dragonwell": {}
        }
        for dw in array:
            major_version_edition = dw.major_version_edition()
            obj = ConfigGenerator(dw).generate_object()
            self.root["dragonwell"][major_version_edition] = obj

    def generate(self):
        file_pwd = os.path.dirname(os.path.realpath(__file__))
        # dump YAML
        with open(os.path.join(file_pwd, 'versions.yaml'), 'w') as f:
            yml = ruamel.yaml.YAML()
            yml.preserve_quotes = False
            yml.Representer = NoAliasDumper
            yml.dump(self.root, f)


Assembler([
    Dragonwell8_Standard(),
    Dragonwell8_Extended(),
    Dragonwell11_Standard(),
    Dragonwell11_Extended(),
    Dragonwell17_Standard(),
]).generate()