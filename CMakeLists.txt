#====================================
# @file   : CMakeLists.txt
# @brief  : cmake configuration file for vsUTCS
#====================================
# Copyright (C) 2020 Evert Vorster, Stephen G. Tuggy,
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


CMAKE_MINIMUM_REQUIRED(VERSION 3.5)
PROJECT(vsUTCS)

INSTALL(DIRECTORY .vegastrike/ DESTINATION share/vegastrike/.vegastrike
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY ai/ DESTINATION share/vegastrike/ai
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY animations/ DESTINATION share/vegastrike/animations
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY bases/ DESTINATION share/vegastrike/bases
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY cgi-accountserver/ DESTINATION share/vegastrike/cgi-accountserver
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY cockpits/ DESTINATION share/vegastrike/cockpits
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY communications/ DESTINATION share/vegastrike/communications
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY documentation/ DESTINATION share/vegastrike/documentation
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY history/ DESTINATION share/vegastrike/history
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY meshes/ DESTINATION share/vegastrike/meshes
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY mission/ DESTINATION share/vegastrike/mission
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY modules/ DESTINATION share/vegastrike/modules
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY music/ DESTINATION share/vegastrike/music
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY programs/ DESTINATION share/vegastrike/programs
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY sectors/ DESTINATION share/vegastrike/sectors
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY sounds/ DESTINATION share/vegastrike/sounds
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY sprites/ DESTINATION share/vegastrike/sprites
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY techniques/ DESTINATION share/vegastrike/techniques
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY textures/ DESTINATION share/vegastrike/textures
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY units/ DESTINATION share/vegastrike/units
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY universe/ DESTINATION share/vegastrike/universe
        PATTERN "*.am" EXCLUDE)

INSTALL(FILES New_Game DESTINATION share/vegastrike)

INSTALL(FILES Version.txt DESTINATION share/vegastrike)

INSTALL(FILES factions.xml DESTINATION share/vegastrike)

INSTALL(FILES master_part_list.csv DESTINATION share/vegastrike)

INSTALL(FILES py27_modules.7z DESTINATION share/vegastrike)

INSTALL(FILES py3_modules.7z DESTINATION share/vegastrike)

INSTALL(FILES setup.config DESTINATION share/vegastrike)

INSTALL(FILES vega-license.txt DESTINATION share/vegastrike)

INSTALL(FILES weapon_list.xml DESTINATION share/vegastrike)


# Linux specific locations from here on out.

INSTALL(FILES vegastrike.config DESTINATION share/vegastrike)

INSTALL(FILES vegastrike.desktop DESTINATION share/applications)
INSTALL(FILES vegasettings.desktop DESTINATION share/applications)

INSTALL(FILES vegastrike.png DESTINATION share/pixmaps)
INSTALL(FILES vegastrike_settings.png DESTINATION share/pixmaps)

INSTALL(FILES vegastrike.xpm DESTINATION share/pixmaps)

INSTALL(FILES vs DESTINATION bin PERMISSIONS
	OWNER_READ OWNER_WRITE OWNER_EXECUTE
	GROUP_READ GROUP_WRITE GROUP_EXECUTE
	WORLD_READ WORLD_WRITE WORLD_EXECUTE)

INSTALL(FILES vsettings DESTINATION bin PERMISSIONS
        OWNER_READ OWNER_WRITE OWNER_EXECUTE
        GROUP_READ GROUP_WRITE GROUP_EXECUTE
        WORLD_READ WORLD_WRITE WORLD_EXECUTE)

# CPack stuff
SET(CPACK_PACKAGE_NAME "vsUTCS")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "3D space combat and trading game")
SET(CPACK_PACKAGE_VENDOR "Vega Strike")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/documentation/readme.txt")
SET(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/vega-license.txt")
SET(CPACK_PACKAGE_VERSION_MAJOR "0")
SET(CPACK_PACKAGE_VERSION_MINOR "7")
SET(CPACK_PACKAGE_VERSION_PATCH "0")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "vsUTCS-${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}")
SET(CPACK_CONTACT "maintainers@vega-strike.org")
SET(CPACK_SOURCE_IGNORE_FILES "/build/;/packages/;/.git/;.*\.pyc;.*\.am")

