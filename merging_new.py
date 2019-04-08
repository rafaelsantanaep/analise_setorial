
# uncomment this to install the package needed to use read_excel
#!pip install xlrd
class CombinandoArquivos():
    file_one = 'dados_empresas_2014.xlsx'
    file_two = 'dados_empresas_2015.xlsx'

    def __init__(self):
        self.df_one = pd.read_excel(self.file_one)
        self.df_two = pd.read_excel(self.file_two)
        self.df_three = pd.read_excel(self.file_one, sheet_name='dados_2014_parte2')
        self.df_four = pd.read_excel(self.file_two, sheet_name='dados_2015_parte2')

    def wrangling(self):
        docstring = """
        Essa módulo irá fazer as mudanças necessárias nos dados que estão disponíveis
        na primeira aba das planilhas de 2014 e  2015.

        Primeiramente, irá colocar o mesmo nome em todas as colunas dos quatro datasets,
        tendo como intuito facilitar o processo de limpeza.

        Depois disso, ela irá substituir os valores faltando por -1, com o intuito,
        de possibilitar a identificação desses valores.

        Posteriormente, cada um dos datasets se tornará mais largo (wide), através
        da utilização da função pivot_table, utilizando como index os identificadores
        do dataset, como coluna as colunas 'segmento' e 'alto crescimento', respectivamente.
        Já em relação aos valores, serão utilizadas todas as colunas numéricas em cada um
        dos quatro datasets.

        Os datasets de cada serão fundidos usando merge. Sobrando assim, dois datasets:
        - Um referente a 2014
        - Outro referente a 2015

        Por fim, esses dois datasets serão combinados, resultando em um dataset com

        688 linhas e 8 colunas.
        """
        print(docstring)
        columns = ['seção_id','seção_descrição','divisão_id',
                    'divisão_descrição','numero_de_empresas','pessoal_ocupado_total',
                    'pessoal_ocupado_assalariados','segmento']
        self.df_one.columns = columns
        self.df_two.columns = columns
        self.df_three.columns = columns
        self.df_four.columns = columns


        def replacing_and_converting(data, segmento):
            columns = ['numero_de_empresas','pessoal_ocupado_total', 'pessoal_ocupado_assalariados']
            for column in columns:
                for index, value in enumerate(data[column]):
                    if str(value).isdigit():
                        data.loc[index, column] = value
                    elif str(value) == 'x':
                        # quando o valor é igual x, ele representa que as empresas não declararam
                        # o valor com o intuito de não identificar as empresas, geralmente,
                        # utilizado as divisões que possuem só uma empresa, no entanto,
                        # em alguns casos, também utilizados para divisões com mais de uma empresa
                        data.loc[index, column] = -1
                    else:
                        # quando o valor do campo é igual a '-', ele representa zero absoluto 
                        # não decorrente de arredondamento
                        data.loc[index, column] = 0

                data[column] = data[column].astype('float64')

            data['divisão_id'].astype('object', inplace=True)

            if segmento == 1:
                value = 'Empresas (com 10 ou mais pessoas ocupadas assalariadas e até 8 anos de idade)'
                data['segmento'] = np.where(data['segmento'] == value,
                                           'Até 8 anos de idade', 'Geral')
            elif segmento == 2:
                value = 'Empresas de \nalto crescimento'
                data['segmento'] = np.where(data['segmento'] == value,
                                           'Alto Crescimento', 'Gazela')

            return data

        self.df_one = replacing_and_converting(self.df_one, 1)
        self.df_two = replacing_and_converting(self.df_two, 1)
        self.df_three = replacing_and_converting(self.df_three, 2)
        self.df_four = replacing_and_converting(self.df_four, 2)

        def concatenating_df(dataframe_one, dataframe_two, keys, new_name):
            data_new = pd.concat([dataframe_one, dataframe_two], axis=0,
                                 keys=keys)
            data_new.reset_index(inplace=True)
            data_new.drop('level_1', axis=1, inplace=True)
            data_new.rename({'level_0': new_name}, axis=1, inplace=True)
            return data_new
        
        self.df_geral = concatenating_df(self.df_one, self.df_two, ['2014','2015'], 'year')
        self.df_autocrescimento = concatenating_df(self.df_three, self.df_four, ['2014','2015'], 'year')
        self.df = concatenating_df(self.df_geral, self.df_autocrescimento, ['geral','altocrescimento'], 'base_de_dados')

    def main(self):
        self.wrangling()
        print('dataset final - shape', self.df.shape)

        self.df.to_csv('merged.csv', index=False)


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    import os

    os.chdir('/home/rafael/Documents/the_hive/the_hive_test/data')
    merging_files = CombinandoArquivos()
    merging_files.main()