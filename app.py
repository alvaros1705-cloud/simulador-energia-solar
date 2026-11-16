import io
import math
import zipfile
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

st.set_page_config(page_title="Solar Lab – Integral Insights", page_icon="☀️", layout="wide")
ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
TEAM = ["Sara Gáfaro Salamanca", "Leidy Stephania Delgado Galvis", "Angel David Carrascal Claro", "Samuel David Jaimes Estrada"]
ES = {
"subtitle":"Análisis de energía solar mediante cálculo integral","nav":"NAVEGACIÓN","dashboard":"Panel principal","measure":"Mediciones","integral":"Análisis integral","hyp":"Laboratorio de hipótesis","history":"Historial","report":"Informes","panels":"Número de paneles","peak":"Potencia máxima por panel (W)","start":"Hora inicial","end":"Hora final","intro":"Explora un modelo matemático de potencia solar, contrasta la integración analítica y numérica y analiza mediciones experimentales.","energy":"Energía estimada","avg":"Potencia promedio","max":"Potencia total máxima","model":"Modelo hipotético","upload":"Cargar mediciones CSV","help":"El archivo debe contener las columnas hora y potencia_w. La hora puede expresarse como 08:30 o como 8.5.","template":"Descargar plantilla CSV","quality":"Calidad de datos (orientativa)","valid":"Registros válidos","missing":"Filas incompletas","duplicates":"Duplicados","negative":"Potencias negativas","outliers":"Posibles atípicos","measured_energy":"Energía integrada","curve":"Ajuste cuadrático","r2":"Coeficiente R²","factor":"Variación de potencia máxima (%)","save":"Guardar escenario en historial","empty":"Aún no hay escenarios guardados en esta sesión.","download_pdf":"Descargar informe PDF","download_csv":"Descargar datos CSV","download_zip":"Descargar paquete ZIP","team":"Equipo de trabajo","institution":"Universidad Simón Bolívar · Ingeniería Multimedia · Cálculo Integral","limitations":"Los parámetros iniciales son hipotéticos. La calidad es orientativa y no certifica instrumentos. No extrapoles el ajuste fuera del intervalo observado.","scenario":"Escenarios de potencia: −20 %, base y +20 %","geometry":"Aplicación geométrica","area":"Área rectangular total de paneles (m²)","radius":"Radio inicial (m)","slope":"Pendiente del radio (m/m)","length":"Longitud (m)","clear":"Limpiar historial","no_data":"Carga un CSV para analizar mediciones reales.","conclusion":"La integral definida representa la energía acumulada a partir de la potencia en el intervalo seleccionado."
}
EN = {
"subtitle":"Solar energy analysis through integral calculus","nav":"NAVIGATION","dashboard":"Dashboard","measure":"Measurements","integral":"Integral analysis","hyp":"Hypothesis lab","history":"History","report":"Reports","panels":"Number of panels","peak":"Maximum power per panel (W)","start":"Start time","end":"End time","intro":"Explore a mathematical solar power model, compare analytical and numerical integration, and analyze experimental measurements.","energy":"Estimated energy","avg":"Average power","max":"Total maximum power","model":"Hypothetical model","upload":"Upload CSV measurements","help":"The file must contain hora and potencia_w columns. Time can be written as 08:30 or 8.5.","template":"Download CSV template","quality":"Data quality (indicative)","valid":"Valid records","missing":"Incomplete rows","duplicates":"Duplicates","negative":"Negative power values","outliers":"Potential outliers","measured_energy":"Integrated energy","curve":"Quadratic fit","r2":"R-squared","factor":"Maximum power variation (%)","save":"Save scenario to history","empty":"No scenarios saved in this session yet.","download_pdf":"Download PDF report","download_csv":"Download CSV data","download_zip":"Download ZIP package","team":"Project team","institution":"Universidad Simón Bolívar · Multimedia Engineering · Integral Calculus","limitations":"Initial parameters are hypothetical. The quality score is indicative and does not certify instruments. Do not extrapolate the fit beyond the observed interval.","scenario":"Power scenarios: −20%, base, and +20%","geometry":"Geometric application","area":"Total rectangular panel area (m²)","radius":"Initial radius (m)","slope":"Radius slope (m/m)","length":"Length (m)","clear":"Clear history","no_data":"Upload a CSV to analyze real measurements.","conclusion":"The definite integral represents accumulated energy from power over the selected interval."
}
if "lang" not in st.session_state: st.session_state.lang = "Español (Colombia)"
if "dark" not in st.session_state: st.session_state.dark = False
if "history" not in st.session_state: st.session_state.history = []
lang_label = st.selectbox("Idioma / Language", ["Español (Colombia)", "English (USA)"], horizontal=True)
st.session_state.lang = lang_label
L = EN if lang_label == "English (USA)" else ES
st.session_state.dark = st.toggle("🌙 Modo oscuro / Dark mode", value=st.session_state.dark)
dark = st.session_state.dark
bg, fg, panel = ("#0B1B30","#F3F7FC","#142B45") if dark else ("#F4F7FC","#172B49","#FFFFFF")
st.markdown(f"""<style>
.stApp{{background:{bg};color:{fg}}} [data-testid="stSidebar"]{{background:{panel}}}
[data-testid="stMetric"]{{background:{panel};border:1px solid #9bb5d022;border-radius:16px;padding:12px}}
.hero{{padding:26px;border-radius:22px;background:linear-gradient(110deg,#2457D622,#10A66A20,#7042C722);border:1px solid #7d9fc044}}
.hero h1{{font-size:2.5rem;font-weight:850;color:{fg};margin:0}} .muted{{color:{fg};opacity:.75}}
</style>""", unsafe_allow_html=True)
c1,c2 = st.columns([1,4])
with c1:
    logo=ASSETS/"logo_universidad_simon_bolivar.png"
    if logo.exists(): st.image(str(logo), use_container_width=True)
