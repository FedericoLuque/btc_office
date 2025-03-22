import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
from odf.opendocument import load

def update_ods_file(json_data, doc, table):
    row = [
        json_data["coordinator"],
        json_data["order_id"],
        json_data["currency"],
        json_data["maker"]["trade_fee_percent"],
        json_data["maker"]["bond_size_sats"],
        json_data["maker"]["is_buyer"],
        json_data["maker"]["sent_fiat"],
        json_data["maker"]["received_sats"],
        json_data["taker"]["trade_fee_percent"],
        json_data["taker"]["bond_size_sats"],
        json_data["taker"]["is_buyer"],
        json_data["taker"]["sent_sats"],
        json_data["taker"]["received_fiat"],
        json_data["platform"]["contract_exchange_rate"],
        json_data["platform"]["contract_timestamp"],
        json_data["platform"]["contract_total_time"],
        json_data["platform"]["routing_budget_sats"],
        json_data["platform"]["trade_revenue_sats"]
    ]
    
    # Si es la primera fila, añade los encabezados
    if len(table.getElementsByType(TableRow)) == 0:
        headers = ["coordinator", "order_id", "currency", "maker_trade_fee_percent", "maker_bond_size_sats", "maker_is_buyer", "maker_sent_fiat", "maker_received_sats", "taker_trade_fee_percent", "taker_bond_size_sats", "taker_is_buyer", "taker_sent_sats", "taker_received_fiat", "platform_contract_exchange_rate", "platform_contract_timestamp", "platform_contract_total_time", "platform_routing_budget_sats", "platform_trade_revenue_sats"]
        header_row = TableRow()
        for header in headers:
            cell = TableCell()
            cell.addElement(P(text=header))  # Añadir texto dentro de la celda usando P
            header_row.addElement(cell)
        table.addElement(header_row)
    
    # Agregar la fila de datos
    data_row = TableRow()
    for cell_data in row:
        cell = TableCell()
        cell.addElement(P(text=str(cell_data)))  # Añadir texto dentro de la celda usando P
        data_row.addElement(cell)
    table.addElement(data_row)
    print("Datos insertados correctamente en el archivo ODS.")

def confirm_and_delete(file):
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno("Confirmar eliminación", f"¿Deseas eliminar el archivo {file} después de procesarlo?")
    
    if result:
        os.remove(file)
        print(f"Archivo {file} eliminado.")
    else:
        print(f"Archivo {file} no eliminado.")

def show_no_files_notification():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Sin archivos JSON", "No se han encontrado archivos .json para procesar.")



def create_or_open_ods(file_path):
    if os.path.exists(file_path):
        # Si el archivo ODS ya existe, ábrelo
        doc = load(file_path)
        table = doc.spreadsheet.getElementsByType(Table)[0]
    else:
        # Si el archivo no existe, crea uno nuevo
        doc = OpenDocumentSpreadsheet()
        table = Table(name="Datos de Trade")
        doc.spreadsheet.addElement(table)
    return doc, table  # Importante devolver doc y table para trabajar con ellos fuera de la función

def choose_format():
    root = tk.Tk()
    root.withdraw()
    return "ods"  # Siempre devuelve "ods" ya que solo trabajamos con este formato

# Procesar múltiples archivos trade.json en la carpeta
json_files_found = False
output_file = "resultados_trade.ods"  # Ruta del archivo ODS
doc, table = create_or_open_ods(output_file)  # Cargar o crear el archivo ODS

for file in os.listdir():
    if file.startswith("trade") and file.endswith(".json"):
        json_files_found = True
        try:
            with open(file, 'r') as f:
                data = json.load(f)

                # Actualizar el archivo ODS
                update_ods_file(data, doc, table)
                doc.save(output_file)  # Guardar el archivo ODS después de cada actualización
                print("Archivo ODS guardado como 'resultados_trade.ods'.")
                
                confirm_and_delete(file)
        except Exception as e:
            print(f"Error procesando {file}: {e}")

# Si no se encontraron archivos .json, mostrar notificación
if not json_files_found:
    show_no_files_notification()
