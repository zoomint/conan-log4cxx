from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class Log4cxxConan(ConanFile):
    name = "log4cxx"
    version = "0.10.0"
    license = "MIT"
    url = "https://github.com/vthiery/conan-log4cxx"
    author = "Vincent Thiery (vjmthiery@gmail.com), Jindrich Hrabal (jindrich.hrabal@eleveo.com)"
    ZIP_FOLDER_NAME = "apache-log4cxx-%s" % version
    settings = "os", "compiler", "build_type", "arch"
    requires = "apr/1.7.0", "apr-util/1.6.1"
    generators = "make"

    autotools = None

    def source(self):
        # Get log4cxx
        zip_name = "apache-log4cxx-%s.tar.gz" % self.version
        tools.download("https://downloads.apache.org/logging/log4cxx/%s/%s" % (self.version, zip_name), zip_name, retry=2, retry_wait=5)
        tools.unzip(zip_name)
        # Apply patches
        with tools.chdir(self.ZIP_FOLDER_NAME):
            tools.download("https://issues.apache.org/jira/secure/attachment/12439513/cppFolder_stringInclude.patch", "cppFolder_stringInclude.patch", retry=2, retry_wait=5)
            tools.download("https://issues.apache.org/jira/secure/attachment/12439514/exampleFolder_stringInclude.patch", "exampleFolder_stringInclude.patch", retry=2, retry_wait=5)
            self.run("patch -p1 -i cppFolder_stringInclude.patch && patch -p1 -i exampleFolder_stringInclude.patch")

    def build(self):
        self.autotools = AutoToolsBuildEnvironment(self)
        self.autotools.cxx_flags.append("-Wno-narrowing")
        self.autotools.configure(configure_dir=self.ZIP_FOLDER_NAME,
            args=["--with-apr=" + self.deps_env_info["apr"].APR_ROOT,
                "--with-apr-util=" + self.deps_env_info["apr-util"].APR_UTIL_ROOT])
        self.autotools.make()

    def package(self):
        self.autotools.make(target="install")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
