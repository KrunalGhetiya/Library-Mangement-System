import pandas as pd
from matplotlib import pyplot as plt
usage = pd.read_csv("user_usage.csv")
usage
device = pd.read_csv("user_device.csv")
device
a = usage.merge(device,on="use_id")
a
s=['device','monthly_mb']
r=a[s]
t=r.groupby('device').sum().reset_index().sort_values('monthly_mb')
plt.plot(t['device'],t['monthly_mb'])
plt.title('Device vs Monthly_Mb')
plt.xlabel('Device')
plt.ylabel('Monthly_mb')
plt.show()
s=['device','outgoing_mins_per_month']
r=a[s]
t=r.groupby('device').sum().reset_index().sort_values('outgoing_mins_per_month')
plt.plot(t['device'],t['outgoing_mins_per_month'])
plt.title('Device vs Outgoing_mins_per_month')
plt.xlabel('Device')
plt.ylabel('outgoing_mins_per_month')
plt.show()
s=['device','outgoing_sms_per_month']
r=a[s]
t=r.groupby('device').sum().reset_index().sort_values('outgoing_sms_per_month')
plt.plot(t['device'],t['outgoing_sms_per_month'])
plt.title('Device vs Outgoing_sms_per_month')
plt.xlabel('Device')
plt.ylabel('outgoing_sms_per_month')
plt.show()