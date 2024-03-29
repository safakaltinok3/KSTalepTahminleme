import pandas as pd
import io
import panel as pn

from plot_functions import time_plot,general_bar_plot,general_pie_chart

from plot_functions import monthly_heatmap,general_pie_chart2
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

# =============================================================================
# Azure Connection and Container
# =============================================================================
# connection string is under access keys
connection_string = "https://ksforecasting.blob.core.windows.net/kstalep?sp=rl&st=2024-03-29T10:53:48Z&se=2024-03-29T18:53:48Z&spr=https&sv=2022-11-02&sr=c&sig=EuKY3alTO0MdlyBb%2BBc5gGC8vvNiKhuflE9Dw0xuwlc%3D"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "kstalep"
container_client = blob_service_client.get_container_client(container_name)


pn.extension('echarts')

def read_blob_file(file_name):
    blob_client_energy = container_client.get_blob_client(file_name)
    blob_data_energy = blob_client_energy.download_blob()
    csv_data_energy = blob_data_energy.readall()
    df = pd.read_csv(io.BytesIO(csv_data_energy))
    return df




df_yearly_perakende = read_blob_file('Yearly_Sales_DFU_Perakende.csv')
df_yearly_kurumsal = read_blob_file('Yearly_Sales_DFU_Kurumsal.csv')
df_yearly_yurtdisi = read_blob_file('Yearly_Sales_DFU_Yurtdisi.csv')

df_time = read_blob_file('Zaman_Serisi_Sonuçları_Perakende.csv')
df_ml1 = read_blob_file('ML_Satıştan_Tahmin_1m_Perakende.csv')
df_ml2 = read_blob_file('ML_Satış+DışVeri_Tahmin_1m_Perakende.csv')

df_ml1_3 = read_blob_file('ML_Satıştan_Tahmin_3m_Perakende.csv')
df_ml2_3 = read_blob_file('ML_Satış+DışVeri_Tahmin_3m_Perakende.csv')

df_time_kurumsal = read_blob_file('Zaman_Serisi_Sonuçları_Kurumsal.csv')
df_ml1_kurumsal = read_blob_file('ML_Satıştan_Tahmin_1m_Kurumsal.csv')
df_ml2_kurumsal = read_blob_file('ML_Satış+DışVeri_Tahmin_1m_Kurumsal.csv')

df_ml1_3_kurumsal = read_blob_file('ML_Satıştan_Tahmin_3m_Kurumsal.csv')
df_ml2_3_kurumsal = read_blob_file('ML_Satış+DışVeri_Tahmin_3m_Kurumsal.csv')

df_time_yurtdisi = read_blob_file('Zaman_Serisi_Sonuçları_Yurtdışı.csv')
df_ml1_yurtdisi = read_blob_file('ML_Satıştan_Tahmin_1m_Yurtdışı.csv')
df_ml2_yurtdisi = read_blob_file('ML_Satış+DışVeri_Tahmin_1m_Yurtdışı.csv')

df_ml1_3_yurtdisi = read_blob_file('ML_Satıştan_Tahmin_3m_Yurtdışı.csv')
df_ml2_3_yurtdisi = read_blob_file('ML_Satış+DışVeri_Tahmin_3m_Yurtdışı.csv')


funk_unique = df_yearly_perakende['FONKSİYON'].value_counts().index.tolist()

funk_dfu = {}
for funk in funk_unique:
    a = df_yearly_perakende[df_yearly_perakende['FONKSİYON'] == funk]
    funk_dfu[funk] = a['DFU1 (FONK+ANA GRUP+EBAT)'].value_counts().index.tolist()
    
select_funk =  pn.widgets.Select(name='Fonksiyon Seçin', 
                                  options=funk_unique)

dagitim_unique = ['Perakende', 'Yurtdışı', 'Kurumsal']
select_dagitim = pn.widgets.Select(name='Dağıtım Kanalı Seçin', 
                                  options=dagitim_unique)
