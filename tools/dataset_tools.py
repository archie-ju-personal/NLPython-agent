import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid GUI issues
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
import io
import sys
from typing import Dict, Any, List, Optional
import traceback
import ast
import re

warnings.filterwarnings('ignore')

class DatasetTools:
    def __init__(self):
        self.current_dataset = None
        self.dataset_info = {}
        self.execution_history = []
        
    def load_iris_dataset(self) -> Dict[str, Any]:
        """Load the Iris dataset and return basic information."""
        try:
            iris = load_iris()
            self.current_dataset = pd.DataFrame(iris.data, columns=iris.feature_names)
            self.current_dataset['target'] = iris.target
            self.current_dataset['species'] = [iris.target_names[i] for i in iris.target]
            
            # Create JSON-safe dataset info
            dtypes_dict = {}
            for col, dtype in self.current_dataset.dtypes.items():
                dtypes_dict[str(col)] = str(dtype)
            
            self.dataset_info = {
                'shape': self.current_dataset.shape,
                'columns': [str(col) for col in self.current_dataset.columns],
                'dtypes': dtypes_dict,
                'missing_values': {str(k): int(v) for k, v in self.current_dataset.isnull().sum().items()},
                'numeric_columns': [str(col) for col in self.current_dataset.select_dtypes(include=[np.number]).columns],
                'categorical_columns': [str(col) for col in self.current_dataset.select_dtypes(include=['object']).columns]
            }
            
            return {
                'success': True,
                'message': f"Loaded Iris dataset with {self.current_dataset.shape[0]} rows and {self.current_dataset.shape[1]} columns",
                'info': self.dataset_info
            }
        except Exception as e:
            return {'success': False, 'message': f"Error loading dataset: {str(e)}"}
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about the current dataset."""
        if self.current_dataset is None:
            return {'success': False, 'message': "No dataset loaded"}
        
        # Convert dtypes to strings to avoid JSON serialization issues
        dtypes_dict = {}
        for col, dtype in self.current_dataset.dtypes.items():
            dtypes_dict[str(col)] = str(dtype)
        
        # Convert describe to a more JSON-friendly format
        describe_dict = {}
        if not self.current_dataset.empty:
            describe = self.current_dataset.describe()
            for col in describe.columns:
                describe_dict[str(col)] = {
                    str(idx): float(val) if not pd.isna(val) else None 
                    for idx, val in describe[col].items()
                }
        
        info = {
            'shape': self.current_dataset.shape,
            'columns': [str(col) for col in self.current_dataset.columns],
            'dtypes': dtypes_dict,
            'missing_values': {str(k): int(v) for k, v in self.current_dataset.isnull().sum().items()},
            'head': self.current_dataset.head().to_dict('records'),
            'describe': describe_dict
        }
        
        return {'success': True, 'info': info}
    
    def execute_python_code(self, code: str) -> Dict[str, Any]:
        """Safely execute Python code with the current dataset."""
        if self.current_dataset is None:
            return {'success': False, 'message': "No dataset loaded. Please load a dataset first."}
        
        # Security check - only allow safe operations
        dangerous_keywords = [
            'import', 'exec', 'eval', 'open', 'file', 'system', 'subprocess',
            'os.', 'sys.', '__import__', 'globals', 'locals', 'del'
        ]
        
        code_lower = code.lower()
        for keyword in dangerous_keywords:
            if keyword in code_lower:
                return {
                    'success': False, 
                    'message': f"Security: Operation '{keyword}' is not allowed for safety reasons."
                }
        
        try:
            # Create a safe execution environment
            local_vars = {
                'df': self.current_dataset.copy(),
                'pd': pd,
                'np': np,
                'plt': plt,
                'sns': sns,
                'px': px,
                'go': go,
                'print': print,
                'len': len,
                'range': range,
                'list': list,
                'dict': dict,
                'str': str,
                'int': int,
                'float': float,
                'train_test_split': train_test_split,
                'StandardScaler': StandardScaler,
                'LinearRegression': LinearRegression,
                'LogisticRegression': LogisticRegression,
                'RandomForestClassifier': RandomForestClassifier,
                'RandomForestRegressor': RandomForestRegressor,
                'accuracy_score': accuracy_score,
                'classification_report': classification_report,
                'confusion_matrix': confusion_matrix
            }
            
            # Capture stdout to get print statements
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            
            # Execute the code
            exec(code, {'__builtins__': {}}, local_vars)
            
            # Get the output
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
            
            # Check if df was modified
            if 'df' in local_vars and local_vars['df'] is not None:
                self.current_dataset = local_vars['df']
            
            # Store execution history
            self.execution_history.append({
                'code': code,
                'output': output,
                'timestamp': pd.Timestamp.now()
            })
            
            return {
                'success': True,
                'output': output,
                'dataset_shape': self.current_dataset.shape if self.current_dataset is not None else None
            }
            
        except Exception as e:
            sys.stdout = old_stdout
            return {
                'success': False,
                'message': f"Error executing code: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    def create_visualization(self, viz_type: str, **kwargs) -> Dict[str, Any]:
        """Create common visualizations for the dataset."""
        if self.current_dataset is None:
            return {'success': False, 'message': "No dataset loaded"}
        
        try:
            if viz_type == "correlation_heatmap":
                numeric_cols = self.current_dataset.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) < 2:
                    return {'success': False, 'message': "Need at least 2 numeric columns for correlation heatmap"}
                
                corr_matrix = self.current_dataset[numeric_cols].corr()
                plt.figure(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
                plt.title('Correlation Heatmap')
                plt.tight_layout()
                
                # Save plot to bytes
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                return {
                    'success': True,
                    'message': "Correlation heatmap created successfully",
                    'plot_data': img_buffer.getvalue()
                }
            
            elif viz_type == "scatter_plot":
                x_col = kwargs.get('x')
                y_col = kwargs.get('y')
                if not x_col or not y_col:
                    return {'success': False, 'message': "Please specify x and y columns for scatter plot"}
                
                plt.figure(figsize=(10, 6))
                plt.scatter(self.current_dataset[x_col], self.current_dataset[y_col])
                plt.xlabel(x_col)
                plt.ylabel(y_col)
                plt.title(f'Scatter Plot: {x_col} vs {y_col}')
                plt.grid(True, alpha=0.3)
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                return {
                    'success': True,
                    'message': f"Scatter plot created: {x_col} vs {y_col}",
                    'plot_data': img_buffer.getvalue()
                }
            
            elif viz_type == "histogram":
                column = kwargs.get('column')
                if not column:
                    return {'success': False, 'message': "Please specify a column for histogram"}
                
                plt.figure(figsize=(10, 6))
                plt.hist(self.current_dataset[column], bins=30, alpha=0.7, edgecolor='black')
                plt.xlabel(column)
                plt.ylabel('Frequency')
                plt.title(f'Histogram of {column}')
                plt.grid(True, alpha=0.3)
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                return {
                    'success': True,
                    'message': f"Histogram created for {column}",
                    'plot_data': img_buffer.getvalue()
                }
            
            else:
                return {'success': False, 'message': f"Unknown visualization type: {viz_type}"}
                
        except Exception as e:
            return {'success': False, 'message': f"Error creating visualization: {str(e)}"}
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the history of executed code."""
        return self.execution_history
    
    def reset_dataset(self) -> Dict[str, Any]:
        """Reset the dataset to its original state."""
        return self.load_iris_dataset()

# Global instance
dataset_tools = DatasetTools() 