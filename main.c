#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include "funcoes/decodificador.h"
#include "funcoes/leitor_de_arquivo.h"
#include "funcoes/parametros.h"
#include "funcoes/gravador_de_arquivo.h"
#include "cache.h"

int main() {
    srand(time(NULL));
    // informações gerais
    int qtdhexa = 51200; // 100
    char arquivoEntrada[50] = "entradas/oficial.cache";
    char arquivoSaida[50];
    char acoes[qtdhexa];
    char binarios[qtdhexa][33];
    int bitsPorRotulo = 0;
    int bitsPorConjunto = 0; 
    int bitsPorPalavra = 0; 

    // parametros para analise
    int escrita;
    int tamanhoLinha;
    int tamanhoCache;
    int associatividade;
    int tamanhoEndereco = 32; 
    int substituicao;
    float tempoAcerto = 5;
    float tempoMP = 70;

    // parametros para os resultados da simulacao
    float entradasEscrita = 0;
    float entradasLeitura = 0;
    int totalEscritaMP = 0;
    int totalLeituraMP = 0;
    float acertoLeitura = 0;
    float acertoEscrita = 0;
    float taxaAcertoLeitura;
    float taxaAcertoEscrita;
    float taxaAcertoGlobal; 
    float tempoMedioAcesso;

    lerParametros(&escrita, &tamanhoLinha, &tamanhoCache, &associatividade, &substituicao, tempoAcerto, tempoMP, arquivoSaida);                                                                                                               

    bitsPorPalavra = (int)log2(tamanhoLinha);

    bitsPorConjunto = (int)log2((tamanhoCache / tamanhoLinha) / associatividade);

    bitsPorRotulo = tamanhoEndereco - bitsPorPalavra - bitsPorConjunto;

    BLOCO *cache = (BLOCO *)malloc((tamanhoCache / tamanhoLinha)*sizeof(BLOCO));
    if(cache == NULL){
        printf("Erro de alocação de memória\n");
        exit(0);    
    }

    limparCache(cache, (tamanhoCache / tamanhoLinha));
    lerArquivo(binarios, acoes, arquivoEntrada);

    for(int i = 0; i < qtdhexa; i++){
        int rotulo;
        int conjunto;

        decodificarEndereco(binarios[i], &rotulo, &conjunto, bitsPorRotulo, bitsPorConjunto);

        if(acoes[i] == 'R'){
            entradasLeitura++;
            lerCache(cache, rotulo, conjunto, &totalLeituraMP, &totalEscritaMP, &acertoLeitura, associatividade, substituicao, escrita);

        }else{
            entradasEscrita++;
            escreverCache(cache, rotulo, conjunto, &totalLeituraMP, &totalEscritaMP, &acertoEscrita, associatividade, substituicao, escrita);
        }
    }

    if(escrita){
        resetarCache(cache, tamanhoCache / tamanhoLinha, &totalEscritaMP);
    }

    taxaAcertoLeitura = (acertoLeitura * 100) / entradasLeitura;
    taxaAcertoEscrita = (acertoEscrita * 100) / entradasEscrita;
    taxaAcertoGlobal = (acertoEscrita + acertoLeitura) * 100 / (float) qtdhexa;
    tempoMedioAcesso = tempoAcerto + (1 - taxaAcertoGlobal / 100) * tempoMP;

    //Gravações 
    gravarArquivo(escrita, tamanhoLinha, (tamanhoCache / tamanhoLinha), associatividade, substituicao, tempoAcerto, tempoMP, arquivoSaida, entradasLeitura, entradasEscrita, (entradasEscrita + entradasLeitura), totalEscritaMP, totalLeituraMP, taxaAcertoLeitura, taxaAcertoEscrita, taxaAcertoGlobal, tempoMedioAcesso, acertoLeitura, acertoEscrita);
    
    free(cache);
    return 0;
}