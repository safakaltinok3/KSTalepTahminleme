def monthly_heatmap(df, dfu_list):
    df['DFU'] = df['DFU'].fillna(method = 'ffill')
    data = []
    
    for d in range(len(dfu_list)):
        df_dfu = df[df['DFU'] == dfu_list[d]]
        for h in range(df.shape[1]-4):
            
            if df_dfu.iloc[0,h+4] == 0:
                 data.append([h,d,'-'])
    
            else:
                mape_daily = abs(df_dfu.iloc[0,h+4]-df_dfu.iloc[1,h+4])/df_dfu.iloc[0,h+4]
                mape_daily = int(mape_daily*10000)/100
                data.append([h,d,mape_daily])

    heat_map = {
       'tooltip': {
         'position': 'top'
       },
       'grid': {
         'height': '60%',
         'top': '10%'
       },
       'xAxis': {
         'type': 'category',
         'data': df.columns.tolist()[4:],
         'splitArea': {
           'show': 'true'
         }
       },
       'yAxis': {
        'type': 'category',
         'data': dfu_list,
         'splitArea': {
           'show': 'true'
         }
       },
       'visualMap': {
         'min': 0,
         'max': 200,
         'calculable': 'true',
         'orient': 'horizontal',
         'left': 'center',
         'bottom': '15%',
         'splitNumber': 8,
         'inRange': {
           'color': ['#f7fcf5',
                     '#e5f5e0',
                     '#c7e9c0',
                      '#a1d99b',
                      '#74c476',
                      '#41ab5d',
                      '#238b45',
                      '#006d2c', 
                      '#00441b'           
           ]
       }},
       'series': [
         {
           'name': 'Punch Card',
           'type': 'heatmap',
           'data': data,
           'label': {
             'show': 'true'
           },
           'emphasis': {
             'itemStyle': {
               'shadowBlur': 10,
               'shadowColor': 'rgba(0, 0, 0, 0.5)'
             }
           }
         }
       ]
     };
 
     
    return heat_map
        



