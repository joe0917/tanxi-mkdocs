import re
from openpyxl import load_workbook
from openpyxl.styles import Font


def process_excel(file_path):
    # 加载Excel文件
    wb = load_workbook(file_path)
    ws = wb.active

    # 存储当前字号15的单元格的值
    current_size_15_value = None

    # 存储最近匹配的符号值
    last_symbol_values = {
        '■': None,
        '□': None,
        '▲': None,
        '△': None
    }

    # 遍历A列
    for i in range(1, ws.max_row + 1):
        cell = ws.cell(row=i, column=1)

        # 检查字号是否为15
        if cell.font and cell.font.size == 15:
            # 复制到B列
            ws.cell(row=i, column=2).value = cell.value
            current_size_15_value = cell.value

            # 获取下一行的前两个非空字符
            if i + 1 <= ws.max_row:
                next_row_cell = ws.cell(row=i + 1, column=1)
                if next_row_cell.value:
                    # 去除空白字符后取前两个字符
                    cleaned_value = ''.join(str(next_row_cell.value).split())
                    first_two_chars = cleaned_value[:2] if len(cleaned_value) >= 2 else cleaned_value
                    ws.cell(row=i, column=3).value = first_two_chars

            # 重置符号值
            last_symbol_values = {k: None for k in last_symbol_values}

        elif current_size_15_value is not None:
            # 只在找到字号15之后处理
            if cell.value and isinstance(cell.value, str):
                # 定义符号和它们的优先级
                symbols = ['■', '□', '▲', '△']

                for symbol in symbols:
                    # 匹配模式：符号和第一个冒号（全角或半角）之间的内容
                    pattern = re.compile(rf'{re.escape(symbol)}([^:：]+)[:：]')
                    match = pattern.search(cell.value)

                    if match:
                        extracted_text = match.group(1).strip()

                        # 设置B列的值
                        ws.cell(row=i, column=2).value = extracted_text

                        # 设置C列的值
                        if symbol == '■':
                            ws.cell(row=i, column=3).value = current_size_15_value
                        else:
                            # 找到前一个符号的索引
                            prev_symbol_index = symbols.index(symbol) - 1
                            prev_symbol = symbols[prev_symbol_index]
                            ws.cell(row=i, column=3).value = last_symbol_values.get(prev_symbol)

                        # 更新当前符号的值
                        last_symbol_values[symbol] = extracted_text
                        break

    # 保存文件
    output_path = file_path.replace('.xlsx', '_processed.xlsx')
    wb.save(output_path)
    print(f"处理完成，结果已保存到: {output_path}")


# 使用示例
if __name__ == "__main__":
    excel_file = input("请输入Excel文件路径: ")
    process_excel(excel_file)