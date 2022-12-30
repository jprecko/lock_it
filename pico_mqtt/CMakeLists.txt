
cmake_minimum_required(VERSION 3.13)
# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()

# find_package(eclipse-paho-mqtt-c REQUIRED)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

include(pico_sdk_import.cmake)
# include(lib/paho.mqtt.c/pico_sdk_import.cmake)


project(my_project CXX C ASM)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

add_subdirectory(external/paho.mqtt.c.git)

file(GLOB_RECURSE SRC_FILES src/*.cpp)
# add_executable(picow_blink ${SRC_FILES})

# rest of your project
add_executable(picow_blink
        picow_blink.c
        ${SRC_FILES}
)

# add_subdirectory(lib/paho.mqtt.c)

target_link_libraries(picow_blink
        pico_stdlib              # for core functionality
        pico_cyw43_arch_none     # we need Wifi to access the GPIO, but we don't need anything else
        # eclipse-paho-mqtt-c::paho-mqtt3as
) 
# create map/bin/hex file etc.
pico_add_extra_outputs(picow_blink)
pico_enable_stdio_usb(picow_blink 1)
pico_enable_stdio_uart(picow_blink 0)

# add url via pico_set_program_url
# example_auto_set_url(picow_blink)