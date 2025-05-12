#====================================
# @file   : CMakeLists.txt
# @brief  : cmake configuration file for vsUTCS
#====================================
# Copyright (C) 2020-2025 Evert Vorster, Stephen G. Tuggy, Roy Falk,
# and other vsUTCS contributors.
#
# This file is part of Vega Strike: Upon the Coldest Sea ("vsUTCS").
#
# vsUTCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# vsUTCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vsUTCS.  If not, see <https://www.gnu.org/licenses/>.


CMAKE_MINIMUM_REQUIRED(VERSION 3.21 FATAL_ERROR)

SET(vsUTCS_VERSION_MAJOR "0")
SET(vsUTCS_VERSION_MINOR "9")
SET(vsUTCS_VERSION_PATCH "1")

# Auto-populate with the git hash of the build
IF (DEFINED ENV{SHORT_SHA} AND NOT "$ENV{SHORT_SHA}" STREQUAL "")
    SET (vsUTCS_VERSION_TWEAK "$ENV{SHORT_SHA}")
ELSE ()
    EXECUTE_PROCESS(
        COMMAND git rev-parse --short HEAD
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        OUTPUT_VARIABLE vsUTCS_VERSION_TWEAK
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
ENDIF ()

PROJECT(vsUTCS
    VERSION
        "${vsUTCS_VERSION_MAJOR}.${vsUTCS_VERSION_MINOR}.${vsUTCS_VERSION_PATCH}"   #.${vsUTCS_VERSION_TWEAK}   # CMake only allows numeric version components, unfortunately.
)

MESSAGE("== Vega Strike: Upon the Coldest Sea Version: ${vsUTCS_VERSION_LONG_STR}")

# Let cmake find our in-tree modules
SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${vsUTCS_SOURCE_DIR})

# Detect available Linux Distros that can be built for
FIND_PACKAGE(LinuxDistro REQUIRED)

INCLUDE(GNUInstallDirs)

SET(CPACK_IGNORE_FILES
    build/
    packages/
    \\\\.git/
    \\\\.vs/
    \\\\.vscode/
    ".*\\\\.pyc"
)
SET(CPACK_SOURCE_IGNORE_FILES
    build/
    packages/
    \\\\.git/
    \\\\.vs/
    \\\\.vscode/
    ".*\\\\.pyc"
)

INSTALL(DIRECTORY .vegastrike/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/.vegastrike)

INSTALL(DIRECTORY ai/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/ai
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY animations/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/animations
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY bases/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/bases)

INSTALL(DIRECTORY cgi-accountserver/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/cgi-accountserver)

INSTALL(DIRECTORY cockpits/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/cockpits
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY communications/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/communications)

INSTALL(DIRECTORY documentation/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/documentation)

INSTALL(DIRECTORY history/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/history)

INSTALL(DIRECTORY meshes/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/meshes
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY mission/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/mission)

INSTALL(DIRECTORY modules/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/modules)

INSTALL(DIRECTORY music/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/music)

INSTALL(DIRECTORY programs/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/programs)

INSTALL(DIRECTORY sectors/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/sectors)

INSTALL(DIRECTORY sounds/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/sounds
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY sprites/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/sprites
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY techniques/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/techniques)

INSTALL(DIRECTORY textures/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/textures
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY units/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/units
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY universe/ DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike/universe)

