void lerParametros(int *escrita, int *tamanhoLinha, int *tamanhoCache, int *associatividade, int *substituicao, int tempoAcerto, int tempoMP, char *arquivoSaida){
    printf("Seja bem vindo!!\n");
    printf("------------------------\n");
    printf("Politica de escrita: 0 - write-through e 1 - write-back\n");
    scanf("%d", &*escrita);
    printf("Tamanho da linha: deve ser potencia de 2, em bytes:\n");
    scanf("%d", &*tamanhoLinha);
    printf("Tamanho da cache: deve ser potencia de 2:\n");
    scanf("%d", &*tamanhoCache);
    printf("Associatividade (numero de linhas) por conjunto: deve ser potencia de 2 (minimo 1 e maximo igual ao numero de linhas):\n");
    scanf("%d", &*associatividade);
    printf("Politica de Substituicao: 0 - LRU (Least Recently Used) e 1 - Aleatoria:\n");
    scanf("%d", &*substituicao);
    printf("Tempo de acesso quando encontra (hit time): %d nanossegundos:\n", tempoAcerto);
    printf("Tempos de leitura/escrita: %d nanossegundos:\n", tempoMP);
    printf("digite o nome do arquivo de saida:\n");
    scanf("%s", arquivoSaida);
}