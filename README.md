# Plotters

Plotters for the T2K TPC testbeams. The Analysis package is stored [here](https://gitlab.com/t2k-beamtest/desy_testbeam).

# Event display
Event display is now availible as a separate package [here](https://gitlab.com/t2k-beamtest/daq-reader).

# Figures plotting with Jupyter

ROOT should be installed with the proper python version. Commands `python3` and `import ROOT` should work from terminal. That should work by default at LXPLUS

T2K style is optional and depends on the [package](https://gitlab.com/suvorov21/t2kstyle_py). If styling is not required -- simply comment the line.

Jupyter can be run either on LXPLUS or at your local machine with mounted path towards the analysis results. Change the `path` variable at the beginning of each notebook to set a path properly.

## Other tips

If Java script is not working, specify `%jsroot off` in the cell.

To make it working specify proper address in the ~/.jupyter/jupyter_notebook_config.py, e.g.
`c.NotebookApp.extra_static_paths=['/Users/suvorov/SOFT/CERN/ROOT/root-6.18.04-buildi_py3/js/']`
