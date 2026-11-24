# source /home/cae/hermes/batterie/umgebung.sh  -- KI-generiert (Claude Opus, 2026-11-11)
export BATTERIE=/home/cae/hermes/batterie
export PATH="$BATTERIE/.venv/bin:$PATH"
export FREECAD_APPIMAGE=/home/cae/Applications/FreeCAD_1.1.4.AppImage
export BLENDER=/usr/bin/blender
# E3 (Sonnet, 2026-11-24): ngspice ohne sudo, KiCad per Flatpak
export NGSPICE_ROOT=$HOME/.local/opt/ngspice
export PATH="$NGSPICE_ROOT/usr/bin:$BATTERIE/werkzeuge:$PATH"
export LD_LIBRARY_PATH="$NGSPICE_ROOT/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export SPICE_LIB_DIR=$NGSPICE_ROOT/usr/lib/x86_64-linux-gnu/ngspice
export KICAD_CLI=$BATTERIE/werkzeuge/kicad-cli.sh
export FREEROUTING="$HOME/.local/opt/freerouting/freerouting.sh"   # Freerouting 2.5.0 Jar + JRE 25 (GPL-3), Autor 2026-11-24; native CLI stürzt ab
