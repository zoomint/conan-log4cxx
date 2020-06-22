from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class Log4cxxConan(ConanFile):
    name = "log4cxx"
    version = "0.10.0"
    license = "MIT"
    url = "https://github.com/zoomint/conan-log4cxx"
    author = "Vincent Thiery (vjmthiery@gmail.com), Jindrich Hrabal (jindrich.hrabal@eleveo.com)"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "patches/**"
    requires = "apr/1.7.0", "apr-util/1.6.1"
    generators = "make"

    _autotools = None

    def configure(self):
        self.options["apr"].shared = False
        self.options["apr-util"].shared = False

    @property
    def _source_subfolder(self):
        return "apache-log4cxx-%s" % self.version

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        self._autotools = AutoToolsBuildEnvironment(self)
        self._autotools.cxx_flags.append("-Wno-narrowing")
        conf_args = [
            "--with-apr=" + self.deps_env_info["apr"].APR_ROOT,
            "--with-apr-util=" + self.deps_env_info["apr-util"].APR_UTIL_ROOT
        ]
        self._autotools.configure(args=conf_args, configure_dir=self._source_subfolder)
        return self._autotools

    def _patch_sources(self):
        for patch in self.conan_data["patches"][self.version]:
            self.output.info("Applying patch: {}".format(patch))
            tools.patch(**patch)

    def source(self):
        # Get log4cxx
        zip_name = "apache-log4cxx-%s.tar.gz" % self.version
        tools.download("https://downloads.apache.org/logging/log4cxx/%s/%s" % (self.version, zip_name), zip_name, retry=2, retry_wait=5)
        tools.unzip(zip_name)

    def build(self):
        self._patch_sources()
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
