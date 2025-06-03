import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

def analyze_csv(file_path: str, report_format='txt'):
    """
    Analisa um arquivo CSV e gera um relatório com estatísticas e gráficos
    """
    
    if not os.path.exists(file_path):
        print(f"Arquivo '{file_path}' não encontrado. Verifique o caminho e tente novamente.")
        return

    print("Lendo o arquivo...")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return
    
    output_dir = "analysis_results"
    os.makedirs(output_dir, exist_ok=True)

    print("Executando análise estatística...")
    report_content = generate_report_content(df)

    print("Salvando o relatório...")
    save_report(report_content, output_dir, report_format)

    print("Gerando gráficos...")
    generate_plots(df, output_dir)

    print(f"\nAnálise concluída com sucesso. Os resultados foram salvos na pasta '{output_dir}'.")

def generate_report_content(df: pd.DataFrame):
    """Gera o conteúdo do relatório com análises estatísticas"""
    
    report = []

    report.append("=== RESUMO DO DATASET ===")
    report.append(f"Número de linhas: {len(df)}")
    report.append(f"Número de colunas: {len(df.columns)}\n")

    report.append("=== ESTATÍSTICAS POR COLUNA ===")
    
    for column in df.columns:
        report.append(f"\nColuna: {column}")
        report.append(f"Tipo de dados: {df[column].dtype}")
        
        if pd.api.types.is_numeric_dtype(df[column]):
            report.append(f"Valores nulos: {df[column].isna().sum()} ({df[column].isna().mean()*100:.2f}%)")
            report.append(f"Média: {df[column].mean():.2f}")
            report.append(f"Mediana: {df[column].median():.2f}")
            report.append(f"Moda: {stats.mode(df[column], keepdims=True).mode[0]:.2f}")
            report.append(f"Desvio padrão: {df[column].std():.2f}")
            report.append(f"Mínimo: {df[column].min():.2f}")
            report.append(f"Máximo: {df[column].max():.2f}")
            report.append(f"Q1 (25%): {df[column].quantile(0.25):.2f}")
            report.append(f"Q3 (75%): {df[column].quantile(0.75):.2f}")
        else:
            report.append(f"Valores nulos: {df[column].isna().sum()} ({df[column].isna().mean()*100:.2f}%)")
            report.append(f"Valores únicos: {df[column].nunique()}")
            report.append("Valores mais frequentes:")
            top_values = df[column].value_counts().head(5)
            for value, count in top_values.items():
                report.append(f"  {value}: {count} ({count/len(df)*100:.2f}%)")
    
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 1:
        report.append("\n=== CORRELAÇÕES ENTRE VARIÁVEIS NUMÉRICAS ===")
        corr_matrix = df[numeric_cols].corr()
        report.append(corr_matrix.to_string())

    return "\n".join(report)

def generate_plots(df: pd.DataFrame, output_dir: str):
    """Gera visualizações dos dados"""
    sns.set(style="whitegrid")

    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        plt.clf()
        sns.histplot(df[col], kde=True)
        plt.title(f'Distribuição de {col}')
        plt.savefig(f"{output_dir}/hist_{col}.png", bbox_inches='tight')

    categorical_cols = df.select_dtypes(exclude=['number']).columns
    for col in categorical_cols:
        if df[col].nunique() < 20:
            plt.clf()
            sns.countplot(y=col, data=df, order=df[col].value_counts().index)
            plt.title(f'Contagem de {col}')
            plt.savefig(f"{output_dir}/bar_{col}.png", bbox_inches='tight')

    if len(numeric_cols) > 1:
        plt.clf()
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
        plt.title('Matriz de Correlação')
        plt.savefig(f"{output_dir}/correlation_matrix.png", bbox_inches='tight')

def save_report(content: str, output_dir: str, format='txt'):
    """Salva o relatório no formato especificado"""
    
    if format == 'html':
        html_content = f"""
        <html>
        <head>
            <title>Relatório de Análise</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #3498db; }}
                pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
                img {{ max-width: 100%; height: auto; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>Relatório de Análise</h1>
            <pre>{content}</pre>
            <h2>Visualizações</h2>
        """
        
        for img_file in os.listdir(output_dir):
            if img_file.endswith('.png'):
                html_content += f'<h3>{img_file.replace(".png", "").replace("_", " ").title()}</h3>\n'
                html_content += f'<img src="{img_file}" alt="{img_file}">\n'
        
        html_content += "</body></html>"
        
        with open(f"{output_dir}/report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    else:
        with open(f"{output_dir}/report.txt", "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    print("Bem-vindo ao analisador de arquivos CSV.")

    file_path = input("Digite o caminho para o seu arquivo CSV: ").strip('"')
    
    report_format = input("Formato do relatório (txt ou html) [padrão: txt]: ").strip().lower()
    if report_format not in ['txt', 'html']:
        print("Formato não reconhecido. O relatório será salvo como 'txt'.")
        report_format = 'txt'

    analyze_csv(file_path, report_format)

    print("\nTudo pronto. Obrigado por usar o analisador!")