sure_unique = ['Aylık Tahmin', 'Üç Aylık Tahmin']
select_sure = pn.widgets.Select(name='Tahmin Süresi Seçin', 
                                  options=sure_unique)
metrik_unique = ['MAPE', 'Normalize Edilmiş MAE']
select_metrik = pn.widgets.Select(name='Tahmin Metriği Seçin', 
                                  options=metrik_unique)
button_general = pn.widgets.Button(name='Analiz için Buraya Tıklayın', button_type="success", 
                                    align = 'center')

def general_analysis_plot(event):
    if button_general.clicks > -1:
        if select_dagitim.value == 'Perakende':
            if select_sure.value == 'Aylık Tahmin':
                df_time_used = df_time
                df_ml1_used = df_ml1
                df_ml2_used = df_ml2
            elif select_sure.value == 'Üç Aylık Tahmin':
                df_time_used = df_time
                df_ml1_used = df_ml1_3
                df_ml2_used = df_ml2_3
            df_yearly = df_yearly_perakende
        elif select_dagitim.value == 'Kurumsal':
            if select_sure.value == 'Aylık Tahmin':
                df_time_used = df_time_kurumsal
                df_ml1_used = df_ml1_kurumsal
                df_ml2_used = df_ml2_kurumsal
            elif select_sure.value == 'Üç Aylık Tahmin':
                df_time_used = df_time_kurumsal
                df_ml1_used = df_ml1_3_kurumsal
                df_ml2_used = df_ml2_3_kurumsal
            df_yearly = df_yearly_kurumsal

                
        else:
            if select_sure.value == 'Aylık Tahmin':
                df_time_used = df_time_yurtdisi
                df_ml1_used = df_ml1_yurtdisi
                df_ml2_used = df_ml2_yurtdisi
            elif select_sure.value == 'Üç Aylık Tahmin':
                df_time_used = df_time_yurtdisi
                df_ml1_used = df_ml1_3_yurtdisi
                df_ml2_used = df_ml2_3_yurtdisi
                
            df_yearly = df_yearly_yurtdisi

            
                
        ranges = [0,0.1,0.20,0.30,0.50,1]
        time_count = []
        ml1_count = []
        ml2_count = []
        funk_sales = df_yearly[df_yearly_perakende['DFU1 (FONK+ANA GRUP+EBAT)'
                                ].isin(funk_dfu[select_funk.value])]
        revenue = []
        miktar = []
        metrik_selected = select_metrik.value
        for k in range(len(ranges)):
            a = df_time_used[df_time_used['DFU'].isin(funk_dfu[select_funk.value])]
            if k != len(ranges)-1:
                b = a[(a[metrik_selected] > ranges[k]) &(a[metrik_selected] < ranges[k+1])]
            else:
                b = a[(a[metrik_selected] > ranges[k])]
            time_count.append(len(b))
            
            a = df_ml1_used[df_ml1_used['DFU'].isin(funk_dfu[select_funk.value])]
            if k != len(ranges)-1:
                b = a[(a[metrik_selected] > ranges[k]) &((a[metrik_selected] < ranges[k+1]))]
            else:
                b = a[(a[metrik_selected] > ranges[k])]
            ml1_count.append(len(b))
            a = df_ml2_used[df_ml2_used['DFU'].isin(funk_dfu[select_funk.value])]
            if k != len(ranges)-1:
                b = a[(a[metrik_selected] > ranges[k]) &((a[metrik_selected] < ranges[k+1]))]
            else:
                b = a[(a[metrik_selected] > ranges[k])]
            ml2_count.append(len(b))
            
            c = funk_sales[funk_sales['DFU1 (FONK+ANA GRUP+EBAT)'].isin(
                b['DFU'].values.tolist())]
            
            revenue.append(c['Fiili Net TL'].sum())
            miktar.append(c['Fiili Miktar (TÖB)'].sum())
        
            
                        
        general_pie = general_pie_chart(revenue)
        general_pie2 = general_pie_chart2(miktar)

        
        pred_plt = general_bar_plot(time_count, ml1_count, ml2_count)
        return  pn.Column(pn.pane.ECharts(pred_plt, width=1200, height=600),
                          pn.Row(pn.pane.ECharts(general_pie, width=600, height=600),
                                 pn.pane.ECharts(general_pie2, width=600, height=600)))
  

