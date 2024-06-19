# iGEM Actions

## Overview

This repository contains the github actions and scripts required to processs and build iGEM distribution packages.

The aim of this package is to simplify the package creation process, streamline package development and ensure the robust creation and utilisation of the iGEM distribution.  

Calculates the complexity score for IDT orders.

## Structure 

The `./scripts` folder contains a python library of scripts that automatically collect, generate or validate materials that are contained within an iGEM distribution package. This includes any requirements, python files and test cases that are required to ensure the scripts function as intended. 

Within `./github`, there is a workflow file which executes unit tests on push. This ensures that only working code can be merged with the live action suite. 

The `action.yml` file contains the specific action information, as well as the workflow for executing the required scripts. 

## Notes

This is v0.1.0, a working beta for testing the initial use case. Updates will be occuring to improve the process.