INSTALL(FILES New_Game DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES Version.txt DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES factions.xml DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

#INSTALL(FILES units.json DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
#INSTALL(FILES ships.json DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES master_part_list.csv DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
INSTALL(FILES master_part_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
INSTALL(FILES master_asteroid_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
INSTALL(FILES master_component_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
INSTALL(FILES master_ship_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES cities.txt DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES py27_modules.7z DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES py3_modules.7z DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES setup.config DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES vega-license.txt DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES weapon_list.xml DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
INSTALL(FILES weapons.json DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES cursor1.cur DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

INSTALL(FILES vegastrike.config DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)

IF (CMAKE_SYSTEM_NAME STREQUAL Linux)
    INSTALL(FILES vegastrike.desktop DESTINATION share/applications)
    INSTALL(FILES vegasettings.desktop DESTINATION share/applications)

    INSTALL(FILES vegastrike.png DESTINATION share/pixmaps)
    INSTALL(FILES vegastrike_settings.png DESTINATION share/pixmaps)

    INSTALL(FILES vegastrike.xpm DESTINATION share/pixmaps)
    INSTALL(FILES vslogo.xpm DESTINATION share/pixmaps)

    INSTALL(FILES vs DESTINATION bin PERMISSIONS
            OWNER_READ OWNER_WRITE OWNER_EXECUTE
            GROUP_READ GROUP_EXECUTE
            WORLD_READ WORLD_EXECUTE)

    INSTALL(FILES vsettings DESTINATION bin PERMISSIONS
            OWNER_READ OWNER_WRITE OWNER_EXECUTE
            GROUP_READ GROUP_EXECUTE
            WORLD_READ WORLD_EXECUTE)
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Windows)
    INSTALL(FILES favicon.ico DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
    INSTALL(FILES uninstall.ico DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
    INSTALL(FILES vega.ico DESTINATION ${CMAKE_INSTALL_DATADIR}/vegastrike)
ENDIF ()

# CPack stuff
SET(CPACK_PACKAGE_NAME "vsUTCS")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "3D space combat and trading game")
SET(CPACK_PACKAGE_VENDOR "Vega Strike")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/documentation/readme.txt")
SET(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/vega-license.txt")
SET(CPACK_PACKAGE_VERSION_MAJOR "${vsUTCS_VERSION_MAJOR}")
SET(CPACK_PACKAGE_VERSION_MINOR "${vsUTCS_VERSION_MINOR}")
SET(CPACK_PACKAGE_VERSION_PATCH "${vsUTCS_VERSION_PATCH}")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "vsUTCS-${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}")
SET(CPACK_CONTACT "maintainers@vega-strike.org")

# Source package filename
IF (DEFINED ENV{TAG_NAME})
    SET(vsUTCS_PACKAGE_VERSION_STR "$ENV{TAG_NAME}")
ELSE (DEFINED ENV{TAG_NAME})
    SET(vsUTCS_PACKAGE_VERSION_STR "${vsUTCS_VERSION_MAJOR}.${vsUTCS_VERSION_MINOR}.${vsUTCS_VERSION_PATCH}-0.${vsUTCS_VERSION_TWEAK}")
ENDIF (DEFINED ENV{TAG_NAME})
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}-Source")
SET(CPACK_SOURCE_GENERATOR "TXZ")

IF (CMAKE_SYSTEM_NAME STREQUAL Windows)
    MESSAGE(STATUS "Configuring Packaging for Windows")
    # NSIS - See https://cmake.org/cmake/help/v3.3/module/CPackNSIS.html
    # NSI bug requires at least 1 set of 4 forwards slashes??
    SET(CPACK_PACKAGE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\favicon.ico")
    SET(CPACK_NSIS_DISPLAY_NAME "Vega Strike Upon the Coldest Sea")
    SET(CPACK_NSIS_HELP_LINK "https:\\\\vega-strike.org")
    SET(CPACK_NSIS_URL_INFO_ABOUT "https:\\\\vega-strike.org/about")
    SET(CPACK_NSIS_CONTACT "maintainers@vega-strike.org")
    SET(CPACK_NSIS_MODIFY_PATH ON)

    SET(CPACK_GENERATOR "NSIS64")
    SET(CPACK_PACKAGE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/packages")
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}_Windows_${CMAKE_SYSTEM_VERSION}_${CMAKE_SYSTEM_PROCESSOR}")
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Darwin)
    MESSAGE(STATUS "Configuring Packaging for macOS")
    # There's a few options for MacOSX; not sure what we want to use
    # DragNDrop -> DMG
    #  See https://cmake.org/cmake/help/v3.3/module/CPackDMG.html
    # Bundle -> Compressed Disk Image
    # PackageMaker - see https://cmake.org/cmake/help/v3.3/module/CPackPackageMaker.html
    SET(CPACK_GENERATOR "DragNDrop")
    SET(CPACK_PACKAGE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/packages")
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}_macOS_${CMAKE_SYSTEM_VERSION}_${CMAKE_SYSTEM_PROCESSOR}")
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Linux)
    MESSAGE(STATUS "Configuring Packaging for Linux")
    SET(CPACK_GENERATOR "TXZ")

    # "DEB"
    IF (VS_CAN_BUILD_DEB)
        MESSAGE(STATUS "Configuring Debian Packaging")
        # See https://cmake.org/cmake/help/v3.3/module/CPackDeb.html
        SET(CPACK_DEBIAN_PACKAGE_NAME "vsUTCS")
        SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "maintainers@vega-strike.org")
        SET(CPACK_DEBIAN_COMPRESSION_TYPE "bzip2")
        SET(CPACK_DEBIAN_PACKAGE_DEPENDS "vega-strike")

        SET(CPACK_PACKAGE_FILE_NAME "${CPACK_DEBIAN_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}")

        SET(CPACK_DEBIAN_PACKAGE_SECTION "Amusements/Games")
        SET(CPACK_DEBIAN_PACKAGE_HOMEPAGE "https://www.vega-strike.org")
        SET(CPACK_GENERATOR "DEB")
    ENDIF ()

    #  "RPM"
    IF (VS_CAN_BUILD_RPM)
        MESSAGE(STATUS "Configuring RPM Packaging")
        # See https://cmake.org/cmake/help/v3.3/module/CPackRPM.html
        SET(CPACK_RPM_PACKAGE_LICENSE "GPLv3") # See ../LICENSE
        SET(CPACK_RPM_PACKAGE_URL "https://www.vega-strike.org")
        SET(CPACK_RPM_PACKAGE_NAME "vsUTCS")
        SET(CPACK_RPM_PACKAGE_REQUIRES "Vega-Strike")

        # Figure out the filename
        IF (LINUX_CODENAME)
            SET(vsUTCS_LINUX_VERSION_STR "${LINUX_CODENAME}")
        ELSE (LINUX_CODENAME)
            SET(vsUTCS_LINUX_VERSION_STR "${LINUX_VERSION_ID}")
        ENDIF (LINUX_CODENAME)

        SET(CPACK_PACKAGE_FILE_NAME "${CPACK_RPM_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}-${LINUX_ID}-${vsUTCS_LINUX_VERSION_STR}")
        SET(CPACK_GENERATOR "RPM")
    ENDIF ()
ELSE ()
    MESSAGE(STATUS "Configuring Packaging for Unknown Platform - \"${CMAKE_SYSTEM_NAME}\"")
    # Unknown Platform --> Just do compressed tarball
    SET(CPACK_GENERATOR "TXZ")
ENDIF ()

INCLUDE(CPack)
