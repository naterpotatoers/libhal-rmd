from conan import ConanFile
from conan.tools.files import copy
from conan.tools.layout import basic_layout
from conan.tools.build import check_min_cppstd
from conan.errors import ConanInvalidConfiguration
import os


required_conan_version = ">=1.50.0"


class LibhalRmdConan(ConanFile):
    name = "libhal-rmd"
    version = "0.3.4"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://libhal.github.io/libhal-rmd"
    description = (
        "A collection of drivers for the RMD series servos and actuators")
    topics = ("servo", "smart servo", "PID")
    settings = "compiler"
    exports_sources = "include/*"
    no_copy_source = True

    def package_id(self):
        self.info.clear()

    @property
    def _min_cppstd(self):
        return "20"

    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "11",
            "clang": "14",
            "apple-clang": "14.0.0"
        }

    def requirements(self):
        self.requires("libhal/0.3.2@")
        self.requires("libhal-util/0.3.3@")

    def validate(self):
        if self.settings.get_safe("compiler.cppstd"):
            check_min_cppstd(self, self._min_cppstd)

        def lazy_lt_semver(v1, v2):
            lv1 = [int(v) for v in v1.split(".")]
            lv2 = [int(v) for v in v2.split(".")]
            min_length = min(len(lv1), len(lv2))
            return lv1[:min_length] < lv2[:min_length]

        compiler = str(self.settings.compiler)
        version = str(self.settings.compiler.version)
        minimum_version = self._compilers_minimum_version.get(compiler, False)

        if minimum_version and lazy_lt_semver(version, minimum_version):
            raise ConanInvalidConfiguration(
                f"{self.name} {self.version} requires C++{self._min_cppstd}, which your compiler ({compiler}-{version}) does not support")

    def layout(self):
        basic_layout(self)

    def package(self):
        copy(self, "LICENSE", dst=os.path.join(
            self.package_folder, "licenses"),  src=self.source_folder)
        copy(self, "*.h", dst=os.path.join(self.package_folder, "include"),
             src=os.path.join(self.source_folder, "include"))
        copy(self, "*.hpp", dst=os.path.join(self.package_folder,
             "include"), src=os.path.join(self.source_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.set_property("cmake_target_name", "libhal::rmd")
