# iGEM Actions

## Overview

This repository contains the github actions and scripts required to processs and build iGEM distribution packages.

The aim of this package is to simplify the package creation process, streamline package development and ensure the robust creation and utilisation of the iGEM distribution.  

## Structure 

The `./scripts` folder contains a python library of scripts that automatically collect, generate or validate materials that are contained within an iGEM distribution package. This includes any requirements, python files and test cases that are required to ensure the scripts function as intended. 

Within `./github`, there is a workflow file which executes unit tests on push. This ensures that only working code can be merged with the live action suite. 

The `action.yml` file contains the specific action information, as well as the workflow for executing the required scripts. 

## User Documentation

The iGEM Actions repository is intended to work together with the [iGEM Package Template](https://github.com/iGEM-Engineering/iGEM-package-template) repository. 

The [iGEM Package Template](https://github.com/iGEM-Engineering/iGEM-package-template) repository can be used to build new distribution packages. This repository calls the iGEM Actions and activates the corresponding GitHub Actions on the repository. Two succesful examples of this template can be found in the [Anderson Promoters Collection](https://github.com/iGEM-Engineering/iGEM-Anderson-Promoters) and the [iGEM RBS Collection](https://github.com/iGEM-Engineering/iGEM-RBS-collection) package.

Please follow these next steps to succesfully use the tool:
1. Fork the [iGEM Package Template](https://github.com/iGEM-Engineering/iGEM-package-template) repository or one of its implementations.

2. Set up the repository. 
Make sure to enable GitHub Actions. Go to the Actions tab in your forked repository and click on **I understand my workflows, go ahead and enable them**
Now, please go to the **Settings** tab. Then, on the left-hand side panel, go to **Actions->General**, and make sure the workflow has reading and and writing permissions. Also, check the box that says **Allow GitHub Actions to create and approve pull requests**, this will be needed to update the files in the repository.

3. Set up IDT Credentials GitHub Secret.
Finally, to check the synthesizability of your sequences by computing the complexity scores, you will need to set up a GitHub secret with your Integrated DNA Technologies(IDT) account credentials. As the software tool uses the IDT API, If you don’t have an account, you will need to [create one](https://www.idtdna.com/site/Account/AccountSetup).
Please go to the **Settings** tab on your repository. Then, on the left-hand side panel, go to **Secrets and variables->Actions**, and select **New repository secret**.
Make sure to name your secret **IDT_CREDENTIALS**, and provide your IDT account details in the dictionary format: **{"username":"X","password":"X","ClientID":"X","ClientSecret":"X"}**

Now, all is set up and the tool is ready to use.

## Notes

This is v0.1.0, a working beta for testing the initial use case. Updates will be occuring to improve the process.

