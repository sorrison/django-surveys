from pygooglechart import PieChart2D

colours = [
    '3374cd',
    '992220',
    '469b57',
    'e4e144',
    'cd3333',
    '749920',
    'ab346f',
    '6682bf',
    'dcab5e',
    '9a66bf',
    'b76683',
    '66aabf',
    '1f4590',
    'd8a303',
    '743920',
    '8ebf66',
]  

def pie_chart(data_dict, title=None):
        
    chart = PieChart2D(500, 225)
    
    chart_data = []
    chart_labels = []
    for label, value in data_dict.items():
        if value > 0:
            chart_labels.append(str(label))
            chart_data.append(value)
            
    if title:
        chart.title = title
        
    chart.add_data(chart_data)
    chart.set_pie_labels(chart_labels)
    chart.set_colours(colours[:len(data_dict)])
    return chart

