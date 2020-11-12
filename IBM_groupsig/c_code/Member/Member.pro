TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt
LIBS += -lgroupsig -lmcl -Wl,-rpath=/usr/local/lib

SOURCES += \
        main.c

DISTFILES += \
    gpk
