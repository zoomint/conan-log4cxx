from conans import ConanFile, AutoToolsBuildEnvironment, tools

class Log4cxxConan(ConanFile):
    name = "log4cxx"
    version = "0.10.0"
    license = "MIT"
    url = "https://github.com/vthiery/conan-log4cxx"
    author = "Vincent Thiery (vjmthiery@gmail.com)"
    ZIP_FOLDER_NAME = "apache-log4cxx-%s" % version
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        # Install the Apache Portable Runtime Libraries
        self.run("sudo apt-get install --yes libapr1-dev libapr1 libaprutil1-dev libaprutil1")
        # Install log4cxx itself
        zip_name = "apache-log4cxx-%s.tar.gz" % self.version
        tools.download("http://www.pirbot.com/mirrors/apache/logging/log4cxx/%s/%s" % (self.version, zip_name), zip_name, retry=2, retry_wait=5)
        tools.unzip(zip_name)
        # Apply patches
        with tools.chdir(self.ZIP_FOLDER_NAME):
            tools.download("https://issues.apache.org/jira/secure/attachment/12439513/cppFolder_stringInclude.patch", "cppFolder_stringInclude.patch", retry=2, retry_wait=5)
            tools.download("https://issues.apache.org/jira/secure/attachment/12439514/exampleFolder_stringInclude.patch", "exampleFolder_stringInclude.patch", retry=2, retry_wait=5)
            self.run("patch -p1 -i cppFolder_stringInclude.patch && patch -p1 -i exampleFolder_stringInclude.patch")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            with tools.chdir(self.ZIP_FOLDER_NAME):
                self.run("CXXFLAGS=-Wno-narrowing ./configure")
                env_build.make()
                self.run("sudo make install")

    def package(self):
        self.copy("*", dst="include", src="/usr/local/include/log4cxx", keep_path=True)
        self.copy("liblog4cxx.*", dst="lib", src="/usr/local/lib", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["log4cxx"]
