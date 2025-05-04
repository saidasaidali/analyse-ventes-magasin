import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Charger les données
df = pd.read_csv('C:\\Users\\HP\\Desktop\\mes cours\\Brainwave Matrix Solutions\\sales_data_sample.csv')
# Afficher les premières lignes
print("Aperçu des données :")
print(df.head())
# 3. Convertir la date en format datetime (si elle existe)
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
else:
    print("⚠️ La colonne 'Date' n'existe pas dans le fichier.")

# 4. Indicateurs clés
total_sales = df['Total Price'].sum()
total_orders = df['Order ID'].nunique()
total_quantity = df['Quantity'].sum()
unique_customers = df['Customer'].nunique()

print("\n--- Indicateurs Clés ---")
print("Total des ventes :", round(total_sales, 2))
print("Nombre total de commandes :", total_orders)
print("Quantité totale vendue :", total_quantity)
print("Nombre de clients uniques :", unique_customers)

# 5. Visualisation : Ventes par mois
if 'Date' in df.columns:
    df['MonthYear'] = df['Date'].dt.to_period('M')
    monthly_sales = df.groupby('MonthYear')['Total Price'].sum()
    monthly_sales.plot(kind='bar', figsize=(10, 5), title="Ventes par Mois")
    plt.ylabel("Total des ventes")
    plt.xlabel("Mois")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
# 6. Produits les plus vendus
top_products = df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).head(10)
top_products.plot(kind='barh', title="Top 10 Produits les plus vendus")
plt.xlabel("Quantité")
plt.tight_layout()
plt.show()

# 7. Ventes par région (si colonne disponible)
if 'Region' in df.columns:
    region_sales = df.groupby('Region')['Total Price'].sum()
    region_sales.plot(kind='pie', autopct='%1.1f%%', title="Répartition des ventes par région")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()
else:
    print("ℹ️ Colonne 'Region' non trouvée dans les données.")

# 8. Meilleurs clients
top_customers = df.groupby('Customer')['Total Price'].sum().sort_values(ascending=False).head(10)
top_customers.plot(kind='barh', title="Top 10 Clients par Total des ventes")
plt.xlabel("Total des ventes")
plt.tight_layout()
plt.show()
print(df.head())



# Exporter les résultats dans un fichier Excel
with pd.ExcelWriter('rapport_ventes.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Données brutes', index=False)

    # Créer un DataFrame avec les KPI
    kpi_df = pd.DataFrame({
        'Indicateur': ['Total des ventes', 'Nombre de commandes', 'Quantité vendue', 'Clients uniques'],
        'Valeur': [round(total_sales, 2), total_orders, total_quantity, unique_customers]
    })
    kpi_df.to_excel(writer, sheet_name='KPI', index=False)

    # Tu peux aussi exporter les Top clients et produits
    top_products.to_frame(name='Quantité vendue').to_excel(writer, sheet_name='Top Produits')
    top_customers.to_frame(name='Total des ventes').to_excel(writer, sheet_name='Top Clients')


# Sauvegarde les graphiques en images
monthly_sales.plot(kind='bar', title='Ventes par Mois')
plt.tight_layout()
plt.savefig('graph_ventes_par_mois.png')
plt.close()

top_products.plot(kind='barh', title='Top Produits')
plt.tight_layout()
plt.savefig('graph_top_produits.png')
plt.close()



from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="Rapport d'Analyse des Ventes", ln=True, align='C')

# Ajouter les KPI
pdf.set_font("Arial", size=12)
pdf.ln(10)
pdf.cell(200, 10, txt=f"Total des ventes : {round(total_sales, 2)}", ln=True)
pdf.cell(200, 10, txt=f"Nombre total de commandes : {total_orders}", ln=True)
pdf.cell(200, 10, txt=f"Quantité totale vendue : {total_quantity}", ln=True)
pdf.cell(200, 10, txt=f"Nombre de clients uniques : {unique_customers}", ln=True)

# Ajouter les graphiques
pdf.ln(10)
pdf.image("graph_ventes_par_mois.png", w=180)
pdf.ln(10)
pdf.image("graph_top_produits.png", w=180)

# Enregistrer
pdf.output("rapport_ventes.pdf")





