
# uncomment this to install the package needed to use read_excel
#!pip install xlrd
class CombinandoArquivos():
    file_one = 'dados_empresas_2014.xlsx'
    file_two = 'dados_empresas_2015.xlsx'

    def __init__(self):
        self.df_one = pd.read_excel(self.file_one)
        self.df_two = pd.read_excel(self.file_two)
        self.df_three = pd.read_excel(self.file_one, sheet_name='dados_2014_parte1')
        self.df_four = pd.read_excel(self.file_two, sheet_name='dados_2015_parte2')

    def wrangling(self):
        """
        Essa função irá fazer as mudanças necessárias nos dados que estão disponíveis
        na primeira aba das planilhas de 2014 e  2015

        Para executá-la é necessário passar uma dessas bases de dados
        """
        # mudando os nomes das colunas
        columns = ['seção_id','seção_descrição','divisão_id',
                    'divisão_descrição','numero_de_empresas','pessoal_ocupado_total',
                    'pessoal_ocupado_assalariados','segmento']
        self.df_one.columns = columns
        self.df_two.columns = columns
        self.df_three.columns = columns
        self.df_four.columns = columns

        # substituindo o valores que não são números pelo valor -1 e convertendo para integer

        def replacing_and_converting(data, segmento):
            columns = ['numero_de_empresas','pessoal_ocupado_total', 'pessoal_ocupado_assalariados']
            for column in columns:
                for index, value in enumerate(data[column]):
                    if str(value).isdigit():
                        data.loc[index, column] = value
                    else:
                        data.loc[index, column] = -1

                data[column] = data[column].astype('int64')

            data['divisão_id'].astype('object', inplace=True)

            if segmento == 1:
                value = 'Empresas (com 10 ou mais pessoas ocupadas assalariadas e até 8 anos de idade)'
                data['segmento'] = np.where(data['segmento'] == value,
                                           'Até 8 anos de idade', 'Mais de 8 anos de idade')
            elif segmento == 2:
                value = 'Empresas de \nalto crescimento'
                data['segmento'] = np.where(data['segmento'] == value,
                                           'Alto Crescimento', 'Gazela')
                data = data.rename({'segmento':'alto_crescimento'}, axis=1)

            return data

        self.df_one = replacing_and_converting(self.df_one, 1)
        self.df_two = replacing_and_converting(self.df_two, 1)
        self.df_three = replacing_and_converting(self.df_three, 2)
        self.df_four = replacing_and_converting(self.df_four, 2)

        #def melting(data):
         #   values = ['numero_de_empresas','pessoal_ocupado_total','pessoal_ocupado_assalariados']
          #  index = ['seção_id','seção_descrição','divisão_id', 'divisão_descrição']
           # column = ['segmento']
            #data_pivoted = pd.pivot_table(data, index=index, columns=column, values=values).reset_index()
            #return data_pivoted

        #self.df_one = melting(self.df_one)
        #self.df_one.columns = ['seção_id','seção_descrição','divisão_id',
        #                       'divisão_descrição','numero_de_empresas_novas',
        #                       'numero_de_empresas']

        def concatenating_df(dataframe_one, dataframe_two):
            data_new = pd.concat([dataframe_one, dataframe_two], axis=0,
                                 keys=[2014, 2015])
            data_new.reset_index(inplace=True)
            data_new.drop('level_1', axis=1, inplace=True)
            data_new.rename({'level_0': 'year'}, inplace=True)
            return data_new

        self.df_segmento = concatenating_df(self.df_one, self.df_two)
        self.df_altocrescimento = concatenating_df(self.df_three, self.df_four)


    def main(self):
        self.wrangling()
        self.df_altocrescimento.to_csv('autocrescimento.csv', index=False)
        self.df_segmento.to_csv('segmento.csv', index=False)


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    import os

    os.chdir('/home/rafael/Documents/the_hive/the_hive_test/data')
    merging_files = CombinandoArquivos()
    merging_files.main()