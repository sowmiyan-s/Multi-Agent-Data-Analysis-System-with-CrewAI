import pandas as pd
import numpy as np
from crewai.tools import tool
from typing import Optional, Dict, Any
from utils.logger import app_logger

class DatasetTools:
    
    @staticmethod
    def _load_df(file_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
        """Helper to load dataframe safely with path fallback."""
        try:
            # Smart path resolution
            if not os.path.exists(file_path):
                alt_path = os.path.join(settings.DATA_DIR, os.path.basename(file_path))
                if os.path.exists(alt_path):
                    app_logger.debug(f"Resolved {file_path} to {alt_path}")
                    file_path = alt_path
            
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path, nrows=nrows)
            elif file_path.endswith(('.xls', '.xlsx')):
                return pd.read_excel(file_path, nrows=nrows)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            app_logger.error(f"Failed to load dataset {file_path}: {e}")
            raise

    @staticmethod
    @tool("Inspect Dataset")
    def inspect_dataset(file_path: str) -> str:
        """
        Returns the structural overview, column types, and first few rows of the dataset.
        Use this to understand what the data looks like.
        """
        try:
            df = DatasetTools._load_df(file_path, nrows=10)
            summary = {
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "shape_sample": df.shape,
                "head": df.head(5).to_dict()
            }
            return f"Dataset Overview for {file_path}:\n{summary}"
        except Exception as e:
            return f"Error inspecting dataset: {str(e)}"

    @staticmethod
    @tool("Data Quality Audit")
    def data_quality_audit(file_path: str) -> str:
        """
        Performs a deep dive into data quality: missing values, duplicates, and cardinality.
        """
        try:
            df = DatasetTools._load_df(file_path)
            stats = {
                "total_rows": len(df),
                "missing_values": df.isnull().sum().to_dict(),
                "duplicate_rows": int(df.duplicated().sum()),
                "unique_counts": df.nunique().to_dict()
            }
            return f"Quality Audit Results:\n{stats}"
        except Exception as e:
            return f"Error auditing data: {str(e)}"

    @staticmethod
    @tool("Statistical Profiling")
    def statistical_profiling(file_path: str) -> str:
        """
        Provides detailed statistics for numeric columns including mean, median, skewness, and kurtosis.
        """
        try:
            df = DatasetTools._load_df(file_path)
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                return "No numeric columns found for statistical profiling."
            
            profile = numeric_df.describe().to_dict()
            # Add skewness
            for col in numeric_df.columns:
                profile[col]['skewness'] = float(numeric_df[col].skew())
            
            return f"Statistical Profile:\n{profile}"
        except Exception as e:
            return f"Error profiling statistics: {str(e)}"

    @staticmethod
    @tool("Identify Correlated Features")
    def identify_correlations(file_path: str, threshold: float = 0.7) -> str:
        """
        Identifies highly correlated features in the dataset.
        Useful for feature selection and understanding relationships.
        """
        try:
            df = DatasetTools._load_df(file_path)
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                return "No numeric columns for correlation analysis."
            
            corr_matrix = numeric_df.corr().abs()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            
            to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
            
            return f"High correlation detected (threshold > {threshold}) in columns: {to_drop}" if to_drop else "No high correlations detected."
        except Exception as e:
            return f"Error calculating correlations: {str(e)}"
