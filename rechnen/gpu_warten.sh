#!/bin/bash
# KI-generiert (Claude Opus, 2026-11-23). Vorgabe Autor 23.11.: „bevor etwas auf die grafikkarte wandert prüfe ob sie frei ist, wenn nicht gehe auf pause und warte bis sie frei ist.“
# Frei = keine Rechenprozesse auf der GPU, Auslastung < 30 %, Speicher < 2000 MiB, kein geladenes ollama-Modell.
# Solange belegt: Datei rechnen/GPU_WARTEN (Meldung an Opus/Autor), Zeile im verlauf.log, alle 60 s neu prüfen. Bricht bei rechnen/STOP ab (rc 1).
cd /home/cae/hermes/batterie; L=rechnen/verlauf.log; W=rechnen/GPU_WARTEN; G=0
belegt() {
  local apps u m o
  apps=$(nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader 2>/dev/null | tr '\n' ' ')
  read -r u m < <(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits 2>/dev/null | tr -d ',')
  o=$(curl -s --max-time 5 localhost:11434/api/ps 2>/dev/null | grep -o '"name":"[^"]*"' | head -1)
  B=""; [ -n "$apps" ] && B="Prozesse: $apps"; [ "${u:-0}" -ge 30 ] && B="$B Auslastung ${u} %"; [ "${m:-0}" -ge 2000 ] && B="$B Speicher ${m} MiB"; [ -n "$o" ] && B="$B ollama $o"
  [ -n "$B" ]
}
while belegt; do
  [ -f rechnen/STOP ] && { rm -f $W; exit 1; }
  if [ $G -eq 0 ]; then echo "$(date '+%F %T') GPU belegt ($B) – Warteschlange pausiert vor GPU-Schritt" | tee $W >>$L; G=1; fi
  sleep 60
done
[ $G -eq 1 ] && { echo "$(date '+%F %T') GPU wieder frei – Warteschlange läuft weiter" >>$L; rm -f $W; touch rechnen/GPU_FREI; }
exit 0