# Source package filename
IF (DEFINED ENV{TRAVIS_TAG})
    SET(vsUTCS_PACKAGE_VERSION_STR "$ENV{TRAVIS_TAG}")
ELSE (DEFINED ENV{TRAVIS_TAG})
    SET(vsUTCS_PACKAGE_VERSION_STR "${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}")
ENDIF (DEFINED ENV{TRAVIS_TAG})
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}-Source")
SET(CPACK_SOURCE_GENERATOR "TXZ")

IF (WIN32 AND NOT UNIX)
    MESSAGE("-- Configuring Packaging for Windows")
    # NSIS - See https://cmake.org/cmake/help/v3.3/module/CPackNSIS.html
    # NSI bug requires at least 1 set of 4 forwards slashes??
    SET(CPACK_PACKAGE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\favicon.ico")
    SET(CPACK_NSIS_DISPLAY_NAME "Vega Strike Upon the Coldest Sea")
    SET(CPACK_NSIS_HELP_LINK "https:\\\\vega-strike.org")
    SET(CPACK_NSIS_URL_INFO_ABOUT "https:\\\\vega-strike.org/about")
    SET(CPACK_NSIS_CONTACT "maintainers@vega-strike.org")
    SET(CPACK_NSIS_MODIFY_PATH ON)

    # NSIS, Wix, and compressed archives (7z, Zip)
    SET(CPACK_GENERATOR "NSIS" "NSIS64" "WIX" "7Z" "ZIP")
    # SET(CPACK_PACKAGE_EXECUTABLES "vegastrike.exe" "mesh_tool.exe" "vegasettings.exe")
ELSEIF (XCODE)
    MESSAGE("-- Configuring Packaging for Mac OS X")
    # Mac OS X
    # There's a few options for MacOSX; not sure what we want to use
    # DragNDrop -> DMG
    #  See https://cmake.org/cmake/help/v3.3/module/CPackDMG.html
    # Bundle -> Compressed Disk Image
    # PackageMaker - see https://cmake.org/cmake/help/v3.3/module/CPackPackageMaker.html
    SET(CPACK_GENERATOR "DragNDrop" "BUNDLE" "TXZ")
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Linux)
    MESSAGE("-- Configuring Packaging for Linux")
    SET(CPACK_GENERATOR "TXZ")

    # Gather info about Linux distro and release (if applicable).
    IF (CMAKE_SYSTEM_NAME STREQUAL Linux)
        EXECUTE_PROCESS(
            COMMAND sh -c "cat /etc/os-release | grep ^ID= | sed 's/^ID=//' | tr -d '\"\n'"
            OUTPUT_VARIABLE LINUX_ID)
        EXECUTE_PROCESS(
            COMMAND sh -c "cat /etc/os-release | grep ^VERSION_CODENAME= | sed 's/^VERSION_CODENAME=//' | tr -d '\"\n'"
             OUTPUT_VARIABLE LINUX_CODENAME)
        EXECUTE_PROCESS(
            COMMAND sh -c "cat /etc/os-release | grep ^VERSION_ID= | sed 's/^VERSION_ID=//' | tr -d '\"\n'"
            OUTPUT_VARIABLE LINUX_VERSION_ID)
    ENDIF (CMAKE_SYSTEM_NAME STREQUAL Linux)

    # SET(LSB_EXISTS FALSE)
    # SET(LSB_LINUX_DISTRIBUTION "Unknown")
    # SET(LSB_LINUX_DISTRIBUTION_CODENAME "Unknown")

    # # Lookup the LSB Data - this is known for Ubuntu, but also used by other distros too.
    # # and may help with distro-sub-selection
    # FIND_PROGRAM(LSB_RELEASE_EXEC lsb_release)
    # IF (LSB_RELEASE_EXEC)
    #     EXECUTE_PROCESS(COMMAND ${LSB_RELEASE_EXEC} --codename --short
    #         OUTPUT_VARIABLE LSB_LINUX_DISTRIBUTION_CODENAME
    #         OUTPUT_STRIP_TRAILING_WHITESPACE)
    #     EXECUTE_PROCESS(COMMAND ${LSB_RELEASE_EXEC} --id --short
    #         OUTPUT_VARIABLE LSB_LINUX_DISTRIBUTION
    #         OUTPUT_STRIP_TRAILING_WHITESPACE)
    #     SET(LSB_EXISTS TRUE)
    #     MESSAGE("Found Linux Distribution Release Name: ${LSB_LINUX_DISTRIBUTION_CODENAME}")
    # ENDIF (LSB_RELEASE_EXEC)

    # "DEB"
    FIND_PROGRAM(HAS_APT NAMES apt-get apt)
    IF (HAS_APT)
        MESSAGE("-- Configuring Debian Packaging")
        # See https://cmake.org/cmake/help/v3.3/module/CPackDeb.html
        SET(CPACK_DEBIAN_PACKAGE_NAME "vsUTCS")
        SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "maintainers@vega-strike.org")
        SET(CPACK_DEBIAN_COMPRESSION_TYPE "bzip2")
        SET(CPACK_DEBIAN_PACKAGE_DEPENDS "vega-strike")

        # Debian Version: /etc/debian_version - <name>/<junk>
        # IF (NOT LSB_EXISTS)
        #     SET(USE_DEBIAN_VERSION TRUE)
        #     FILE(READ "/etc/debian_version" DEBIAN_VERSION_DATA)
        #     STRING(REGEX MATCH "^(.+)\/.*$" DEBIAN_VERSION_DATA DEBIAN_RELEASE_VERSION)
        # ELSE (NOT LSB_EXISTS)
        #     SET(USE_DEBIAN_VERSION FALSE)
        #     SET(DEBIAN_RELEASE_VERSION "Debian Derivative Release Version ${LSB_LINUX_DISTRIBUTION_CODENAME}")
        # ENDIF (NOT LSB_EXISTS)

        # IF (USE_DEBIAN_VERSION)
        #     SET(CPACK_PACKAGE_FILE_NAME "${CPACK_DEBIAN_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}-debian-${DEBIAN_RELEASE_VERSION}_x86_64")
        # ELSE (USE_DEBIAN_VERSION)
        #     SET(CPACK_PACKAGE_FILE_NAME "${CPACK_DEBIAN_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}-${LSB_LINUX_DISTRIBUTION}-${LSB_LINUX_DISTRIBUTION_CODENAME}_x86_64")
        # ENDIF (USE_DEBIAN_VERSION)

        SET(CPACK_PACKAGE_FILE_NAME "${CPACK_DEBIAN_PACKAGE_NAME}_${vsUTCS_PACKAGE_VERSION_STR}")

        SET(CPACK_DEBIAN_PACKAGE_SECTION "Amusements/Games")
        SET(CPACK_DEBIAN_PACKAGE_HOMEPAGE "https://www.vega-strike.org")
        SET(CPACK_GENERATOR "DEB")
    ENDIF (HAS_APT)

    #  "RPM"
    FIND_PROGRAM(HAS_RPMBUILD rpmbuild)
    IF (HAS_RPMBUILD)
        MESSAGE("-- Configuring RPM Packaging")
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
    ENDIF (HAS_RPMBUILD)
ELSE (WIN32 AND NOT UNIX)
    MESSAGE("-- Configuring Packaging for Unknown Platforms - \"${CMAKE_SYSTEM_NAME}\"")
    # Unknown Platform --> Just do compressed tarball
    SET(CPACK_GENERATOR "TXZ")
ENDIF (WIN32 AND NOT UNIX)

INCLUDE(CPack)
