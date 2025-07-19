import os
import re
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
import numpy as np

def process_cache_data_interactive(folder_path, output_image_name_table="tabela_resultados_cache.png", output_excel_name="resultados_cache.xlsx", output_image_name_graph="grafico_parametros_cache.png"):
    """
    Processa arquivos de dados de cache em uma pasta, extrai parâmetros selecionados interativamente,
    os organiza em uma tabela (ordenada pelo primeiro parâmetro escolhido), gera uma imagem PNG
    da tabela e um arquivo Excel. Em seguida, permite a seleção de parâmetros e título para gerar um gráfico.
    """

    table_name = "Tabela de Resultados da Simulação de Cache"

    # Mapeamento de todos os parâmetros possíveis encontrados nos TXT para nomes amigáveis
    # Ordem reflete a ordem desejada de apresentação na lista de escolha.
    all_possible_parameters = {
        "Politica de escrita": "1. Política de Escrita",
        "tamanhoLinha": "2. Tamanho da Linha",
        "numeroDeLinhas": "3. Número de Linhas",
        "associatividade": "4. Associatividade",
        "Politica de Substituicao": "5. Política de Substituição",
        "tempoAcerto": "6. Tempo de Acerto",
        "tempoMP": "7. Tempo MP",
        "totalLeitura": "8. Total de Leituras",
        "totalEscrita": "9. Total de Escritas",
        "TotalEnderecos": "10. Total de Endereços",
        "totalEscritaMP": "11. Escritas na MP",
        "totalLeituraMP": "12. Leituras na MP",
        "taxaAcertoLeitura": "13. Taxa de Acerto (Leitura)",
        "taxaAcertoEscrita": "14. Taxa de Acerto (Escrita)",
        "taxaAcertoGlobal": "15. Taxa de Acerto Global (%)", # Nome amigável para a tabela
        "tempoMedioAcesso": "16. Tempo médio de Acesso (ns)",
        "_num_blocos": "17. Número de Blocos" # Prefixo com _ para indicar que é inferido
    }

    # --- Interatividade para escolha de parâmetros para a TABELA ---
    print("--- Configuração da Tabela ---")
    print("Parâmetros disponíveis para a tabela:")
    param_list = list(all_possible_parameters.items()) # Lista de (chave_interna, nome_exibicao)
    for i, (key, display_name) in enumerate(param_list):
        # Remove a numeração temporária para exibição da lista, o input vai usar a numeração gerada
        print(f"{i + 1}. {display_name.split('. ')[1] if '. ' in display_name else display_name}")

    selected_indices_input = input("Digite os NÚMEROS dos parâmetros desejados para a TABELA, separados por vírgula (ex: 1,3,5): ")
    try:
        selected_indices = [int(x.strip()) - 1 for x in selected_indices_input.split(',')]
        
        parameters_to_extract_ordered = []
        for idx in selected_indices:
            if 0 <= idx < len(param_list):
                original_key, original_display_name = param_list[idx]
                # Armazena o nome de exibição limpo, sem o número inicial
                clean_display_name = original_display_name.split('. ')[1] if '. ' in original_display_name else original_display_name
                parameters_to_extract_ordered.append((original_key, clean_display_name))
            else:
                print(f"Aviso: Índice {idx + 1} inválido para a tabela. Ignorando.")

        if not parameters_to_extract_ordered:
            print("Nenhum parâmetro válido selecionado para a tabela. Encerrando.")
            return

    except ValueError:
        print("Entrada inválida. Digite apenas números separados por vírgula.")
        return
    except Exception as e:
        print(f"Ocorreu um erro na seleção de parâmetros para a tabela: {e}")
        return

    # --- Lógica de processamento dos arquivos ---
    data_for_df = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            
            current_row_data = {}
            
            # Tentar extrair o número de blocos do nome do arquivo, se foi selecionado
            num_blocos_display_name = None
            if "_num_blocos" in [item[0] for item in parameters_to_extract_ordered]:
                # Pega o nome de exibição "limpo" para a coluna
                num_blocos_display_name = next(d_name for k, d_name in parameters_to_extract_ordered if k == "_num_blocos")
                num_blocos_match = re.search(r'tamanhoCache(\d+)\.txt', filename)
                if num_blocos_match:
                    current_row_data[num_blocos_display_name] = int(num_blocos_match.group(1))
                else:
                    current_row_data[num_blocos_display_name] = "N/A"

            try:
                with open(filepath, 'r') as f:
                    content = f.read()

                for param_key, display_name in parameters_to_extract_ordered:
                    if param_key == "_num_blocos":
                        continue

                    # Use re.escape para garantir que caracteres especiais no param_key não quebrem a regex
                    match = re.search(fr'{re.escape(param_key)}\s*[:=]\s*([\d.,]+(?:\s*=\s*[\d.]+)?)?', content)
                    if match:
                        value = match.group(1).replace(',', '.')
                        
                        if param_key.startswith("taxaAcerto"):
                            value_parts = value.split('=')
                            if len(value_parts) > 0:
                                try:
                                    value_num = float(value_parts[0].strip())
                                    # Formata sempre com 4 casas para taxas na tabela
                                    current_row_data[display_name] = f"{value_num:.4f}%" 
                                except ValueError:
                                    current_row_data[display_name] = value
                            else:
                                current_row_data[display_name] = value
                        else:
                            try:
                                current_row_data[display_name] = float(value)
                            except ValueError:
                                current_row_data[display_name] = value # Mantém como string se não for número

                    else: # Parâmetro não encontrado no arquivo
                        if display_name not in current_row_data:
                            current_row_data[display_name] = "N/A"
                
                data_for_df.append(current_row_data)

            except Exception as e:
                print(f"Erro ao processar o arquivo {filename}: {e}")
                for param_key, display_name in parameters_to_extract_ordered:
                    if display_name not in current_row_data:
                        current_row_data[display_name] = "N/A"
                data_for_df.append(current_row_data)


    # --- Criação do DataFrame e ordenação das colunas ---
    if data_for_df:
        df = pd.DataFrame(data_for_df)
        
        final_column_order = [display_name for param_key, display_name in parameters_to_extract_ordered]
        
        actual_columns_order = [col for col in final_column_order if col in df.columns]
        df = df[actual_columns_order]
        
        # --- Ordenar a tabela pelo PRIMEIRO parâmetro escolhido, se for numérico ---
        if parameters_to_extract_ordered:
            first_selected_display_name = parameters_to_extract_ordered[0][1] # Pega o nome de exibição do primeiro
            if first_selected_display_name in df.columns:
                # Tenta converter a coluna para numérico antes de ordenar, para lidar com strings como "N/A" ou "%"
                temp_col_for_sort = pd.to_numeric(
                    df[first_selected_display_name].astype(str).str.replace('%', '', regex=False),
                    errors='coerce'
                )
                if pd.api.types.is_numeric_dtype(temp_col_for_sort):
                    df = df.assign(sort_key=temp_col_for_sort).sort_values(by='sort_key').drop(columns='sort_key').reset_index(drop=True)
                else:
                    print(f"Aviso: O primeiro parâmetro '{first_selected_display_name}' não é numérico ou contém dados não-numéricos. A tabela não será ordenada por ele.")
        
        print(f"\n## {table_name}\n")
        print(tabulate(df, headers='keys', tablefmt="pipe"))

        # --- Geração da imagem PNG da TABELA ---
        fig, ax = plt.subplots(figsize=(len(df.columns) * 2.5, len(df) * 0.4 + 1))
        ax.axis('off')
        ax.set_title(table_name, fontsize=16, pad=20)

        mpl_table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(10)
        mpl_table.scale(1.2, 1.2)

        for (i, j), cell in mpl_table._cells.items():
            if i == 0:
                cell.set_facecolor("#D4EDF8")
                cell.set_text_props(weight='bold', color='black')
            else:
                cell.set_facecolor("#E0F2F9")
            cell.set_edgecolor('black')
            cell.set_linewidth(0.5)

        plt.tight_layout()
        plt.savefig(output_image_name_table, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f"\nTabela salva como '{output_image_name_table}'")

        # --- Geração do arquivo Excel ---
        try:
            df_for_excel = df.copy() 
            # Prepara o DataFrame para o Excel, convertendo para numérico onde possível
            for col in df_for_excel.columns:
                # Se a coluna é string e tem '%', remove e tenta converter
                if df_for_excel[col].dtype == 'object' and len(df_for_excel[col]) > 0 and isinstance(df_for_excel[col].iloc[0], str) and '%' in df_for_excel[col].iloc[0]:
                    df_for_excel[col] = df_for_excel[col].str.replace('%', '', regex=False).astype(float)
                
                # Tenta converter para numérico de forma mais robusta, para caso haja "N/A" ou outros não-numéricos
                df_for_excel[col] = pd.to_numeric(df_for_excel[col], errors='coerce')

            df_for_excel.to_excel(output_excel_name, index=False)
            print(f"Dados salvos em '{output_excel_name}' com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar o arquivo Excel '{output_excel_name}': {e}")

        # --- Interatividade para escolha de parâmetros para o GRÁFICO ---
        print("\n--- Configuração do Gráfico ---")
        
        # Lista todas as colunas do DataFrame final para a escolha do gráfico
        print("Colunas disponíveis para o gráfico (serão convertidas para numérico, se possível):")
        for i, col_name in enumerate(df.columns):
            print(f"{i + 1}. {col_name}")

        try:
            x_col_index = int(input("Digite o NÚMERO da coluna para o EIXO X: ")) - 1
            y_col_index = int(input("Digite o NÚMERO da coluna para o EIXO Y: ")) - 1

            if not (0 <= x_col_index < len(df.columns) and 0 <= y_col_index < len(df.columns)):
                print("Seleção de coluna inválida para o gráfico.")
                return

            x_column_name = df.columns[x_col_index]
            y_column_name = df.columns[y_col_index]

            # Converte os dados para numérico, tratando 'N/A' e '%'
            x_data = pd.to_numeric(df[x_column_name].astype(str).str.replace('%', '', regex=False), errors='coerce').dropna()
            y_data = pd.to_numeric(df[y_column_name].astype(str).str.replace('%', '', regex=False), errors='coerce').dropna()

            # Garante que os dados do eixo X e Y correspondam após o dropna
            common_indices = x_data.index.intersection(y_data.index)
            x_data = x_data.loc[common_indices]
            y_data = y_data.loc[common_indices]

            if len(x_data) < 2 or len(y_data) < 2:
                print("Não há dados suficientes (pelo menos 2 pontos numéricos) para gerar o gráfico com as colunas selecionadas.")
                return
            
            # Ordena os dados para o gráfico com base no eixo X
            graph_data = pd.DataFrame({x_column_name: x_data, y_column_name: y_data}).sort_values(by=x_column_name)
            x_data_sorted = graph_data[x_column_name]
            y_data_sorted = graph_data[y_column_name]

            # Pedir títulos do gráfico
            graph_title = input("Digite o título PRINCIPAL para o gráfico (deixe em branco para um título padrão): ")
            if not graph_title:
                graph_title = f'{y_column_name} vs {x_column_name}' # Título padrão se vazio
            
            x_label_input = input(f"Digite o título para o EIXO X (padrão: '{x_column_name}'): ")
            x_label = x_label_input if x_label_input else x_column_name

            y_label_input = input(f"Digite o título para o EIXO Y (padrão: '{y_column_name}'): ")
            y_label = y_label_input if y_label_input else y_column_name

            # --- Geração do Gráfico ---
            fig, ax = plt.subplots(figsize=(10, 6))

            ax.plot(x_data_sorted, y_data_sorted, marker='o', color='blue', linestyle='-')

            # Tentar aplicar escala logarítmica ao eixo X (heurística mais flexível)
            if (x_data_sorted > 0).all() and (x_data_sorted.max() / x_data_sorted.min() > 10):
                 try:
                    ax.set_xscale('log', base=2)
                    ax.set_xticks(x_data_sorted)
                    ax.set_xticklabels([str(int(s)) for s in x_data_sorted if not pd.isna(s)])
                 except Exception as e:
                    print(f"Aviso: Não foi possível aplicar escala logarítmica ao eixo X: {e}. Usando escala linear.")
                    ax.set_xticks(x_data_sorted)
            else:
                ax.set_xticks(x_data_sorted)

            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(graph_title)
            ax.grid(True, which="both", ls="--", linewidth=0.5)

            # Ajuste da escala Y para dar mais espaço acima do maior valor
            y_max_current = y_data_sorted.max()
            y_min_current = y_data_sorted.min()
            
            y_range = y_max_current - y_min_current
            if y_range == 0:
                y_upper_limit = y_max_current + (y_max_current * 0.15 if y_max_current != 0 else 1)
                y_lower_limit = y_min_current - (y_min_current * 0.05 if y_min_current != 0 else 0)
            else:
                y_upper_limit = y_max_current + (y_range * 0.20)
                y_lower_limit = y_min_current - (y_range * 0.05)
            
            if y_lower_limit < 0 and y_min_current >= 0:
                 y_lower_limit = 0 if y_min_current == 0 else y_min_current - (y_range * 0.05 if y_range * 0.05 < y_min_current else y_min_current / 2)
                 if y_lower_limit < 0: y_lower_limit = 0

            ax.set_ylim(bottom=y_lower_limit, top=y_upper_limit)

            # Adicionando os valores de cada ponto - Offset calculado sobre a nova altura do eixo Y
            for x, y in zip(x_data_sorted, y_data_sorted):
                y_text_offset_absolute = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.07
                
                if "Taxa" in y_column_name or "(%)" in y_column_name or "%" in y_column_name:
                    ax.text(x, y + y_text_offset_absolute, f'{y:.4f}%', ha='center', fontsize=8)
                elif "Tempo" in y_column_name or "Acesso" in y_column_name:
                    ax.text(x, y + y_text_offset_absolute, f'{y:.4f}', ha='center', fontsize=8)
                else:
                    ax.text(x, y + y_text_offset_absolute, f'{y}', ha='center', fontsize=8)

            fig.tight_layout()
            fig.savefig(output_image_name_graph, bbox_inches='tight', dpi=300)
            plt.close(fig)
            print(f"Gráfico salvo como '{output_image_name_graph}'")

        except ValueError:
            print("Entrada inválida. Digite apenas números inteiros para as colunas do gráfico.")
        except Exception as e:
            print(f"Erro ao gerar o gráfico: {e}")
            plt.close(plt.gcf())

    else:
        print("Nenhum arquivo .txt encontrado ou nenhum dado extraído para processar.")

# --- Exemplo de uso ---
if __name__ == "__main__":
    folder_with_data = "."
    process_cache_data_interactive(folder_with_data)