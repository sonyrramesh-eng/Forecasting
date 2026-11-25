from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='DengueWATCH | AI Analytics', page_icon='🦟', layout='wide', initial_sidebar_state='expanded')
BASE = Path(__file__).resolve().parent.parent
OUT = BASE / 'outputs'

# ---------- Premium visual system ----------
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--bg:#070b18;--panel:#101a30;--panel2:#14213b;--line:rgba(99,183,255,.18);--cyan:#42e8f5;--teal:#38d9bd;--muted:#8fa4c5;--white:#edf5ff}
.stApp{background:radial-gradient(ellipse at 80% 0%,#142849 0%,#090f20 42%,#070b18 78%);color:var(--white);font-family:'DM Sans',sans-serif}
.block-container{max-width:1500px;padding-top:1.6rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1830 0%,#091224 100%);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:#dceaff}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#152440;border:1px solid #294362}
[data-testid="stHeader"]{background:transparent}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;color:#f3f8ff!important;letter-spacing:-.03em}
.hero{padding:28px 32px;border:1px solid rgba(66,232,245,.28);border-radius:22px;background:linear-gradient(115deg,rgba(19,48,79,.95),rgba(26,31,67,.92));box-shadow:0 18px 55px rgba(0,0,0,.25),inset 0 1px rgba(255,255,255,.05);margin-bottom:26px;position:relative;overflow:hidden}
.hero:after{content:'';position:absolute;width:240px;height:240px;right:-55px;top:-120px;border-radius:50%;background:rgba(66,232,245,.13);filter:blur(8px)}
.eyebrow{color:#54eaf3;font-size:11px;letter-spacing:.18em;font-weight:700;text-transform:uppercase}
.hero-title{font:700 34px 'Space Grotesk';margin:7px 0;color:#fff}.hero-sub{color:#a9c5e6;font-size:13px}
.kpi{background:linear-gradient(145deg,rgba(20,36,63,.98),rgba(13,24,44,.98));border:1px solid rgba(100,174,230,.22);border-radius:17px;padding:19px 20px;min-height:116px;box-shadow:0 12px 30px rgba(0,0,0,.16)}
.kpi-label{color:#91aacb;font-size:11px;text-transform:uppercase;letter-spacing:.11em;font-weight:600}.kpi-value{font:700 29px 'Space Grotesk';color:#47e5f1;margin-top:8px}.kpi-note{font-size:11px;color:#8199bb;margin-top:3px}
.panel{background:rgba(15,27,49,.78);border:1px solid rgba(99,183,255,.16);border-radius:17px;padding:18px 20px}
.section-kicker{color:#46e5ee;font-size:12px;text-transform:uppercase;letter-spacing:.14em;font-weight:700;margin-bottom:5px}
div[data-testid="stPlotlyChart"]{background:rgba(14,25,45,.7);border:1px solid rgba(99,183,255,.13);border-radius:15px;padding:8px}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px}
.stButton>button{border:1px solid #2d718b;background:linear-gradient(90deg,#123e59,#174b61);color:#eaffff;border-radius:10px}
hr{border-color:rgba(99,183,255,.15)}
small,.muted{color:#8fa4c5}

/* DISTRICT SELECTBOX: dark text on its light selected-value surface */
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #42e8f5 !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"],
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #14243b !important;
    -webkit-text-fill-color: #14243b !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] input {
    color: #14243b !important;
    -webkit-text-fill-color: #14243b !important;
    caret-color: #14243b !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] svg {
    fill: #14243b !important;
    color: #14243b !important;
}
/* Open options list: readable white text on navy */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"] {
    background-color: #14243b !important;
    color: #ffffff !important;
}
[data-baseweb="popover"] [role="option"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
</style>''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_csv(name, required=True):
    p=OUT/name
    if not p.exists():
        if required: raise FileNotFoundError(f'Missing required project file: {p}')
        return pd.DataFrame()
    return pd.read_csv(p)

try:
    daily=load_csv('karnataka_dengue_rainfall_combined.csv')
    monthly=load_csv('karnataka_monthly_dengue_trend.csv')
    predictions=load_csv('forecasting_model_predictions.csv')
    performance=load_csv('forecasting_model_performance.csv')
    rainfall=load_csv('karnataka_monthly_rainfall.csv',False)
    correlations=load_csv('validated_district_correlations.csv',False)
except Exception as e:
    st.error(f'Data loading issue: {e}')
    st.stop()

for frame,col in [(daily,'date'),(monthly,'month'),(predictions,'month'),(rainfall,'month')]:
    if col in frame.columns: frame[col]=pd.to_datetime(frame[col],errors='coerce')

# Sidebar
with st.sidebar:
    st.markdown('## 🦟 DengueWATCH')
    st.caption('KARNATAKA · DISEASE INTELLIGENCE')
    st.markdown('---')
    page=st.radio('WORKSPACE',['Command Center','Dengue Trends','District Intelligence','Rainfall Signals','Forecast Lab','Data Explorer'],label_visibility='visible')
    st.markdown('---')
    st.markdown('**GLOBAL FILTERS**')
    districts=['All Districts']+sorted(daily['district'].dropna().astype(str).unique().tolist())
    district=st.selectbox('District',districts)
    min_date=daily.date.min().date(); max_date=daily.date.max().date()
    date_range=st.date_input('Date range',value=(min_date,max_date),min_value=min_date,max_value=max_date)
    st.markdown('---')
    st.caption('Data view · Existing project datasets')

if isinstance(date_range,(tuple,list)) and len(date_range)==2:
    start,end=pd.Timestamp(date_range[0]),pd.Timestamp(date_range[1])
else: start,end=pd.Timestamp(min_date),pd.Timestamp(max_date)
filtered=daily[(daily.date>=start)&(daily.date<=end)].copy()
if district!='All Districts': filtered=filtered[filtered.district==district]

cases=float(filtered.daily_cases.sum()) if not filtered.empty else 0
suspected=float(filtered.daily_suspected.sum()) if not filtered.empty else 0
deaths=float(filtered.daily_deaths.sum()) if not filtered.empty else 0
district_count=int(filtered.district.nunique()) if not filtered.empty else 0

def hero(tag,title,subtitle):
    st.markdown(f'<div class="hero"><div class="eyebrow">{tag}</div><div class="hero-title">🦟 {title}</div><div class="hero-sub">{subtitle}</div></div>',unsafe_allow_html=True)
def kpi(label,value,note='Selected period'):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',unsafe_allow_html=True)
def chart_layout(fig,height=360):
    fig.update_layout(height=height,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans',color='#dceaff'),margin=dict(l=18,r=18,t=38,b=18),legend=dict(orientation='h',y=1.12))
    fig.update_xaxes(showgrid=False,zeroline=False)
    fig.update_yaxes(gridcolor='rgba(143,164,197,.12)',zeroline=False)
    return fig

if page=='Command Center':
    hero('KARNATAKA DISEASE INTELLIGENCE / OVERVIEW','Command Center','A unified view of reported dengue activity, district coverage and historical signals.')
    cols=st.columns(4)
    for c,(lab,val,note) in zip(cols,[('TOTAL DENGUE CASES',f'{cases:,.0f}','Confirmed cases in selected period'),('SUSPECTED CASES',f'{suspected:,.0f}','Reported suspected cases'),('REPORTED DEATHS',f'{deaths:,.0f}','Reported deaths'),('DISTRICTS COVERED',f'{district_count:,}','Districts with records')]):
        with c:kpi(lab,val,note)
    st.markdown('')
    a,b=st.columns([1.65,1])
    with a:
        st.markdown('### Dengue activity timeline')
        trend=filtered.groupby('date',as_index=False).agg(cases=('daily_cases','sum'),suspected=('daily_suspected','sum'))
        fig=px.area(trend,x='date',y='cases',labels={'date':'Date','cases':'Cases'},color_discrete_sequence=['#39ddea'])
        st.plotly_chart(chart_layout(fig,370),width='stretch')
    with b:
        st.markdown('### District case leaders')
        top=filtered.groupby('district',as_index=False).daily_cases.sum().nlargest(10,'daily_cases').sort_values('daily_cases')
        fig=px.bar(top,x='daily_cases',y='district',orientation='h',labels={'daily_cases':'Cases','district':''},color='daily_cases',color_continuous_scale=['#15506a','#42e8f5'])
        st.plotly_chart(chart_layout(fig,370),width='stretch')
    st.caption('Figures are aggregated from the supplied project dataset and respond to the sidebar filters.')

elif page=='Dengue Trends':
    hero('TIME-SERIES ANALYTICS','Dengue Trends','Explore monthly case movement, suspected reports and reported deaths.')
    d=monthly.copy()
    if district!='All Districts':
        # Monthly source is statewide; use selected district's daily data instead.
        d=filtered.assign(month=filtered.date.dt.to_period('M').dt.to_timestamp()).groupby('month',as_index=False).agg(total_dengue_cases=('daily_cases','sum'),total_suspected=('daily_suspected','sum'),total_deaths=('daily_deaths','sum'))
    else:
        d=d[(d.month>=start)&(d.month<=end)]
    c1,c2=st.columns([1.5,1])
    with c1:
        st.markdown('### Monthly confirmed cases')
        fig=px.area(d,x='month',y='total_dengue_cases',labels={'month':'Month','total_dengue_cases':'Cases'},color_discrete_sequence=['#42e8f5'])
        fig.update_traces(line_width=2,fillcolor='rgba(66,232,245,.13)')
        st.plotly_chart(chart_layout(fig,390),width='stretch')
    with c2:
        st.markdown('### Case composition')
        vals={'Confirmed':d.total_dengue_cases.sum(),'Suspected':d.total_suspected.sum()}
        fig=px.pie(names=list(vals),values=list(vals.values()),hole=.68,color_discrete_sequence=['#42e8f5','#9b8cff'])
        st.plotly_chart(chart_layout(fig,390),width='stretch')
    st.markdown('### Monthly reporting table')
    st.dataframe(d,use_container_width=True,hide_index=True)

elif page=='District Intelligence':
    hero('GEOSPATIAL & DISTRICT VIEW','Karnataka District Map','Click any district on the map to view its dengue case count and reporting details.')
    import json
    import pydeck as pdk
    map_file = BASE / 'data' / 'maps' / 'karnataka_31_districts.geojson'
    if not map_file.exists():
        st.error(f'Karnataka district boundary file not found: {map_file}')
        st.stop()
    with map_file.open('r', encoding='utf-8') as f:
        karnataka_geo = json.load(f)
    by=filtered.groupby('district',as_index=False).agg(cases=('daily_cases','sum'),suspected=('daily_suspected','sum'),deaths=('daily_deaths','sum'),records=('date','count'))
    # Align source spelling with the official boundary file.
    aliases={'VIJAYANAGAR':'VIJAYANAGARA','DAVANGERE':'DAVANAGERE'}
    by['map_district']=by['district'].replace(aliases)
    lookup=by.set_index('map_district').to_dict('index')
    maximum=max(1.0,float(by['cases'].max()) if not by.empty else 1.0)
    for feature in karnataka_geo.get('features',[]):
        props=feature.setdefault('properties',{})
        map_name=props.get('DISTRICT','')
        values=lookup.get(map_name,{})
        cases=float(values.get('cases',0) or 0)
        intensity=min(1.0,cases/maximum)
        props['cases']=cases
        props['suspected']=float(values.get('suspected',0) or 0)
        props['deaths']=float(values.get('deaths',0) or 0)
        props['records']=int(values.get('records',0) or 0)
        props['source_district']=str(values.get('district',map_name))
        props['fill_color']=[int(12+intensity*35),int(65+intensity*155),int(92+intensity*145),210]
    layer=pdk.Layer('GeoJsonLayer',data=karnataka_geo,id='district-polygons',pickable=True,stroked=True,filled=True,extruded=False,auto_highlight=True,get_fill_color='properties.fill_color',get_line_color=[92,205,230,220],line_width_min_pixels=1)
    view=pdk.ViewState(latitude=15.2,longitude=76.0,zoom=5.0,min_zoom=4,max_zoom=9,pitch=0,bearing=0)
    deck=pdk.Deck(layers=[layer],initial_view_state=view,map_style='dark',tooltip={'html':'<b>{DISTRICT}</b><br/>Confirmed cases: {cases}<br/>Suspected: {suspected}<br/>Deaths: {deaths}','style':{'backgroundColor':'#101a30','color':'#eaf4ff'}})
    st.markdown('### Interactive Karnataka map · select a district')
    try:
        map_event=st.pydeck_chart(deck,width='stretch',on_select='rerun',selection_mode='single-object',key='karnataka_district_map')
        objects=(map_event.selection.objects or {}) if map_event and map_event.selection else {}
        selected_objects=objects.get('district-polygons',[])
        if selected_objects:
            props=selected_objects[0]
            clicked_name=props.get('source_district') or props.get('DISTRICT')
            if clicked_name in by['district'].values:
                st.session_state['map_selected_district']=clicked_name
    except TypeError:
        st.pydeck_chart(deck,width='stretch')
        st.caption('Your Streamlit version does not expose map selection. Use the district selector below.')
    choices=['Select from list']+sorted(by['district'].dropna().astype(str).unique().tolist())
    previous=st.session_state.get('map_selected_district','')
    default_index=choices.index(previous) if previous in choices else 0
    chosen=st.selectbox('Or choose a district',choices,index=default_index,key='district_map_fallback')
    selected=chosen if chosen!='Select from list' else st.session_state.get('map_selected_district','')
    if selected and selected in by['district'].values:
        row=by.loc[by.district==selected].iloc[0]
        st.markdown(f'## {selected.title()}')
        m1,m2,m3,m4=st.columns(4)
        with m1:kpi('CONFIRMED CASES',f"{row['cases']:,.0f}",'Selected district')
        with m2:kpi('SUSPECTED CASES',f"{row['suspected']:,.0f}",'Selected district')
        with m3:kpi('REPORTED DEATHS',f"{row['deaths']:,.0f}",'Selected district')
        with m4:kpi('RECORDS',f"{row['records']:,.0f}",'Daily records in period')
        district_daily=filtered[filtered.district==selected].sort_values('date')
        if not district_daily.empty:
            detail_fig=px.area(district_daily,x='date',y='daily_cases',labels={'date':'Date','daily_cases':'Confirmed cases'},color_discrete_sequence=['#42e8f5'])
            st.plotly_chart(chart_layout(detail_fig,300),width='stretch')
    else:
        st.info('Click a district polygon on the map to see its case count, suspected cases, deaths and daily trend.')
    st.caption('Counts come from your existing filtered dataset. No outbreak risk score or new forecast is fabricated.')

elif page=='Rainfall Signals':
    hero('CLIMATE & DISEASE SIGNALS','Rainfall Signals','Review rainfall patterns and the validated district-level lag correlations in your project outputs.')
    if rainfall.empty:
        st.warning('Monthly rainfall output is not available in outputs/.')
    else:
        r=rainfall[(rainfall.month>=start)&(rainfall.month<=end)]
        a,b=st.columns([1.5,1])
        with a:
            st.markdown('### Average monthly rainfall')
            fig=px.area(r,x='month',y='average_district_rainfall_mm',labels={'month':'Month','average_district_rainfall_mm':'Average rainfall (mm)'},color_discrete_sequence=['#9b8cff'])
            st.plotly_chart(chart_layout(fig,360),width='stretch')
        with b:
            st.markdown('### Rainfall coverage')
            fig=px.bar(r,x='month',y='districts_reporting',labels={'month':'Month','districts_reporting':'Districts reporting'},color_discrete_sequence=['#42e8f5'])
            st.plotly_chart(chart_layout(fig,360),width='stretch')
    if not correlations.empty:
        st.markdown('### Validated rainfall lag correlations')
        cc=correlations.copy()
        if district!='All Districts': cc=cc[cc.district==district]
        fig=px.scatter(cc,x='rainfall_lag_months',y='correlation',color='district',size='months_compared',hover_data=['months_compared'],labels={'rainfall_lag_months':'Rainfall lag (months)','correlation':'Correlation','district':'District'},color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(chart_layout(fig,420),width='stretch')
        st.caption('Correlation indicates association in the analyzed data; it does not establish causation.')
    else: st.warning('Validated district correlation output is not available.')

elif page=='Forecast Lab':
    hero('MODEL EVALUATION WORKSPACE','Forecast Lab','Inspect the saved model evaluation and prediction outputs. No models are retrained here.')
    a,b=st.columns([1,1.5])
    with a:
        st.markdown('### Model performance')
        st.dataframe(performance,use_container_width=True,hide_index=True)
        best=performance.loc[performance['MAE'].idxmin()] if {'MAE','Model'}.issubset(performance.columns) and not performance.empty else None
        if best is not None:
            st.markdown(f'<div class="panel"><div class="section-kicker">LOWEST MAE IN SAVED EVALUATION</div><h3>{best["Model"]}</h3><span class="muted">MAE: {float(best["MAE"]):,.2f}</span></div>',unsafe_allow_html=True)
    with b:
        st.markdown('### Actual vs saved predictions')
        p=predictions.copy()
        cols=[c for c in ['actual_cases','baseline_prediction','model_a_prediction','model_b_prediction'] if c in p.columns]
        long=p.melt(id_vars='month',value_vars=cols,var_name='series',value_name='cases')
        fig=px.line(long,x='month',y='cases',color='series',markers=True,labels={'month':'Month','cases':'Cases','series':'Series'},color_discrete_sequence=['#42e8f5','#9b8cff','#38d9bd','#ffbd69'])
        st.plotly_chart(chart_layout(fig,400),width='stretch')
    st.dataframe(predictions,use_container_width=True,hide_index=True)
    st.warning('The saved evaluation uses a small test period. Treat these outputs as an experimental comparison, not a reliable live outbreak warning.')

elif page=='Data Explorer':
    hero('TRANSPARENT DATA ACCESS','Data Explorer','Filter, inspect and export the underlying combined dengue-rainfall records.')
    st.markdown(f'**{len(filtered):,}** records match the current filters.')
    search=st.text_input('Search within visible records',placeholder='Enter district name or value...')
    view=filtered.copy()
    if search:
        mask=view.astype(str).apply(lambda col: col.str.contains(search,case=False,na=False)).any(axis=1)
        view=view[mask]
    st.dataframe(view,use_container_width=True,height=500,hide_index=True)
    st.download_button('⬇ Download filtered CSV',data=view.to_csv(index=False).encode('utf-8'),file_name='denguewatch_filtered_data.csv',mime='text/csv')

st.markdown('<hr><div style="display:flex;justify-content:space-between;color:#7188a9;font-size:11px"><span>DENGUEWATCH · KARNATAKA</span><span>Research dashboard · Historical project data</span></div>',unsafe_allow_html=True)
