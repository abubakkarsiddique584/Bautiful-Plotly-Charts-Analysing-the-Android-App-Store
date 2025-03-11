import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('apps.csv')

# Convert 'Installs' and 'Price' to numeric
# Remove non-numeric characters from 'Installs'
df['Installs'] = df['Installs'].str.replace(r'[+,]', '', regex=True).astype(float)
# Remove '$' sign and convert 'Price' to float
df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)

# Calculate estimated revenue (Revenue = Price * Installs)
df['Revenue_Estimate'] = df['Price'] * df['Installs']

# Find the top 10 highest-grossing paid apps
top_grossing_apps = df[df['Price'] > 0].nlargest(10, 'Revenue_Estimate')
games_in_top_10 = top_grossing_apps[top_grossing_apps['Category'] == 'GAME']

print("Top 10 Highest Grossing Paid Apps:")
print(top_grossing_apps[['App', 'Category', 'Revenue_Estimate']])
print(f"Number of games among the top 10 highest-grossing paid apps: {len(games_in_top_10)}")
print("Names of games in top 10:", games_in_top_10['App'].tolist())

# Plot: Bar Chart - Most Competitive Categories
category_counts = df['Category'].value_counts()
fig1 = px.bar(category_counts, 
              x=category_counts.index, 
              y=category_counts.values,
              title="Highest Competition (Number of Apps per Category)",
              labels={'x': 'Category', 'y': 'Number of Apps'})
fig1.show()

# Plot: Horizontal Bar Chart - Most Popular Categories (Highest Downloads)
downloads_by_category = df.groupby('Category')['Installs'].sum().sort_values()
fig2 = px.bar(downloads_by_category, 
              x=downloads_by_category.values, 
              y=downloads_by_category.index,
              title="Most Popular Categories (Highest Downloads)",
              labels={'x': 'Total Installs', 'y': 'Category'},
              orientation='h')
fig2.show()

# Scatter Plot - Category Concentration: Downloads vs. Competition
fig3 = px.scatter(df, 
                  x=df['Category'], 
                  y=df['Installs'], 
                  size=df['Installs'], 
                  color=df['Category'],
                  title="Downloads vs. Competition by Category",
                  log_y=True)
fig3.show()

# Extracting Nested Genres
genres_split = df['Genres'].str.split(';', expand=True).stack()
genre_counts = genres_split.value_counts()
print(f"Total unique genres: {len(genre_counts)}")

# Box Plot - Free vs Paid Apps Installations
fig4 = px.box(df, x='Type', y='Installs', 
              title="Lost Downloads for Paid Apps", 
              log_y=True)
fig4.show()

# Box Plot - Revenue by App Category
fig5 = px.box(df[df['Price'] > 0], x='Category', y='Revenue_Estimate', 
              title="Revenue by App Category", 
              log_y=True,
              points='outliers')
fig5.update_layout(xaxis={'categoryorder': 'min ascending'})
fig5.show()

# Median price for paid apps
median_price = df[df['Price'] > 0]['Price'].median()
print(f"Median price for a paid app: ${median_price:.2f}")

# Box Plot - Paid App Pricing Strategies by Category
fig6 = px.box(df[df['Price'] > 0], x='Category', y='Price', 
              title="Paid App Pricing Strategies by Category",
              log_y=True, 
              points="outliers")
fig6.update_layout(xaxis={'categoryorder': 'max descending'})
fig6.show()