with c2:
    st.markdown(f'<div class="hero"><div class="muted">INGENIERÍA MULTIMEDIA · CÁLCULO INTEGRAL</div><h1>☀️ Solar Lab – Integral Insights</h1><p class="muted">{L["subtitle"]}</p></div>',unsafe_allow_html=True)
with st.sidebar:
    ml=ASSETS/("logo_ingenieria_multimedia_oscuro.png" if dark else "logo_ingenieria_multimedia_claro.png")
    if ml.exists(): st.image(str(ml),width=115)
    page=st.radio(L["nav"],[L["dashboard"],L["measure"],L["integral"],L["hyp"],L["history"],L["report"]])
    st.divider()
    st.markdown("**"+L["team"]+"**")
    for person in TEAM: st.caption("• "+person)
    st.markdown(L["institution"])

st.sidebar.subheader("⚙️ "+L["model"])
panels=st.sidebar.number_input(L["panels"],1,100,1)
pmax=st.sidebar.slider(L["peak"],50,600,300,10)
start=st.sidebar.slider(L["start"],6.0,12.0,6.0,.5)
end=st.sidebar.slider(L["end"],12.0,18.0,18.0,.5)
if end<=start: st.error("El intervalo final debe ser mayor que el inicial."); st.stop()

def power(t, peak): return peak*(1-((np.asarray(t)-12)**2)/36)
def primitive(t, peak): return peak*(t-((t-12)**3)/108)
def energy(a,b,peak): return float(primitive(b,peak)-primitive(a,peak))
def hour(v):
    if isinstance(v,(int,float,np.integer,np.floating)): return float(v)
    s=str(v).strip()
    if ":" in s:
        h,m=s.split(":")[:2]; return float(h)+float(m)/60
    return float(s)
