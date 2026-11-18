# KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Wandelt Test#5-xlsx (Rohdaten, nur lesen) in schlanke CSV nach /home/cae/cae_projekte/batterie/c2/.
import openpyxl, csv, sys, os
D="/home/cae/cae_projekte/batterie/c2/t5/Test#5/"; O="/home/cae/cae_projekte/batterie/c2/csv/"; os.makedirs(O,exist_ok=True)
F={"m10":"JC_BYD_SOP_March22_-10degC_channel_1_Channel_1_Wb_1.xlsx","p00":"JC_BYD_SOP_March18_0degC_Channel_1_Channel_1_Wb_1.xlsx","p40":"JC_BYD_SOP_Aug14_40degC_Channel_1_Wb_1.xlsx"}
COL=["Test_Time(s)","Current(A)","Voltage(V)","SOC","Aux_Temperature_1(thermocouple1(C))"]
for k in (sys.argv[1:] or F):
    wb=openpyxl.load_workbook(D+F[k],read_only=True,data_only=True); ws=wb.worksheets[-1]
    it=ws.iter_rows(values_only=True); h=list(next(it)); ix=[h.index(c) if c in h else [j for j,x in enumerate(h) if x and str(x).startswith("Aux_Temperature") and "dT" not in str(x)][0] for c in COL]
    with open(O+k+".csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["t","I","V","SOC","T"]); n=0
        for r in it:
            w.writerow([r[i] for i in ix]); n+=1
    print(k,n,flush=True)
