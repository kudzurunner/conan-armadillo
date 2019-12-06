from conans import ConanFile, CMake, tools
import os
import shutil

class ArmadilloConan(ConanFile):
    name = "armadillo"
    version = "9.800.3"
    license = "http://arma.sourceforge.net/license.html"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-armadillo"
    description = "Armadillo is a high quality linear algebra library (matrix maths) for the C++ language, aiming towards a good balance between speed and ease of use"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    source_name = "{}-{}".format(name, version)
    build_name = "build"
    exports = (
        "patches/*.patch")
    suffix = ""

    def requirements(self):
        self.requires.add('hdf5/1.10.5@kudzurunner/stable')
        self.requires.add('openblas/0.3.7@kudzurunner/stable')

    def source(self):
        url_template = "http://sourceforge.net/projects/arma/files/{}"
        archive_name = "{}.tar.xz".format(self.source_name)

        url = url_template.format(archive_name)
        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

        tools.patch(base_path=self.source_name, patch_file="patches/openblas.patch")

        self.suffix = ("_d" if self.settings.build_type == "Debug" else "")
        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_name), "project(armadillo CXX C)",
                              '''project(armadillo CXX C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(NOT CMAKE_DEBUG_POSTFIX)
  set(CMAKE_DEBUG_POSTFIX %s)
endif()''' % self.suffix)

    def build(self):
        os.mkdir(self.build_name)
        shutil.move("conanbuildinfo.cmake", self.build_name)

        config = "{}/include/armadillo_bits/config.hpp".format(self.source_name)
        tools.replace_in_file(file_path=config, search="// #define ARMA_USE_HDF5", replace="#define ARMA_USE_HDF5")
        tools.replace_in_file(file_path=config, search="#define ARMA_USE_HDF5_ALT", replace="// #define ARMA_USE_HDF5_ALT")

        if self.settings.build_type == "Release":
            tools.replace_in_file(file_path=config, search="// #define ARMA_NO_DEBUG", replace="#define ARMA_NO_DEBUG")

        cmake = CMake(self)
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.configure(source_folder=self.source_name, build_folder=self.build_name)
        cmake.build()

    def package(self):
        self.copy("*", dst="include", src="{}/include".format(self.source_name))
        self.copy("*.lib", dst="lib", src=self.build_name, keep_path=False)
        self.copy("*.dll", dst="bin", src=self.build_name, keep_path=False)
        self.copy("*.so", dst="lib", src=self.build_name, keep_path=False)
        self.copy("*.dylib", dst="lib", src=self.build_name, keep_path=False)
        self.copy("*.a", dst="lib", src=self.build_name, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
