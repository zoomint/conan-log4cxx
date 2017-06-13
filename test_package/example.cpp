#include <log4cxx/basicconfigurator.h>
#include <log4cxx/logger.h>
#include <log4cxx/helpers/messagebuffer.h>

using namespace log4cxx;

LoggerPtr logger(Logger::getLogger("com.foo"));

int main()
{
    int result = EXIT_SUCCESS;

    try
    {
        BasicConfigurator::configure();

        LOG4CXX_INFO(logger, "Simple message text:");
        LOG4CXX_DEBUG(logger, "Hello World!");
    }
    catch (const std::exception& e)
    {
        result = EXIT_FAILURE;
    }

    return result;
}