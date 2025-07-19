void lerArquivo(char binarios[][33], char *acoes, char *arquivo) {
    FILE *f = fopen(arquivo, "r");
    char hexa[9];
    char acao;
    int i = 0;

    if (!f) {
        printf("Erro ao abrir o arquivo\n");
        exit(0);
    }

    // leitura do arquivo de entrada
    while (fscanf(f, "%8s %c", hexa, &acao) == 2) {
        // coloca o hexadecimal para binario dentro da tupla de binarios
        decodificarHexa(hexa, binarios[i]);
        acoes[i++] = acao;
        // printf("%d - %s - %c\n", i-1, binarios[i-1], acoes[i-1]);
    }
    fclose(f);
}