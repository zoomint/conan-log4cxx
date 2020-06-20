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
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            configure_command = "CXXFLAGS=-Wno-narrowing ./configure"
            configure_command += " --with-apr=" + self.deps_env_info["apr"].APR_ROOT
            configure_command += " --with-apr-util=" + self.deps_env_info["apr-util"].APR_UTIL_ROOT
            configure_command += " --prefix=" + os.getcwd()

            with tools.chdir(self.ZIP_FOLDER_NAME):
                # Install log4cxx itself
                self.run(configure_command)
                env_build.make()
                self.run("sudo make install")

    def package(self):
        self.copy("*", dst="include", src="include", keep_path=True)
        self.copy("liblog4cxx*", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["log4cxx"]
