import streamlit as st
import pandas as pd

from edbo.plus.optimizer_botorch import EDBOplus

def create_input_fields(num_variables):
    variables_dict = {}
    for i in range(num_variables):
        variable_name = st.text_input(f"Variable {i + 1} name:")
        variable_values = st.text_input(f"Variable {i + 1} values (comma-separated):")
        values_list = [value.strip() for value in variable_values.split(',')]
        
        # Convert numeric values to floats
        converted_values = []
        for value in values_list:
            try:
                converted_values.append(float(value))
            except ValueError:
                converted_values.append(value)

        variables_dict[variable_name] = converted_values

    return variables_dict

def upload_file():
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    return {}


def create_scope(variables_list):
    df = EDBOplus().generate_reaction_scope(
        components=variables_list, 
        filename='my_optimization.csv',
        check_overwrite=False)
    
    return df


def optimize_reaction(dataframe, objective_name, objective_maxmin, batch_size):
    if isinstance(objective_name, str):
        objective_name = objective_name.split(',')

    df = EDBOplus().run(
            data_frame= dataframe,
            filename='2024-01-17T12-22_export.csv',  # Previously generated scope.
            objectives= objective_name,  # Objectives to be optimized.
            objective_mode= objective_maxmin.split(','),  # Maximize yield and ee but minimize side_product.
            batch= batch_size,  # Number of experiments in parallel that we want to perform in this round.
            columns_features='all', # features to be included in the model.
            init_sampling_method='cvtsampling'  # initialization method.
        )
    return df

def main():
    st.title("Bayesian Reaction Optimizer")
    tab1, tab2 = st.tabs(["Create Scope", "Optimize"])

    with tab1:
        st.header("Create Scope")
        num_variables = st.number_input("How many variables do you have?", min_value=1, value=1)
        variables_list = create_input_fields(num_variables)
        if st.button('Create Scope'):
            with st.spinner('Wait for it...'):
                df = create_scope(variables_list= variables_list)
                st.data_editor(df)
                csv_data = df.to_csv(index=False, mode='w', header=list(variables_list.keys())).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name='data.csv',
                    mime='text/csv'
                )
        
    with tab2:
        st.header("Optimize Reaction")
        variables_list = upload_file()
        batch_size = st.number_input(f"Batch Size:", min_value=1, value=1)
        if isinstance(variables_list, pd.DataFrame):
            if st.checkbox('1st time'):
                objective_name = st.text_input(f"Objective Name: (comma-separated):", placeholder= "Yield,Purity")
                objective_maxmin = st.text_input(f"Maximize or Minimize:(comma-separated):", placeholder= "max,min")
            else:
                objective_name = st.multiselect(
                    'Select the objective functions',
                    variables_list.columns)
                objective_maxmin = st.text_input(f"Maximize or Minimize:")
        else:
            st.warning("Please upload a valid file before proceeding.")
            
            
        if st.button('Optimize'):
            with st.spinner('Wait for it...'):
                df = optimize_reaction(dataframe= variables_list, objective_name= objective_name, objective_maxmin= objective_maxmin, batch_size= batch_size)
                # st.data_editor(df, key= 'optimize')
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name='data.csv',
                    mime='text/csv'
                )



if __name__ == "__main__":
    main()
