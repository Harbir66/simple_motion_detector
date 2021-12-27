## This small code that takes df from detect py and plots it in a readable manner

from bokeh.models.annotations import Tooltip
from detect import df 
from bokeh.plotting import figure,show,output_file
from bokeh.models import HoverTool,ColumnDataSource

df["start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["end_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")


cds=ColumnDataSource(df)


p=figure(x_axis_type='datetime',height=100,width=500,title="Motion Graph")
p.yaxis.minor_tick_line_color=None

hover=HoverTool(tooltips=[("Start","@start_string"),("End","@end_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="red",source=cds)

output_file("Graph1.html")
show(p)