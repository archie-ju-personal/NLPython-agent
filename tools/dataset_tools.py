import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid GUI issues
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels
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
            
            # Create minimal dataset info to reduce token usage
            self.dataset_info = {
                'shape': self.current_dataset.shape,
                'columns': [str(col) for col in self.current_dataset.columns],
                'numeric_columns': [str(col) for col in self.current_dataset.select_dtypes(include=[np.number]).columns],
                'categorical_columns': [str(col) for col in self.current_dataset.select_dtypes(include=['object']).columns]
            }
            
            return {
                'success': True,
                'message': f"Loaded Iris dataset: {self.current_dataset.shape[0]} rows, {self.current_dataset.shape[1]} columns",
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
        
        # Get only essential statistics to reduce token usage
        if not self.current_dataset.empty:
            numeric_cols = self.current_dataset.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Get only basic stats for numeric columns
                basic_stats = self.current_dataset[numeric_cols].describe()
                stats_dict = {}
                for col in basic_stats.columns:
                    stats_dict[str(col)] = {
                        'count': float(basic_stats[col]['count']),
                        'mean': float(basic_stats[col]['mean']),
                        'std': float(basic_stats[col]['std']),
                        'min': float(basic_stats[col]['min']),
                        'max': float(basic_stats[col]['max'])
                    }
            else:
                stats_dict = {}
        else:
            stats_dict = {}
        
        # Return optimized info with minimal token usage
        info = {
            'shape': self.current_dataset.shape,
            'columns': [str(col) for col in self.current_dataset.columns],
            'dtypes': dtypes_dict,
            'missing_values': {str(k): int(v) for k, v in self.current_dataset.isnull().sum().items()},
            'basic_stats': stats_dict
        }
        
        return {'success': True, 'info': info}
    
    def execute_python_code(self, code: str) -> Dict[str, Any]:
        """Safely execute Python code with the current dataset."""
        if self.current_dataset is None:
            return {'success': False, 'message': "No dataset loaded. Please load a dataset first."}
        
        # Security check - only allow safe operations
        dangerous_keywords = [
            'exec', 'eval', 'open', 'file', 'system', 'subprocess',
            'globals', 'locals'
        ]
        
        # Check for dangerous keywords with word boundaries
        import re
        code_lower = code.lower()
        
        # Check for dangerous keywords as complete words
        for keyword in dangerous_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', code_lower):
                return {
                    'success': False, 
                    'message': f"Security: Operation '{keyword}' is not allowed for safety reasons."
                }
        
        # Special checks for module imports (os., sys.)
        if re.search(r'\bos\.', code_lower):
            return {
                'success': False, 
                'message': "Security: Operation 'os.' is not allowed for safety reasons."
            }
        
        if re.search(r'\bsys\.', code_lower):
            return {
                'success': False, 
                'message': "Security: Operation 'sys.' is not allowed for safety reasons."
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
                'sklearn': sklearn,
                'train_test_split': train_test_split,
                'StandardScaler': StandardScaler,
                'LinearRegression': LinearRegression,
                'LogisticRegression': LogisticRegression,
                'RandomForestClassifier': RandomForestClassifier,
                'RandomForestRegressor': RandomForestRegressor,
                'accuracy_score': accuracy_score,
                'classification_report': classification_report,
                'confusion_matrix': confusion_matrix,
                'sm': sm,
                'smf': smf,
                'statsmodels': statsmodels
            }
            
            # Capture stdout to get print statements
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            
            # Preprocess the code to handle escaped newlines
            processed_code = code.replace('\\n', '\n')
            
            # Execute the code with import support
            exec(processed_code, {'__builtins__': {'__import__': __import__}}, local_vars)
            
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
    
    def create_visualization(self, code: str) -> Dict[str, Any]:
        """Execute arbitrary Python code to create a visualization and return the plot as PNG bytes."""
        if self.current_dataset is None:
            return {'success': False, 'message': "No dataset loaded"}
        try:
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
                'sklearn': sklearn,
                'train_test_split': train_test_split,
                'StandardScaler': StandardScaler,
                'LinearRegression': LinearRegression,
                'LogisticRegression': LogisticRegression,
                'RandomForestClassifier': RandomForestClassifier,
                'RandomForestRegressor': RandomForestRegressor,
                'accuracy_score': accuracy_score,
                'classification_report': classification_report,
                'confusion_matrix': confusion_matrix,
                'sm': sm,
                'smf': smf,
                'statsmodels': statsmodels
            }
            # Prepare to capture stdout and the plot
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            plt.clf()
            plt.close('all')
            # Preprocess the code to handle escaped newlines
            processed_code = code.replace('\\n', '\n')
            
            # Execute the visualization code with import support
            exec(processed_code, {'__builtins__': {'__import__': __import__}}, local_vars)
            # Save the current figure to a buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            
            # Also save to file for viewing (LangGraph Studio enhancement)
            import os
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"visualization_{timestamp}.png"
            filepath = os.path.join("static", "visualizations", filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save to file
            plt.savefig(filepath, format='png', dpi=300, bbox_inches='tight')
            plt.close('all')
            
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
            # Optionally update df if modified
            if 'df' in local_vars and local_vars['df'] is not None:
                self.current_dataset = local_vars['df']
            
            abs_filepath = os.path.abspath(filepath)
            self.execution_history.append({
                'code': code,
                'output': output,
                'timestamp': pd.Timestamp.now(),
                'visualization_file': abs_filepath
            })
            
            # Return optimized response with minimal token usage
            return {
                'success': True,
                'message': f"Visualization created successfully! Saved to: {abs_filepath}",
                'file_path': abs_filepath,
                'output': output
            }
        except Exception as e:
            sys.stdout = old_stdout
            return {
                'success': False,
                'message': f"Error creating visualization: {str(e)}",
                'traceback': traceback.format_exc()
            }
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the history of executed code."""
        return self.execution_history
    
    def reset_dataset(self) -> Dict[str, Any]:
        """Reset the dataset to its original state."""
        return self.load_iris_dataset()

# Global instance
dataset_tools = DatasetTools() 