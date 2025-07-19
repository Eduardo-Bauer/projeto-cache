struct bloco{
    int rotulo;
    int lru;
    int dirtyBit;
};
typedef struct bloco BLOCO;

void limparCache(BLOCO *cache, int numeroLinha){
    for(int i = 0; i < numeroLinha; i++){
        cache[i].rotulo = -1;
        cache[i].lru = 0;
        cache[i].dirtyBit = 0;
    }
}

void resetarCache(BLOCO *cache, int numeroLinha, int *totalEscritaMP){
    for(int i = 0; i < numeroLinha; i++){
        if(cache[i].dirtyBit){
            *totalEscritaMP = *totalEscritaMP + 1;
            cache[i].dirtyBit = 0;
        }
    }
}

void calcularLru(BLOCO *cache, int bloco, int associatividade, int valorUsado){
    for(int j = 0; j < associatividade; j++){
        if(bloco + j != valorUsado){
            cache[bloco + j].lru++;
        }
    }
    cache[valorUsado].lru = 0;
}

void lerCache(BLOCO *cache, int rotulo, int conjunto, int *totalLeituraMP, int *totalEscritaMP, float *acertoLeitura, int associatividade, int substituicao, int escrita){
    int bloco = conjunto * associatividade;
    
    for(int i = 0; i < associatividade; i++){
        
        if(cache[bloco + i].rotulo == rotulo){
            *acertoLeitura = *acertoLeitura + 1;

            calcularLru(cache, bloco, associatividade, bloco + i);
            return;
        }
    }
    *totalLeituraMP = *totalLeituraMP + 1;

    if(escrita){
        // substituicao aleatorio
        if(substituicao){
            int aleatorio = (rand() % associatividade);

            if(cache[bloco + aleatorio].dirtyBit){
                *totalEscritaMP = *totalEscritaMP + 1;
            }

            cache[bloco + aleatorio].rotulo = rotulo;
            cache[bloco + aleatorio].dirtyBit = 0;

        // substituicao LRU
        }else{
            int maisVelho = bloco;
            for(int i = 0; i < associatividade; i++){
                if(cache[bloco + i].lru > cache[maisVelho].lru){
                    maisVelho = bloco + i;
                }
            }

            if(cache[maisVelho].dirtyBit){
                *totalEscritaMP = *totalEscritaMP + 1;
            }

            cache[maisVelho].rotulo = rotulo;
            cache[maisVelho].dirtyBit = 0;
            calcularLru(cache, bloco, associatividade, maisVelho);
        }

    }else{
        // substituicao aleatorio
        if(substituicao){
            int aleatorio = (rand() % associatividade);

            cache[bloco + aleatorio].rotulo = rotulo;

        // substituicao LRU
        }else{
            int maisVelho = bloco;
            for(int i = 0; i < associatividade; i++){
                if(cache[bloco + i].lru > cache[maisVelho].lru){
                    maisVelho = bloco + i;
                }
            }

            cache[maisVelho].rotulo = rotulo;
            calcularLru(cache, bloco, associatividade, maisVelho);
        }
    }
}

void escreverCache(BLOCO *cache, int rotulo, int conjunto, int *totalLeituraMP, int *totalEscritaMP, float *acertoEscrita, int associatividade, int substituicao, int escrita){
    int bloco = conjunto * associatividade;
    
    for(int i = 0; i < associatividade; i++){
        
        if(cache[bloco + i].rotulo == rotulo){
            *acertoEscrita = *acertoEscrita + 1;

            if(escrita){
                if(!cache[bloco + i].dirtyBit){
                    cache[bloco + i].dirtyBit = 1;
                }

            }else{
                *totalEscritaMP = *totalEscritaMP + 1; 
            }

            calcularLru(cache, bloco, associatividade, bloco + i);
            return;
        }
    }

    if(escrita){
        *totalLeituraMP = *totalLeituraMP + 1;
        
        // substituicao aleatorio
        if(substituicao){
            int aleatorio = (rand() % associatividade);
            
            if(cache[bloco + aleatorio].dirtyBit){
                *totalEscritaMP = *totalEscritaMP + 1;
            }

            cache[bloco + aleatorio].rotulo = rotulo;
            cache[bloco + aleatorio].dirtyBit = 1;

        // substituicao LRU
        }else{
            int maisVelho = bloco;
            for(int i = 0; i < associatividade; i++){
                if(cache[bloco + i].lru > cache[maisVelho].lru){
                    maisVelho = bloco + i;
                }
            }

            if(cache[maisVelho].dirtyBit){
                *totalEscritaMP = *totalEscritaMP + 1;
            }

            cache[maisVelho].rotulo = rotulo;
            cache[maisVelho].dirtyBit = 1;
            calcularLru(cache, bloco, associatividade, maisVelho);
        }

    }else{
    	*totalEscritaMP = *totalEscritaMP + 1;
	}
}