def chart(x,y,title,ylabel,fill=False):
    fig,ax=plt.subplots(figsize=(9,3.4),dpi=140)
    ax.plot(x,y,color="#2457D6",lw=2.8)
    if fill: ax.fill_between(x,y,color="#10A66A",alpha=.18)
    ax.set_title(title); ax.set_xlabel("Hora / Time"); ax.set_ylabel(ylabel); ax.grid(alpha=.2); fig.tight_layout()
    return fig
x=np.linspace(start,end,241); y=power(x,pmax)*panels
e=energy(start,end,pmax)*panels
en=np.trapezoid(y,x) if hasattr(np,"trapezoid") else np.trapz(y,x)
avg=e/(end-start)
if "measurements" not in st.session_state: st.session_state.measurements=None
if "quality" not in st.session_state: st.session_state.quality=None

if page==L["dashboard"]:
    st.caption(L["intro"])
    a,b,c,d=st.columns(4)
    a.metric(L["max"],f"{pmax*panels:,.0f} W")
    b.metric(L["energy"],f"{e/1000:,.3f} kWh")
    c.metric(L["avg"],f"{avg:,.1f} W")
    d.metric("Diferencia analítica-numérica",f"{abs(e-en):.6f} Wh")
    fig=chart(x,y,L["model"],"Potencia (W)",True); st.pyplot(fig,use_container_width=True); plt.close(fig)
    st.latex(r"P(t)=P_{max}\left(1-\frac{(t-12)^2}{36}\right),\quad E=\int_a^b P(t)\,dt")
    st.info(L["conclusion"])
    st.markdown("### "+L["scenario"])
    rows=[{"Escenario":tag,"Potencia máxima (W)":pmax*panels*f,"Energía (kWh)":energy(start,end,pmax*f)*panels/1000} for f,tag in [(0.8,"−20 %"),(1,"Base"),(1.2,"+20 %")]]
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
elif page==L["measure"]:
    st.header("🧾 "+L["measure"]); st.info(L["help"])
    template=pd.DataFrame({"hora":["06:00","08:00","10:00","12:00","14:00","16:00","18:00"],"potencia_w":[0,133.33,233.33,300,233.33,133.33,0]})
    st.download_button(L["template"],template.to_csv(index=False).encode("utf-8-sig"),"plantilla_mediciones_solar.csv","text/csv")
    f=st.file_uploader(L["upload"],type=["csv"])
    if f:
        try:
            raw=pd.read_csv(f)
            if not {"hora","potencia_w"}.issubset(raw.columns): st.error("Se requieren las columnas hora y potencia_w.")
            else:
                raw=raw[["hora","potencia_w"]].copy()
                missing=int(raw.isna().any(axis=1).sum()); dup=int(raw.duplicated().sum())
                raw=raw.dropna(); raw["hora"]=raw["hora"].apply(hour); raw["potencia_w"]=pd.to_numeric(raw["potencia_w"],errors="coerce")
                raw=raw.dropna().sort_values("hora")
                neg=int((raw.potencia_w<0).sum()); out=0
                if len(raw)>=4:
                    q1,q3=raw.potencia_w.quantile([.25,.75]); out=int(((raw.potencia_w<q1-1.5*(q3-q1))|(raw.potencia_w>q3+1.5*(q3-q1))).sum())
                valid=len(raw)>=2 and raw.hora.nunique()>=2 and neg==0
                score=max(0,100-min(30,missing*5)-min(25,dup*5)-min(25,neg*10)-min(20,out*3))
                if valid:
                    xx=raw.hora.to_numpy(float); yy=raw.potencia_w.to_numpy(float)
                    cum=np.r_[0,np.cumsum(np.diff(xx)*(yy[1:]+yy[:-1])/2)]
                    raw["energia_acumulada_wh"]=cum
                    st.session_state.measurements=raw
                    st.session_state.quality={"valid":True,"missing":missing,"duplicates":dup,"negative":neg,"outliers":out,"score":score,"energy":float(cum[-1])}
                else: st.error("Se requieren al menos dos horas distintas y potencias no negativas.")
        except Exception as exc: st.error(f"Error al procesar el CSV: {exc}")
    m=st.session_state.measurements; q=st.session_state.quality
    if m is not None and q:
        a,b,c,d,e1=st.columns(5)
        a.metric(L["valid"],len(m)); b.metric(L["missing"],q["missing"]); c.metric(L["duplicates"],q["duplicates"]); d.metric(L["outliers"],q["outliers"]); e1.metric(L["quality"],f'{q["score"]:.0f}%')
        st.metric(L["measured_energy"],f'{q["energy"]:,.3f} Wh')
        st.dataframe(m,use_container_width=True,hide_index=True)
        fig=chart(m.hora,m.potencia_w,L["measure"],"Potencia (W)",True); st.pyplot(fig); plt.close(fig)
        if m.hora.nunique()>=3:
            coeff=np.polyfit(m.hora,m.potencia_w,2); xx=np.linspace(m.hora.min(),m.hora.max(),160); yy=np.polyval(coeff,xx)
            pred=np.polyval(coeff,m.hora); ssr=float(np.sum((m.potencia_w-pred)**2)); sst=float(np.sum((m.potencia_w-m.potencia_w.mean())**2)); r2=1-ssr/sst if sst else 1
            fig,ax=plt.subplots(figsize=(9,3.2)); ax.scatter(m.hora,m.potencia_w,label="Mediciones"); ax.plot(xx,yy,color="#10A66A",lw=2.5,label=L["curve"]); ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
            st.metric(L["r2"],f"{r2:.4f}")
    else: st.info(L["no_data"])
