void decodificarHexa(char *hexa, char *binario) {
    binario[0] = '\0';
    for (int i = 0; i < strlen(hexa); i++) {
        switch (hexa[i]) {
            case '0': strcat(binario, "0000"); break;
            case '1': strcat(binario, "0001"); break;
            case '2': strcat(binario, "0010"); break;
            case '3': strcat(binario, "0011"); break;
            case '4': strcat(binario, "0100"); break;
            case '5': strcat(binario, "0101"); break;
            case '6': strcat(binario, "0110"); break;
            case '7': strcat(binario, "0111"); break;
            case '8': strcat(binario, "1000"); break;
            case '9': strcat(binario, "1001"); break;
            case 'A': case 'a': strcat(binario, "1010"); break;
            case 'B': case 'b': strcat(binario, "1011"); break;
            case 'C': case 'c': strcat(binario, "1100"); break;
            case 'D': case 'd': strcat(binario, "1101"); break;
            case 'E': case 'e': strcat(binario, "1110"); break;
            case 'F': case 'f': strcat(binario, "1111"); break;
            default: printf("caracter invalido em um hexadecimal"); exit(0);
        }
    }
}

void decodificarEndereco(char *endereco, int *rotulo, int *conjunto, int bitsPorRotulo, int bitsPorConjunto){
    char bitsRotulo[33] = {0};
    char bitsConjunto[33] = {0};

    // pega os bits do endereco e ja transforma em decimal
    for(int i = 0; i < bitsPorRotulo; i++){
        bitsRotulo[i] = endereco[i];
    }
    *rotulo = strtol(bitsRotulo, NULL, 2);

    // pega os bits do conjunto e ja transforma em decimal
    for(int i = bitsPorRotulo, j = 0; j < bitsPorConjunto; i++, j++){
        bitsConjunto[j] = endereco[i];
    }
    *conjunto = strtol(bitsConjunto, NULL, 2); 
}