# -----------------------------------------------------------
# This app demonstrates the webcam detecting objects into the frame using cv2
# and generates interactive data visualization (graph) using Bokeh library.
#
# email dhruvdave61@gmail.com
# ----------------------------------------------------------


from object_detection import df
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

# it generates the full date and time when the object enters and exits from the frame
df["Start"] = pd.to_datetime(df.Start)
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End"] = pd.to_datetime(df.End)
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

# it creates the graph of object intervals into the frame
p = figure(x_axis_type='datetime', height=100, width=500,  title="Motion graph")
p.yaxis.minor_tick_line_color = None

# hover tool shows the date and time of the object intervals in the graph
hover = HoverTool(tooltips=[("Start ", "@Start_string"), ("End ", "@End_string")])
p.add_tools(hover)

# quadrant used to plot the time intervals of the objects in the frame
q = p.quad(left="Start", right="End", bottom=0, top=1, color="blue", source=cds)

output_file("Graph.html")

show(p)
