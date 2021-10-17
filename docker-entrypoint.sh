#!/usr/bin/env sh

case "${1}" in
    "api")
        shift
        echo "Starting API ..." && \
        exec python -m src
        ;;

    "pytest")
        shift
        echo "Tests"
        exec pytest
        ;;

    "help")
        shift
        exec echo "Set command: api pytest"
        ;;

    *)
        exec ${@}
        ;;
esac