component_general_analysis = pn.Column(pn.Row(select_funk,select_dagitim, select_sure,select_metrik)
                                   , button_general,pn.panel(pn.bind(general_analysis_plot, button_general), loading_indicator=True))

#############################################################################

funk_dict = {}
for funk in funk_unique:
    a = df_yearly_perakende[df_yearly_perakende['FONKSİYON'] == funk]
    funk_dict[funk] = a['ANA GRUP'].value_counts().index.tolist()

select_funk_heat =  pn.widgets.Select(name='Fonksiyon Seçin', 
                                  options=funk_unique) 


select_ana_heat = pn.widgets.Select(name='Ana Grup Seçin', 
                                  options=funk_dict[select_funk_heat.value])

def callback(target, event):
    target.options = funk_dict[event.new]

select_funk_heat.link(select_ana_heat, callbacks={'value': callback})

ana_unique = df_yearly_perakende['ANA GRUP'].value_counts().index.tolist()
and_dict = {}
for ana in ana_unique:
    a = df_yearly_perakende[df_yearly_perakende['ANA GRUP'] == ana]
    and_dict[ana] = a['DFU1 (FONK+ANA GRUP+EBAT)'].value_counts().index.tolist()


select_dagitim_heat = pn.widgets.Select(name='Dağıtım Kanalı Seçin', 
                                  options=dagitim_unique)

select_sure_beat = pn.widgets.Select(name='Tahmin Süresi Seçin', 
                                  options=sure_unique)


button_heat= pn.widgets.Button(name='Analiz için Buraya Tıklayın', button_type="success", 
                                    align = 'center')



def heatmap_plot(event):
    if button_heat.clicks > -1:
        if select_dagitim_heat.value == 'Perakende':
            if select_sure_beat.value == 'Aylık Tahmin':
                
                df_ml2_used = df_ml2
            elif select_sure_beat.value == 'Üç Aylık Tahmin':
                
                df_ml2_used = df_ml2_3
        
        elif select_dagitim_heat.value == 'Kurumsal':
            if select_sure_beat.value == 'Aylık Tahmin':
                
                df_ml2_used = df_ml2_kurumsal
            elif select_sure_beat.value == 'Üç Aylık Tahmin':
                
                df_ml2_used = df_ml2_3_kurumsal
                
        else:
            if select_sure_beat.value == 'Aylık Tahmin':
                
                df_ml2_used = df_ml2_yurtdisi
            elif select_sure_beat.value == 'Üç Aylık Tahmin':
                
                df_ml2_used = df_ml2_3_yurtdisi
             
        df_ml2_used['DFU'] = df_ml2_used['DFU'].fillna(method = 'ffill')
                        
        intersected_list = []

        for element in and_dict[select_ana_heat.value]:

          if element in df_ml2_used['DFU'].values.tolist():

              intersected_list.append(element)
        
        return pn.pane.ECharts(monthly_heatmap(df_ml2_used,intersected_list
                                        ), width=1200, height=50*len(intersected_list))
        
        
  

component_heatmap = pn.Column(pn.Row(select_funk_heat,select_ana_heat, select_dagitim_heat,
                                     select_sure_beat),
                                     button_heat,
                      pn.panel(pn.bind(heatmap_plot, button_heat), loading_indicator=True),)



#################################################################################

funk_dict = {}
for funk in funk_unique:
    a = df_yearly_perakende[df_yearly_perakende['FONKSİYON'] == funk]
    funk_dict[funk] = a['ANA GRUP'].value_counts().index.tolist()

