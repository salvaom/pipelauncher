## Introduction

Code for http://dev.salvaom.com/eco

## Installation


Windows
```
git clone https://github.com/salvaom/pipelauncher
git clone https://github.com/PeregrineLabs/Ecosystem pipelauncher/Ecosystem
git clone https://github.com/ColinDuquesnoy/QDarkStyleSheet pipelauncher/source/QDarkStyleSheet
cd pipelauncher
set ECO_ENV=%cd%/resources/envs
set PYTHONPATH=%cd%/Ecosystem/bin;%cd%/source;%cd%/source/QDarkStyleSheet
set SOFTWARE_BASE=%cd%/software
set PIPE_PROJECT_PATH=%cd%/resources/projects
set PIPE_APP_PATH=%cd%/resources/apps
```


## Execution

```
python -m pipelauncher
```
