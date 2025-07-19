void gravarArquivo(int politicaDeEscrita, int tamanhoLinha, int numeroDeLinhas, int associatividade, int substituicao, int tempoAcerto, int tempoMP, char *arquivoSaida,  int totalLeitura, int totalEscrita, int TotalEnderecos, int totalEscritaMP, int totalLeituraMP, float taxaAcertoLeitura, float taxaAcertoEscrita, float taxaAcertoGlobal,  float tempoMedioAcesso, int acertoLeitura, int acertoEscrita) {                                                                     
    
    FILE *f; 

    f = fopen(arquivoSaida, "w");

    if (f == NULL) {
        printf("Erro ao abrir/criar o arquivo!\n");
        return; 
    }

    // dados que vamos passar pra escrever no arquivo
    fprintf(f, "PARAMETROS DE ENTRADA: \n\n");
    fprintf(f, "Politica de escrita: %s \n", (politicaDeEscrita == 0) ? "write-through" : "write-back");
    fprintf(f, "tamanhoLinha: %d \n", tamanhoLinha);
    fprintf(f, "numeroDeLinhas: %d \n", numeroDeLinhas);
    fprintf(f, "associatividade: %d \n", associatividade);
    fprintf(f, "Politica de Substituicao: %s \n", (substituicao == 0) ? "LRU (Least Recently Used)" : "Aleatoria");
    fprintf(f, "tempoAcerto: %d \n", tempoAcerto);
    fprintf(f, "tempoMP: %d \n\n\n", tempoMP);

    fprintf(f, "PARAMETROS DE SAIDA: \n\n");
    fprintf(f, "totalLeitura: %d \n", totalLeitura);
    fprintf(f, "totalEscrita: %d \n", totalEscrita);
    fprintf(f, "TotalEnderecos: %d \n", TotalEnderecos);
    fprintf(f, "totalEscritaMP: %d \n", totalEscritaMP);
    fprintf(f, "totalLeituraMP: %d \n", totalLeituraMP);
    fprintf(f, "taxaAcertoLeitura: %.4f = %d \n", taxaAcertoLeitura, acertoLeitura);
    fprintf(f, "taxaAcertoEscrita: %.4f = %d \n", taxaAcertoEscrita, acertoEscrita);
    fprintf(f, "taxaAcertoGlobal: %.4f = %d \n", taxaAcertoGlobal, acertoEscrita + acertoLeitura);
    fprintf(f, "tempoMedioAcesso: %.4f \n", tempoMedioAcesso);

    fclose(f);
}