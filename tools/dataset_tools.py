import pandas as pd
import numpy as np
from crewai.tools import tool

class DatasetTools:
    @tool("Read Dataset Head")
    def read_dataset_head(file_path: str):
        """Reads the first 10 rows of the dataset to understand its structure."""
        try:
            df = pd.read_csv(file_path, nrows=100)
            if len(df.columns) > 20:
                cols = list(df.columns[:10]) + ["..."] + list(df.columns[-10:])
                df = df[cols]
            return df.head(10).to_markdown(index=False)
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @tool("Get Dataset Info")
    def get_dataset_info(file_path: str):
        """Returns summarized information about the dataset. Production-safe for large files."""
        try:
            # Get columns and total rows without loading everything
            df_cols = pd.read_csv(file_path, nrows=0)
            row_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore')) - 1
            
            # Read a sample for quality analysis
            df_sample = pd.read_csv(file_path, nrows=500)
            
            info = [f"Total Rows: {row_count}", f"Total Columns: {len(df_cols.columns)}"]
            cols_to_show = df_cols.columns[:15]
            info.append("\nSample Analysis (first 15 cols):")
            for col in cols_to_show:
                null_count = df_sample[col].isnull().sum()
                info.append(f"- {col}: {df_sample[col].dtype} | Sample Nulls: {null_count}")
            
            if len(df_cols.columns) > 15:
                info.append(f"... +{len(df_cols.columns) - 15} more.")
            return "\n".join(info)
        except Exception as e:
            return f"Error analyzing metadata: {str(e)}"

    @tool("Get Statistical Summary")
    def get_statistical_summary(file_path: str):
        """Returns a statistical summary of the numeric columns."""
        try:
            df = pd.read_csv(file_path)
            numeric_df = df.select_dtypes(include=['number'])
            if numeric_df.empty: return "No numeric columns found."
            return numeric_df[numeric_df.columns[:15]].describe().to_markdown()
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    @tool("Get Correlation Matrix")
    def get_correlation_matrix(file_path: str):
        """Calculates the correlation matrix for numeric columns."""
        try:
            df = pd.read_csv(file_path)
            numeric_df = df.select_dtypes(include=['number'])
            cols_to_corr = [col for col in numeric_df.columns if numeric_df[col].nunique() > 1][:10]
            if not cols_to_corr: return "Not enough variation for correlation."
            return numeric_df[cols_to_corr].corr().to_markdown()
        except Exception as e:
            return f"Error calculating correlation: {str(e)}"

    @tool("Detect Outliers")
    def detect_outliers(file_path: str):
        """Identifies columns with potential outliers using the IQR method."""
        try:
            df = pd.read_csv(file_path)
            numeric_df = df.select_dtypes(include=['number'])
            if numeric_df.empty: return "No numeric columns."
            results = []
            for col in numeric_df.columns[:10]:
                Q1, Q3 = numeric_df[col].quantile(0.25), numeric_df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = numeric_df[(numeric_df[col] < Q1 - 1.5 * IQR) | (numeric_df[col] > Q3 + 1.5 * IQR)]
                if not outliers.empty:
                    results.append(f"- {col}: {len(outliers)} outliers (Min: {numeric_df[col].min()}, Max: {numeric_df[col].max()})")
            return "\n".join(results) if results else "No significant outliers detected."
        except Exception as e:
            return f"Error detecting outliers: {str(e)}"

    @tool("Get Data Quality Report")
    def get_data_quality_report(file_path: str):
        """Generates a detailed quality report including duplicates and skewness."""
        try:
            df = pd.read_csv(file_path)
            report = [f"Duplicates: {df.duplicated().sum()}"]
            numeric_df = df.select_dtypes(include=['number'])
            report.append("\nSkewness:")
            for col in numeric_df.columns[:10]:
                report.append(f"- {col}: {numeric_df[col].skew():.2f}")
            return "\n".join(report)
        except Exception as e:
            return f"Error generating quality report: {str(e)}"
