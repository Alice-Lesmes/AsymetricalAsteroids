pluginManagement {
    repositories {

        google {
            content {
                includeGroupByRegex("com\\.android.*")
                includeGroupByRegex("com\\.google.*")
                includeGroupByRegex("androidx.*")
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven("https://github.com/irmen/pickle")
        maven("https://github.com/chaquo/chaquopy")
/*
        maven { url'https://github.com/irmen/pickle' }
*/
    }
}

rootProject.name = "AsymetricAsteroids"
include(":app")
 