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

    # 编号计数器
    counters = {
        '5': 1,  # 字号15的编号
        '6': 1,  # ■符号的编号
        '7': 1,  # □符号的编号
        '8': 1,  # ▲符号的编号
        '9': 1,  # △符号的编号
        '4': 1  # C列独立编号
    }

    # 存储所有B列值和对应编号
    b_values_mapping = {}

    # 存储所有C列值和对应编号（用于4开头编号）
    c_values_mapping = {}

    # 遍历A列
    for i in range(1, ws.max_row + 1):
        cell = ws.cell(row=i, column=1)

        # 检查字号是否为15
        if cell.font and cell.font.size == 15:
            # 复制到B列
            b_value = cell.value
            ws.cell(row=i, column=2).value = b_value
            current_size_15_value = b_value

            # 生成B列编号(5开头)
            b_number = f"5{str(counters['5']).zfill(4)}"
            ws.cell(row=i, column=4).value = b_number
            counters['5'] += 1

            # 记录B列值和编号映射
            b_values_mapping[b_value] = b_number

            # 获取下一行的前两个非空字符
            if i + 1 <= ws.max_row:
                next_row_cell = ws.cell(row=i + 1, column=1)
                if next_row_cell.value:
                    # 去除空白字符后取前两个字符
                    cleaned_value = ''.join(str(next_row_cell.value).split())
                    first_two_chars = cleaned_value[:2] if len(cleaned_value) >= 2 else cleaned_value
                    ws.cell(row=i, column=3).value = first_two_chars

                    # 处理C列编号
                    if first_two_chars in b_values_mapping:
                        # 如果C列值在B列已出现，复制B列编号
                        ws.cell(row=i, column=5).value = b_values_mapping[first_two_chars]
                    else:
                        # 否则检查是否已有4开头的编号
                        if first_two_chars in c_values_mapping:
                            ws.cell(row=i, column=5).value = c_values_mapping[first_two_chars]
                        else:
                            # 生成新的4开头编号
                            c_number = f"4{str(counters['4']).zfill(4)}"
                            ws.cell(row=i, column=5).value = c_number
                            c_values_mapping[first_two_chars] = c_number
                            counters['4'] += 1

            # 重置符号值
            last_symbol_values = {k: None for k in last_symbol_values}

        elif current_size_15_value is not None:
            # 只在找到字号15之后处理
            if cell.value and isinstance(cell.value, str):
                # 定义符号和它们的优先级
                symbols = ['■', '□', '▲', '△']
                symbol_found = None

                for symbol in symbols:
                    # 匹配模式：符号和第一个冒号（全角或半角）之间的内容
                    pattern = re.compile(rf'{re.escape(symbol)}([^:：]+)[:：]')
                    match = pattern.search(cell.value)

                    if match:
                        symbol_found = symbol
                        extracted_text = match.group(1).strip()

                        # 设置B列的值
                        ws.cell(row=i, column=2).value = extracted_text

                        # 设置B列编号
                        if symbol == '■':
                            prefix = '6'
                        elif symbol == '□':
                            prefix = '7'
                        elif symbol == '▲':
                            prefix = '8'
                        elif symbol == '△':
                            prefix = '9'

                        b_number = f"{prefix}{str(counters[prefix]).zfill(4)}"
                        ws.cell(row=i, column=4).value = b_number
                        counters[prefix] += 1
                        b_values_mapping[extracted_text] = b_number

                        # 设置C列的值
                        if symbol == '■':
                            c_value = current_size_15_value
                        else:
                            # 找到前一个符号的索引
                            prev_symbol_index = symbols.index(symbol) - 1
                            prev_symbol = symbols[prev_symbol_index]
                            c_value = last_symbol_values.get(prev_symbol)

                        ws.cell(row=i, column=3).value = c_value

                        # 处理C列编号
                        if c_value in b_values_mapping:
                            # 如果C列值在B列已出现，复制B列编号
                            ws.cell(row=i, column=5).value = b_values_mapping[c_value]
                        else:
                            # 检查是否已有4开头的编号
                            if c_value in c_values_mapping:
                                ws.cell(row=i, column=5).value = c_values_mapping[c_value]
                            else:
                                # 生成新的4开头编号
                                c_number = f"4{str(counters['4']).zfill(4)}"
                                ws.cell(row=i, column=5).value = c_number
                                c_values_mapping[c_value] = c_number
                                counters['4'] += 1

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