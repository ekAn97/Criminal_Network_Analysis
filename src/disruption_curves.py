import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from  matplotlib.ticker import FuncFormatter

#---- F U N C T I O N S ----

def r_index(df):
    dataframe = pd.DataFrame()
    
    for i in range(2, len(df.columns)):
        dataframe[df.columns[i]] = [1 - (abs(df.iat[0, i] -\
                                             df.iat[j, i]) /\
                                         df.iat[0, i]) for j in range(len(df.index))]
        
    return dataframe
    

#----- M A I N -----

path_load = "Final_Results/Full_Network/directed/Node_removal/strongly/"
path_save = path_load + "Pllots/"
method = {1: "Block", 2: "Cascade"}
n = ["2", "5"]

for key, value in method.items():
    if key == 1:
        for i0 in n:
            file_name = path_load + "Final_" + method[key] + "_" + i0 + ".xlsx"
            xls_f = pd.ExcelFile(file_name, engine = "openpyxl")
            
            for sheet_name in xls_f.sheet_names:
                df = pd.read_excel(file_name, sheet_name = sheet_name)
                if sheet_name != "Components #":
                    iter_df = df["Unnamed: 0"]
                    df = r_index(df)
                    ylabel = r"$\frac{|NLSCC_{0} - NLSCC_{i}|}{NLSCC_{0}}$"
                else:
                    iter_df = df["Unnamed: 0"]
                    df = df.drop(["Unnamed: 0", "Iteration"], axis = 1)
                    ylabel = "Number of strongly connected components"
                
                
                df = df.drop(["In_Katz", "Out_Katz"], axis = 1)
                # Plot variables
                sb.set(style = "whitegrid")
                n_col = len(df.columns)
                plt.figure(figsize = (12, 6))
                
                for col in df.columns:
                    xvals = iter_df.values[:21]
                    yvals = df[col][:21]
                    # Plot
                    sb.lineplot(x = xvals, y = yvals, label = col)
                    if sheet_name != "Components #":
                        plt.xticks(xvals)
                    else:
                        plt.xticks(ticks=np.arange(0, len(xvals), 5),
                               labels=np.arange(0, len(xvals), 5))
                    #ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))
                
                # Visualization
                plt.xlabel("Time-Step", fontdict = {"fontweight": "bold"})
                plt.ylabel(ylabel)
                #plt.title(sheet_name, fontdict = {"fontsize": 14,
                #"fontweight": "bold", "fontstyle": "italic"})
                plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), 
                           fancybox=True, shadow=True, ncol=5)
                plt.subplots_adjust(bottom=0.2)
    
                # Storing plot as a jpg image
                plt.tight_layout()
                plt.savefig(path_save + "{}_{}_{}.jpg".format(sheet_name, i0, 
                                                              method[key]), 
                            format = "jpg", dpi=300)
                 
                
    elif key == 2:
        file_name = path_load + "Final_" + method[key] + ".xlsx"
        xls_f = pd.ExcelFile(file_name, engine = "openpyxl")
        
        for sheet_name in xls_f.sheet_names:
            df = pd.read_excel(file_name, sheet_name = sheet_name)
            if sheet_name != "Components #":
                iter_df = df["Unnamed: 0"]
                df = r_index(df)
                ylabel = r"$\frac{|NLSCC_{0} - NLSCC_{i}|}{NLSCC_{0}}$"
            else:
                iter_df = df["Unnamed: 0"]
                df = df.drop(["Unnamed: 0", "Iteration"], axis = 1)
                ylabel = "Number of strongly connected components"
            
            df = df.drop(["In_Katz", "Out_Katz"], axis = 1)
            # Plot
            sb.set(style = "whitegrid")
            n_col = len(df.columns)
            plt.figure(figsize = (12, 6))
                
            for col in df.columns:
                xvals = iter_df.values[:21]
                yvals = df[col][:21]
                #Plot
                sb.lineplot(x = xvals, y = yvals, label = col)
                if sheet_name != "Components #":
                        plt.xticks(xvals)
                else:
                    plt.xticks(ticks=np.arange(0, len(xvals), 5),
                               labels=np.arange(0, len(xvals), 5))
                #ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))
            
            # Visualization
            plt.xlabel("Time-Step", fontdict = {"fontweight": "bold"})
            plt.ylabel(ylabel)
            #plt.title(sheet_name, fontdict = {"fontsize": 14, 
             #                               "fontweight": "bold", 
              #                              "fontstyle": "italic"})
            plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), 
                       fancybox=True, shadow=True, ncol=5)
            plt.subplots_adjust(bottom=0.2)
    
            # Storing plot as a jpg image
            plt.tight_layout()
            plt.savefig(path_save + "{}_{}.jpg".format(sheet_name, method[key]), 
                        format = "jpg", dpi=300)