select_funk_pred =  pn.widgets.Select(name='Fonksiyon Seçin', 
                                  options=funk_unique) 


select_ana = pn.widgets.Select(name='Ana Grup Seçin', 
                                  options=funk_dict[select_funk_pred.value])

def callback(target, event):
    target.options = funk_dict[event.new]

select_funk_pred.link(select_ana, callbacks={'value': callback})

ana_unique = df_yearly_perakende['ANA GRUP'].value_counts().index.tolist()
and_dict = {}
for ana in ana_unique:
    a = df_yearly_perakende[df_yearly_perakende['ANA GRUP'] == ana]
    and_dict[ana] = a['DFU1 (FONK+ANA GRUP+EBAT)'].value_counts().index.tolist()

select_dfu = pn.widgets.Select(name='Ana Grup Seçin', 
                                  options=and_dict[select_ana.value])

def callback(target, event):
    target.options = and_dict[event.new]

select_ana.link(select_dfu, callbacks={'value': callback})

select_dagitim_pred = pn.widgets.Select(name='Dağıtım Kanalı Seçin', 
                                  options=dagitim_unique)

select_sure_pred = pn.widgets.Select(name='Tahmin Süresi Seçin', 
                                  options=sure_unique)


button_pred= pn.widgets.Button(name='Çizim için Buraya Tıklayın', button_type="success", 
                                    align = 'center')

def dfu_tahmin_plot(event):
    if button_pred.clicks > -1:
        if select_dagitim_pred.value == 'Perakende':
            if select_sure_pred.value == 'Aylık Tahmin':
                df_ml2_used = df_ml2

            elif select_sure_pred.value == 'Üç Aylık Tahmin':
                df_ml2_used = df_ml2_3
        
        elif select_dagitim_pred.value == 'Kurumsal':
            if select_sure_pred.value == 'Aylık Tahmin':
                df_ml2_used = df_ml2_kurumsal

            elif select_sure_pred.value == 'Üç Aylık Tahmin':
                df_ml2_used = df_ml2_3_kurumsal
                
        else:
            if select_sure_pred.value == 'Aylık Tahmin':
                df_ml2_used = df_ml2_yurtdisi

            elif select_sure_pred.value == 'Üç Aylık Tahmin':
                df_ml2_used = df_ml2_3_yurtdisi
                
        df_ml2_used['DFU'] = df_ml2_used['DFU'].fillna(method = 'ffill')
        
        a = df_ml2_used[df_ml2_used['DFU'] == select_dfu.value]        
        
        mape_value = int(10000*a['MAPE'].iloc[0])/100
        if mape_value > 10**5:
            mape_value = 10**5
        
        ind_mape = pn.indicators.Number(name='MAPE', value=mape_value, 
                                                #format='{mape}',
                                                colors=[(100, 'green'), (1000, 'gold'), (10000, 'red')])

        
        pred_plt = time_plot(a.iloc[0,4:], a.iloc[1,4:], a.columns.tolist()[4:])
        return  pn.Row(pn.pane.ECharts(pred_plt, width=900, height=600),ind_mape)
  

component_pred_time = pn.Column(pn.Row(select_funk_pred,select_ana, select_dfu),
                                    pn.Row(select_dagitim_pred, select_sure_pred ), button_pred,
                      pn.panel(pn.bind(dfu_tahmin_plot, button_pred), loading_indicator=True),)

#################################################################################

tabs_machine = pn.Tabs(
    ('Genel Tahmin Analizi',component_general_analysis),
    ('Aylık Tahmin Analizi',component_heatmap),
    ('Tahmin Çizimi',component_pred_time),
    dynamic=False
    )


template = pn.template.MaterialTemplate(title="Kale Seramik Satış Tahmin Analizi")


template.main.append( tabs_machine)

template.servable()



