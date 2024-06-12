import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from jinja2 import Template


engine = create_engine('sqlite:///test.db')
conn = engine.connect()


query = 'SELECT * FROM sales'
df = pd.read_sql(query, conn)
conn.close()


grouped = df.groupby(['date', 'product']).sum().reset_index()
for product in grouped['product'].unique():
    product_data = grouped[grouped['product'] == product]
    plt.plot(product_data['date'], product_data['quantity'], label=product)

plt.xlabel('Date')
plt.ylabel('Quantity Sold')
plt.title('Sales Report')
plt.legend()
plt.savefig('sales_report.png')
plt.close()


template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>Sales Report</title>
</head>
<body>
    <h1>Sales Report</h1>
    <img src="cid:sales_report.png" alt="Sales Report">
    <table border="1">
        <tr>
            <th>Date</th>
            <th>Product</th>
            <th>Quantity</th>
            <th>Price</th>
        </tr>
        {% for row in data %}
        <tr>
            <td>{{ row['date'] }}</td>
            <td>{{ row['product'] }}</td>
            <td>{{ row['quantity'] }}</td>
            <td>{{ row['price'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
""")
html_content = template.render(data=df.to_dict(orient='records'))


with open('report.html', 'w') as f:
    f.write(html_content)


sender_email = 'sender@gmail.com'
receiver_email = 'receiver@gmail.com'
subject = 'Daily Sales Report'
body = 'Please find attached the daily sales report.'


msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

with open('report.html', 'r') as f:
    html_content = f.read()
msg.attach(MIMEText(html_content, 'html'))

with open('sales_report.png', 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<sales_report.png>')
    msg.attach(img)