def general_pie_chart(revenue):
    
    total = sum(revenue)
    per_revenue = []
    for i in range(len(revenue)):
        per_revenue.append(int(revenue[i]/total*10000)/100)

    columns = ['0-10 Hata', '10-20 Hata', '20-30 Hata', '30-50 Hata',
            '50-100 Hata', '<100 Hata']

    total_m = int(total/10000)/100    
    option = {
       'title': {
         'text': 'Yıllık Gelir (Yüzdesel) - Tahminlere Göre',
         'left': 'Toplam Gelir = '+ str(total_m) + ' milyon TL'
       },
      'tooltip': {
        'trigger': 'item'
      },
      # 'legend': {
      #   'orient': 'vertical',
      #   'left': 'left'
      # },
      'series': [
        {
          'name': '',
          'type': 'pie',
          'radius': '75%',
          # 'label': {
          #   'show': 'true',
          #   'formatter': function (params) {
          #     return echarts.time.format(params.value[0], '{dd}', false);
          #   },
          #   #offset: [-cellSize[0] / 2 + 10, -cellSize[1] / 2 + 10],
          #   fontSize: 14
          # },
          'data': [
            { 'value': per_revenue[0], 'name': columns[0] },
            { 'value': per_revenue[1], 'name':  columns[1]},
            { 'value': per_revenue[2], 'name':  columns[2]  },
            { 'value': per_revenue[3], 'name':  columns[3]},
            { 'value': per_revenue[4], 'name': columns[4] },
            { 'value': per_revenue[5], 'name':  columns[5]},
          ],
          'emphasis': {
            'itemStyle': {
              'shadowBlur': 10,
              'shadowOffsetX': 0,
              'shadowColor': 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };

    return option

def general_pie_chart2(revenue):
    
    total = sum(revenue)
    per_revenue = []
    for i in range(len(revenue)):
        per_revenue.append(int(revenue[i]/total*10000)/100)

    columns = ['0-10 Hata', '10-20 Hata', '20-30 Hata', '30-50 Hata',
            '50-100 Hata', '<100 Hata']

    total_m = int(total/10000)/100    
    option = {
       'title': {
         'text': 'Yıllık Satış Miktarı (Yüzdesel) - Tahminlere Göre',
         'left': 'Toplam Gelir = '+ str(total_m) + ' Adet/m2'
       },
      'tooltip': {
        'trigger': 'item'
      },
      # 'legend': {
      #   'orient': 'vertical',
      #   'left': 'left'
      # },
      'series': [
        {
          'name': '',
          'type': 'pie',
          'radius': '75%',
          # 'label': {
          #   'show': 'true',
          #   'formatter': function (params) {
          #     return echarts.time.format(params.value[0], '{dd}', false);
          #   },
          #   #offset: [-cellSize[0] / 2 + 10, -cellSize[1] / 2 + 10],
          #   fontSize: 14
          # },
          'data': [
            { 'value': per_revenue[0], 'name': columns[0] },
            { 'value': per_revenue[1], 'name':  columns[1]},
            { 'value': per_revenue[2], 'name':  columns[2]  },
            { 'value': per_revenue[3], 'name':  columns[3]},
            { 'value': per_revenue[4], 'name': columns[4] },
            { 'value': per_revenue[5], 'name':  columns[5]},
          ],
          'emphasis': {
            'itemStyle': {
              'shadowBlur': 10,
              'shadowOffsetX': 0,
              'shadowColor': 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };

    return option
def general_bar_plot(l1, l2,l3):
    option = {
  'tooltip': {
    'trigger': 'axis',
    'axisPointer': {
      'type': 'shadow'
    }
  },
  'legend': {
    'data': ['0-10 Hata', '10-20 Hata', '20-30 Hata', '30-50 Hata',
            '50-100 Hata', '<100 Hata']
  },
  'toolbox': {
    'show': 'true',
    'orient': 'vertical',
    'left': 'right',
    'top': 'center',
    'feature': {
      'mark': { 'show': 'true' },
      'dataView': { 'show': 'true', 'readOnly': 'false' },
      'magicType': { 'show': 'true', 'type': ['line', 'bar', 'stack'] },
      'restore': { 'show': 'true' },
      'saveAsImage': { 'show': 'true' }
    }
  },
  'xAxis': [
    {
      'type': 'category',
      'axisTick': { 'show': 'false' },
      'data': ['Time Serisi', 'ML - Satış', 'ML - Satış+Dış Veri']
    }
  ],
  'yAxis': [
    {
      'type': 'value'
    }
  ],
  'series': [
    {
      'name': '0-10 Hata',
      'type': 'bar',
      'barGap': 0,
      'label': {
          'show': 'true',
          'position': 'insideBottom',
          'distance': 15,
          'align': 'left',
          'verticalAlign': 'middle',
          'rotate': 90,
          'formatter': '{c}  {name|{a}}',
          'fontSize': 14,
          'rich': {
            'name': {}
          },},
      'emphasis': {
        'focus': 'series'
      },
      'data': [l1[0],l2[0],l3[0]]
    },
      
      {
        'name': '10-20 Hata',
        'type': 'bar',
        'barGap': 0,
        'label': {
            'show': 'true',
            'position': 'insideBottom',
            'distance': 15,
            'align': 'left',
            'verticalAlign': 'middle',
            'rotate': 90,
            'formatter': '{c}  {name|{a}}',
            'fontSize': 14,
            'rich': {
              'name': {}
            },},
        'emphasis': {
          'focus': 'series'
        },
        'data': [l1[1],l2[1],l3[1]]
      },
        
      {
        'name': '20-30 Hata',
        'type': 'bar',
        'barGap': 0,
        'label': {
            'show': 'true',
            'position': 'insideBottom',
            'distance': 15,
            'align': 'left',
            'verticalAlign': 'middle',
            'rotate': 90,
            'formatter': '{c}  {name|{a}}',
            'fontSize': 14,
            'rich': {
              'name': {}
            },},
        'emphasis': {
          'focus': 'series'
        },
        'data': [l1[2],l2[2],l3[2]]
      },
        
      {
        'name': '30-50 Hata',
        'type': 'bar',
        'barGap': 0,
        'label': {
            'show': 'true',
            'position': 'insideBottom',
            'distance': 15,
            'align': 'left',
            'verticalAlign': 'middle',
            'rotate': 90,
            'formatter': '{c}  {name|{a}}',
            'fontSize': 14,
            'rich': {
              'name': {}
            },},
        'emphasis': {
          'focus': 'series'
        },
        'data': [l1[3],l2[3],l3[3]]
      },
        
      {
        'name': '50-100 Hata',
        'type': 'bar',
        'barGap': 0,
        'label': {
            'show': 'true',
            'position': 'insideBottom',
            'distance': 15,
            'align': 'left',
            'verticalAlign': 'middle',
            'rotate': 90,
            'formatter': '{c}  {name|{a}}',
            'fontSize': 14,
            'rich': {
              'name': {}
            },},
        'emphasis': {
          'focus': 'series'
        },
        'data': [l1[4],l2[4],l3[4]]
      },
       
      {
        'name': '<100 Hata',
        'type': 'bar',
        'barGap': 0,
        'label': {
            'show': 'true',
            'position': 'insideBottom',
            'distance': 15,
            'align': 'left',
            'verticalAlign': 'middle',
            'rotate': 90,
            'formatter': '{c}  {name|{a}}',
            'fontSize': 14,
            'rich': {
              'name': {}
            },},
        'emphasis': {
          'focus': 'series'
        },
        'data': [l1[5],l2[5],l3[5]]
     
        }
  ]
};

    return option



def time_plot(test, pred, columns):
    #columns = df_time.columns.tolist()[1:]
    option = {
      # 'title': {
      #   text: 'Stacked Line'
      # },
      'labelLayout': {
       'moveOverlap': 'shiftY'
     },
     'emphasis': {
       'focus': 'series'
     },
      'animationDuration': 'true',
      
      'tooltip': {
        'trigger': 'axis'
      },
      'legend': {
        'data': ['Gerçek Değerler', 'Tahmin Değerleri']
      },
      'grid': {
        'left': '3%',
        'right': '4%',
        'bottom': '3%',
        'containLabel': 'true'
      },
      'toolbox': {
        'feature': {
          'saveAsImage': {}
        }
      },
      'xAxis': {
        'type': 'category',
        'boundaryGap': 'false',
        'data': columns
      },
      'yAxis': {
        'type': 'value'
      },
      'series': [
          {
                'name': 'Gerçek Değerler',
                'type': 'line',
                #'stack': 'Total',
                'smooth': 'true',
                "data": test,
            },
          {
                'name': 'Tahmin Değerleri',
                'type': 'line',
                #'stack': 'Total',
                'smooth': 'true',
                "data": pred,
            },
            
        
      ],
      "replaceMerge": ['series']
    };
    return option

def bar_plot(df_corr):
    
    echart_bar = {
        'grid': {
        'containLabel': 'true',
          },
        'legend': {
            'data': ['Ruhsat Alımları']
        },
          'xAxis': {
            'type': 'category',
            'data':df_corr.index.tolist(),
             'axisLabel': {
                      'rotate': 45, 
                    }
          },
          'yAxis': {
            'type': 'value'
          },
          'series': [
            {
              'name': 'Coefficient of Variations',
              'data': df_corr.values.tolist(),
              'type': 'bar',
              'showBackground': 'true',
              'backgroundStyle': {
                'color': 'rgba(180, 180, 180, 0.2)'
              }
              },
              
            
          ]
        };
    return echart_bar
def dis_time_plot(df):
    #columns = df_time.columns.tolist()[1:]
    option = {
      # 'title': {
      #   text: 'Stacked Line'
      # },
      'labelLayout': {
       'moveOverlap': 'shiftY'
     },
     'emphasis': {
       'focus': 'series'
     },
      'animationDuration': 'true',
      
      'tooltip': {
        'trigger': 'axis'
      },
      'legend': {
        'data': df.columns.tolist()
      },
      'grid': {
        'left': '3%',
        'right': '4%',
        'bottom': '3%',
        'containLabel': 'true'
      },
      'toolbox': {
        'feature': {
          'saveAsImage': {}
        }
      },
      'xAxis': {
        'type': 'category',
        'boundaryGap': 'false',
        'data': df.index.tolist()
      },
      'yAxis': {
        'type': 'value'
      },
      'series': [
          {
                'name': df.columns.tolist()[0],
                'type': 'line',
                #'stack': 'Total',
                'smooth': 'true',
                "data": df.iloc[:,0].values.tolist(),
            },
          {
                'name': df.columns.tolist()[1],
                'type': 'line',
                #'stack': 'Total',
                'smooth': 'true',
                "data": df.iloc[:,1].values.tolist(),
            },
            
        
      ],
      "replaceMerge": ['series']
    };
    return option