elif page==L["integral"]:
    st.header("∫ "+L["integral"])
    st.latex(r"F(t)=P_{max}\left(t-\frac{(t-12)^3}{108}\right)")
    st.write(f"**Energía analítica:** {e:,.4f} Wh ({e/1000:.4f} kWh)")
    st.write(f"**Regla del trapecio:** {en:,.4f} Wh")
    st.write(f"**Diferencia absoluta:** {abs(e-en):.8f} Wh")
    st.subheader(L["geometry"])
    a,b=st.columns(2)
    with a: length_panel=st.number_input("Largo del panel (m)",.1,5.,1.7,.05)
    with b: width_panel=st.number_input("Ancho del panel (m)",.1,5.,1.,.05)
    st.metric(L["area"],f"{length_panel*width_panel*panels:.4f} m²")
    st.caption("El área rectangular no equivale al área bajo la curva de potencia.")
    a,b,c=st.columns(3)
    with a: r0=st.number_input(L["radius"],.001,1.,.1,.01)
    with b: slope=st.number_input(L["slope"],0.,1.,.05,.01)
    with c: length=st.number_input(L["length"],.1,10.,2.,.1)
    volume=math.pi*(r0*r0*length+r0*slope*length**2+slope**2*length**3/3)
    st.metric("Volumen por revolución (m³)",f"{volume:.6f}")
    st.latex(r"V=\pi\int_0^L(r_0+mx)^2\,dx")
elif page==L["hyp"]:
    st.header("🧪 "+L["hyp"])
    variation=st.slider(L["factor"],-50,50,0,5); hypothetical=pmax*(1+variation/100)
    eh=energy(start,end,hypothetical)*panels
    a,b,c=st.columns(3); a.metric(L["max"],f"{hypothetical*panels:,.1f} W"); b.metric(L["energy"],f"{eh/1000:.4f} kWh"); c.metric("Cambio",f"{variation:+d}%")
    fig,ax=plt.subplots(figsize=(9,3.5)); ax.plot(x,y,label="Base",lw=2.5); ax.plot(x,power(x,hypothetical)*panels,label="Hipótesis",lw=2.5); ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    if st.button(L["save"],type="primary"):
        st.session_state.history.append({"fecha":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"variacion_pct":variation,"paneles":int(panels),"energia_kwh":eh/1000,"intervalo":f"{start:g}-{end:g}"})
        st.success("Escenario guardado.")
