#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generic shared functions."""

import configparser
import logging
import logging.config
import os
import sys
import toml


def load_logging() -> None:
    """Load logging configuration."""
    try:
        logging.config.fileConfig("config/logging.ini")
    except KeyError as inst:
        logging_config_recovery(inst)
    except FileNotFoundError as inst:
        logging_log_recovery(inst)
    except PermissionError as inst:
        print(f"Restricted access to one or more logging files - {inst}", file=sys.stderr)
    except Exception as inst:
        print(f"Unexpected exception, contact maintainer - {inst}", file=sys.stderr)


def logging_config_recovery(issue: FileNotFoundError) -> None:
    """Recover logging configuration file.

    Args:
        issue: exception containing data on why load failed

    """
    print(f"There was an exception when loading logging configuration: {issue}", file=sys.stderr)
    try:
        os.replace("config/logging.ini", "config/logging.ini.old")
    except FileNotFoundError:
        try:
            os.mkdir("config")
        except FileExistsError:
            pass
        else:
            print("Config directory was absent, created and continuing.", file=sys.stderr)
    else:
        print("Renamed old configuration file to logging.ini.old", file=sys.stderr)
    finally:
        print("Created new logging configuration", file=sys.stderr)
        create_logging_config()


def logging_log_recovery(issue: Exception) -> None:
    """Recover logging log file.

    Args:
        issue: exception containing data on why load failed

    """
    print(f"There was an exception when loading logging configuration: {issue}", file=sys.stderr)
    try:
        os.mkdir("logs")
    except Exception as inst:
        print(f"Unexpected exception - {inst}")
    else:
        print("Log directory was absent, created and continuing.", file=sys.stderr)


def create_logging_config() -> None:
    """Generate a standard logging configuration."""
    config = configparser.ConfigParser()
    config["loggers"] = {"keys": "root"}
    config["handlers"] = {"keys": "systemFileHandler, systemStreamHandler, errorFileHandler"}
    config["formatters"] = {"keys": "systemFormatter, errorFormatter"}
    config["logger_root"] = {
        "level": "INFO",
        "handlers": "systemFileHandler, systemStreamHandler, errorFileHandler"
    }
    config["handler_systemFileHandler"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "INFO",
        "formatter": "systemFormatter",
        "args": "('logs/utilities.log', 'a+', 10 * 1024 * 1024, 10,)"
    }
    config["handler_systemStreamHandler"] = {
        "class": "StreamHandler",
        "level": "WARNING",
        "formatter": "systemFormatter",
        "args": "(sys.stderr,)"
    }
    config["handler_errorFileHandler"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "WARNING",
        "formatter": "errorFormatter",
        "args": "('logs/utilities.errors.log', 'a+', 10 * 1024 * 1024, 10,)"
    }
    config["formatter_systemFormatter"] = {
        "format": "%(asctime)s - %(name)s::%(module)s - %(levelname)s - %(message)s"
    }
    config["formatter_errorFormatter"] = {
        "format": "%(asctime)s -- %(name)s::%(module)s::%(funcname)s::%(lineno)s -- %(levelname)s -- %(message)s"
    }
    with open("config/logging.ini", "w+") as out:
        config.write(out)


def validate_config(issue: Exception) -> None:
    """Validate utils configuration file.

    Notes:
        Called after a configuration load fails, should complete with
        an empty configuration file generated barring major issues.

        Attempts to load the configuration again and initiates recovery
        based on exceptions that occur

    """
    logger = logging.getLogger(__name__)
    logger.warning(f"Configuration validation initiated due to exception - {issue}")
    with open("config/utils.toml", "r") as conffile:
        try:
            config = toml.load(conffile)
        except FileNotFoundError:
            try:
                os.mkdir("config")
            except FileExistsError:
                pass
            else:
                logger.debug("Directory 'config' already exists")
            finally:
                create_empty_config()
        except KeyError:
            logger.warning("Appending '.old' to old config and generating clean file")
            os.replace("config/utils.toml", "config/utils.toml.old")
            create_empty_config()


def create_empty_config() -> None:
    """Generate an empty configuration for utilities."""

    logger = logging.getLogger(__name__)

    config = {}

    config["system"] = {}

    config["system"]["screen"] = {}
    screen = config["system"]["screen"]
    screen["color"] = "yellow"
    screen["type"] = "phat"
    screen["orientation"] = "landscape"
    screen["vert_flip"] = True

    config["system"]["misc"] = {}
    config["system"]["misc"]["datefmt"] = "YYYY-MM-DD"

    config["utils"] = {}

    config["utils"]["analog"] = {}
    config["utils"]["analog"]["second_hand"] = True

    config["utils"]["calendar"] = {}
    config["utils"]["calendar"]["week_start"] = "Monday"

    config["apis"] = {}

    config["apis"]["darksky"] = {}
    darksky = config["apis"]["darksky"]
    darksky["secret"] = "Replace me"
    darksky["message_limit"] = 1000
    darksky["latitude"] = 0.000
    darksky["longitude"] = 0.000

    with open("config/utils.toml", "w+") as out:
        toml.dump(config, out)
