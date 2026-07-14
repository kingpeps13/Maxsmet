# В конце файла добавьте эту функцию

def export_estimate_to_excel(df, filename, client, object_name, total, total_discount, total_vat, total_base):
    """Экспорт сметы в Excel как в вашем файле"""
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # --- ЛИСТ СМЕТА ---
        export_df = df[['room', 'category', 'work_type', 'work', 'unit', 'quantity', 'price', 'discount', 'total']].copy()
        export_df.columns = ['Помещение', 'Категория', 'Тип работ', 'Услуга', 'ед.изм.', 'Кол-во', 'Цена', 'Скидка', 'Стоимость']
        
        export_df.to_excel(writer, sheet_name='Смета', index=False)
        
        # Настройка ширины колонок
        worksheet = writer.sheets['Смета']
        worksheet.column_dimensions['A'].width = 15  # Помещение
        worksheet.column_dimensions['B'].width = 15  # Категория
        worksheet.column_dimensions['C'].width = 15  # Тип работ
        worksheet.column_dimensions['D'].width = 35  # Услуга
        worksheet.column_dimensions['E'].width = 10  # ед.изм.
        worksheet.column_dimensions['F'].width = 10  # Кол-во
        worksheet.column_dimensions['G'].width = 12  # Цена
        worksheet.column_dimensions['H'].width = 10  # Скидка
        worksheet.column_dimensions['I'].width = 15  # Стоимость
        
        # Добавляем строки с итогами
        last_row = len(export_df) + 3
        from openpyxl.styles import Font
        
        worksheet.cell(row=last_row, column=9, value=f"Базовая стоимость: {total_base:,.2f} руб.")
        worksheet.cell(row=last_row, column=9).font = Font(bold=True)
        worksheet.cell(row=last_row+1, column=9, value=f"Скидка: {total_discount:,.2f} руб.")
        worksheet.cell(row=last_row+1, column=9).font = Font(bold=True)
        worksheet.cell(row=last_row+2, column=9, value=f"НДС: {total_vat:,.2f} руб.")
        worksheet.cell(row=last_row+2, column=9).font = Font(bold=True)
        worksheet.cell(row=last_row+3, column=9, value=f"ИТОГО: {total:,.2f} руб.")
        worksheet.cell(row=last_row+3, column=9).font = Font(bold=True)
        
        # --- СВОД ПО ПОМЕЩЕНИЯМ ---
        room_summary = df.groupby('room').agg({
            'total': 'sum',
            'quantity': 'sum'
        }).reset_index()
        room_summary.columns = ['Помещение', 'Стоимость', 'Кол-во']
        
        room_summary.to_excel(writer, sheet_name='Свод по помещениям', index=False)
        
        ws_room = writer.sheets['Свод по помещениям']
        ws_room.column_dimensions['A'].width = 20
        ws_room.column_dimensions['B'].width = 15
        ws_room.column_dimensions['C'].width = 15
        
        # Итог по своду
        last_room_row = len(room_summary) + 2
        ws_room.cell(row=last_room_row, column=2, value=f"ИТОГО: {total:,.2f} руб.")
        ws_room.cell(row=last_room_row, column=2).font = Font(bold=True)
    
    # Скачивание
    st.download_button(
        label="📥 Скачать Excel",
        data=output.getvalue(),
        file_name=f"{filename}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
