import streamlit as st
import pandas as pd
import numpy as np

#Sehifenin nastroykasi
st.set_page_config(
    page_title='İstehsal',
    page_icon='logo.png',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# İstehsal \n Bu hesabat FAB şirkətlər qrupu üçün hazırlanmışdır."
    }
)

#Excel melumati oxuyuruq
@st.cache_data
def load_data():
    data = pd.read_excel('Excel.xlsx')
    return data

#Melumat yenilemek ucun knopka
res_button = st.sidebar.button(':red[🗘 Məlumatları Yenilə]')
if res_button:
    st.cache_data.clear()
with st.spinner('Məlumatlar yüklənir...'):
    data = load_data()

table_level = 0

data['sth_date'] = pd.to_datetime(data['sth_tarih']).dt.date    
data['year'] = data['sth_tarih'].dt.year

unique_years = data['year'].unique()

SELECT_YEARS = st.selectbox('İl', sorted(unique_years),
                                    label_visibility='visible')


data_finish_products = data[(data['year'] == SELECT_YEARS)
                            &
                            (data['table_no'] == 'TB1')
                            ]
data_finish_products_name = data_finish_products['sto_isim'].unique().tolist()

SELECT_PRODUCT_NAME = st.selectbox('Məhsul', sorted(data_finish_products_name),
                                    label_visibility='visible')

table_finish_product = data_finish_products[data_finish_products['sto_isim'] == SELECT_PRODUCT_NAME]
table_finish_product['Resept'] = False
show_table_column = ['sth_date','sth_stok_kod','sto_isim','sth_miktar','sth_tip']  

with st.expander('Göstər / Gizlət', expanded=True):
    selected_table_finish_product = st.data_editor(table_finish_product,
                   column_order=(show_table_column+['Resept']),
                   hide_index=True ,
                   disabled=show_table_column,
                   use_container_width=True)

    selected_finished_product_evrakno = selected_table_finish_product[selected_table_finish_product['Resept'] == True]['sth_evrakno_sira'].tolist()

if len(selected_finished_product_evrakno)>0:
    st.write(selected_finished_product_evrakno[-1])
    selected_finished_product_evrakno_sira = selected_finished_product_evrakno[-1]
    table_finish_product['Resept'] = False

    table_semi_product = data[(data['sth_evrakno_sira'] == selected_finished_product_evrakno_sira)
                                      &
                                      (data['table_no'] == 'TB2')
                                      ]
    table_semi_product['Resept'] = np.where(
                                            table_semi_product['sth_parti_kodu'].notna()
                                            &
                                            (table_semi_product['sth_parti_kodu'] != ''), False, None)
    
    with st.expander('Göstər / Gizlət', expanded=True):
        selected_table_semi_product = st.data_editor(table_semi_product,
                       column_order=(show_table_column+['Resept']),
                       hide_index=True ,
                       disabled=show_table_column,
                       use_container_width=True
                       )

    selected_semi_product_sth_parti = selected_table_semi_product[selected_table_semi_product['Resept'] == True]['sth_parti_kodu'].tolist()
    selected_semi_product_sth_kod = selected_table_semi_product[selected_table_semi_product['Resept'] == True]['sth_stok_kod'].tolist()
    
    if len(selected_semi_product_sth_parti)>0:
        selected_semi_product_evrakno = data[
                                            (data['sth_stok_kod'] == selected_semi_product_sth_kod[-1])
                                            &
                                            (data['sth_parti_kodu'] == selected_semi_product_sth_parti[-1])
                                            &
                                            (data['sth_tip'] == 'İstehsal')
                                             ]['sth_evrakno_sira'].tolist()

        if len(selected_semi_product_evrakno)>0:
            st.write(selected_semi_product_evrakno[-1])
            selected_semi_product_evrakno_sira = selected_semi_product_evrakno[-1]
            selected_table_semi_product['Resept'] = False
        
            table_raw_product = data[(data['sth_evrakno_sira'] == selected_semi_product_evrakno_sira)
                                              &
                                              (data['table_no'] == 'TB3')
                                              ]
            table_raw_product['Resept'] = ''
            
            with st.expander('Göstər / Gizlət', expanded=True):
                selected_table_raw_product = st.data_editor(table_raw_product,
                               column_order=(show_table_column+['Resept']),
                               hide_index=True ,
                               disabled=True,
                               use_container_width=True
                               )


css_page = """
<style>
    .stSlider [data-testid="stTickBar"] {
        display: none;
    }
    .stSlider label {
        display: block;
        text-align: left;
    }
    
    .stSelectbox label {
        text-align: left;
        display: block;
        width: 100%;
    }

    [data-testid="stHeader"] {
        display: none;
    }
    
    [class="viewerBadge_link__qRIco"] {
        display: none;
    }
    
    [data-testid="stElementToolbar"] {
        display: none;
    }
    
</style>
"""

st.markdown(css_page, unsafe_allow_html=True)