elif page==L["history"]:
    st.header("🕘 "+L["history"])
    if st.session_state.history:
        hist=pd.DataFrame(st.session_state.history); st.dataframe(hist,use_container_width=True,hide_index=True)
        st.download_button(L["download_csv"],hist.to_csv(index=False).encode("utf-8-sig"),"historial_solar_lab.csv","text/csv")
        if st.button(L["clear"]): st.session_state.history=[]; st.rerun()
    else: st.info(L["empty"])
elif page==L["report"]:
    st.header("📑 "+L["report"])
    st.markdown("**"+L["team"]+":** "+" · ".join(TEAM)); st.caption(L["institution"])
    rows=[{"hora":float(t),"potencia_w":float(v),"energia_acumulada_wh":float(energy(start,t,pmax)*panels)} for t,v in zip(x,y)]
    if st.session_state.measurements is not None: rows += st.session_state.measurements.to_dict("records")
    data=pd.DataFrame(rows); csv=data.to_csv(index=False).encode("utf-8-sig")
    pdf=io.BytesIO(); styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name="BlueTitle",parent=styles["Title"],textColor=colors.HexColor("#2457D6"),fontSize=19))
    doc=SimpleDocTemplate(pdf,pagesize=A4,rightMargin=1.7*cm,leftMargin=1.7*cm,topMargin=1.5*cm,bottomMargin=1.5*cm)
    story=[]
    for logo_path,w,h in [(ASSETS/"logo_universidad_simon_bolivar.png",14*cm,3*cm),(ASSETS/"logo_ingenieria_multimedia_claro.png",2.5*cm,2.5*cm)]:
        if logo_path.exists(): story.append(Image(str(logo_path),width=w,height=h,kind="proportional"))
    story += [Paragraph("Solar Lab – Integral Insights",styles["BlueTitle"]),Paragraph(L["subtitle"],styles["Heading2"]),Spacer(1,10),Paragraph(L["institution"],styles["BodyText"]),Spacer(1,8),Paragraph("<b>Equipo:</b> "+" · ".join(TEAM),styles["BodyText"]),Spacer(1,12)]
    table=[["Indicador","Resultado"],["Paneles",str(panels)],["Potencia máxima",f"{pmax*panels:.2f} W"],["Intervalo",f"{start:g}:00 – {end:g}:00"],["Energía analítica",f"{e:.4f} Wh"],["Energía numérica",f"{en:.4f} Wh"],["Diferencia",f"{abs(e-en):.8f} Wh"]]
    tb=Table(table,colWidths=[7*cm,8*cm]); tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2457D6")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#C8D7EE")),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F2F6FC")]),("PADDING",(0,0),(-1,-1),7)])); story.append(tb)
    story += [Spacer(1,14),Paragraph("Conclusión",styles["Heading2"]),Paragraph(L["conclusion"],styles["BodyText"]),Spacer(1,8),Paragraph(L["limitations"],styles["BodyText"])]
    doc.build(story); pdfbytes=pdf.getvalue()
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w",zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("informe_solar_lab.pdf",pdfbytes); archive.writestr("datos_solar_lab.csv",csv)
    st.download_button(L["download_pdf"],pdfbytes,"informe_solar_lab_integral_insights.pdf","application/pdf",type="primary")
    st.download_button(L["download_csv"],csv,"datos_solar_lab.csv","text/csv")
    st.download_button(L["download_zip"],z.getvalue(),"paquete_solar_lab.zip","application/zip")
st.divider()
st.caption("Solar Lab – Integral Insights · Universidad Simón Bolívar · Proyecto académico de Cálculo Integral")
