## CAP 394 - Data Science

**Alunos:** Fabiana Zioti, Gabriel Sansigolo e Rafael Mariano

**Resumo:** As queimadas são atividades que causam impactos negativos no âmbito social, ambiental e econômico. Essas consequências motiva diversas pesquisas relacionadas à ocorrência de incêndios e seus impactos em diversos biomas. O objetivo deste trabalho é realizar um estudo sobre os índices espectrais aliado a aplicação de métodos de aprendizado de máquina, com o  propósito de verificar se uma perspectiva automática no processo de detecção de cicatrizes de queimadas possui um resultado similar ao método de detecção semiautomático, realizado pelos especialistas. Visando futuramente, aderir aos métodos automáticos no processo de detecção de queimadas.

**Sumario:**

* [1 Análise Exploratória dos Dados](https://github.com/GSansigolo/CAP-240-394/blob/master/src/analise_dados/analise.ipynb)
* 2 Algoritmos de Aprendizado
    * 2.1 Abordagem por Região (Dados Shapefile-Queimadas)
        * [Máquina Vetores de Suporte (SVM)](https://github.com/GSansigolo/CAP-240-394/blob/master/src/SVM/SVM.ipynb)
        * [Rede Neural Perceptron Multicamadas (MLP)](https://github.com/GSansigolo/CAP-240-394/blob/master/src/MLP/neural_network.ipynb)
        * [Árvore de Decisão](https://github.com/GSansigolo/CAP-240-394/blob/master/src/Decision-Tree/decision_tree_sklearning.ipynb)
    * 2.2 Abordagem Pixel-a-Pixel 
        * [Indices Espectrais](https://github.com/GSansigolo/CAP-240-394/blob/master/src/landsat_8_object/NDVI-Difference.ipynb)
        * [Convolutional Neural Network (CNN)](https://github.com/GSansigolo/CAP-240-394/blob/master/src/MLP/data_science.ipynb) 
    * 2.2 Códigos Auxiliares
        * [Composição RGB](https://github.com/GSansigolo/CAP-240-394/blob/master/src/cut-areas/prepDataTest.ipynb)
        * [Preparação dos Dados para Teste (CNN)](https://github.com/GSansigolo/CAP-240-394/blob/master/src/cut-areas/prepDataTest.ipynb)
        * [Preparação dos Dados para Treinamento (CNN)](https://github.com/GSansigolo/CAP-240-394/blob/master/src/cut-areas/prepDataTrainQ.ipynb)
        * [Mascara Nuvem](https://github.com/GSansigolo/CAP-240-394/blob/master/src/cloud-mask/cloud-mask.ipynb)
* [3 Resultados e Conclusões](https://github.com/GSansigolo/CAP-240-394/blob/master/src/MLP/data_science.ipynb)

