#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma pack(1)
typedef struct _Endereco Endereco;

struct _Endereco
{
	char logradouro[72];
	char bairro[72];
	char cidade[72];
	char uf[72];
	char sigla[2];
	char cep[8];
	char lixo[2];
};


int main(int argc, char**argv)
{
    FILE *f;
	Endereco e;
	int qt;
	int c=0;
	int a=0;
	long posicao, primeiro, ultimo, meio;

	if(argc != 2)
	{
		fprintf(stderr, "USO: %s [CEP]", argv[0]);
		return 1;
	}
	f = fopen("cep_ordenado.dat","r");
	fseek(f,0,SEEK_END);
	posicao = ftell(f);
	rewind(f);
	primeiro = 0;
	ultimo = (posicao/sizeof(Endereco))-1;

    while(primeiro <= ultimo){

        meio = (primeiro+ultimo)/2;
        fseek(f,meio*sizeof(Endereco),SEEK_SET);
        fread(&e,sizeof(Endereco),1,f);
        c++;
		if(strncmp(argv[1],e.cep,8)==0)
		{
			printf("%.72s\n%.72s\n%.72s\n%.72s\n%.2s\n%.8s\n",e.logradouro,e.bairro,e.cidade,e.uf,e.sigla,e.cep);
			a=1;
			break;
		}
		else if(strncmp(argv[1],e.cep,8)<0){
            ultimo=meio-1;
		}
		else{
            primeiro=meio+1;
		}
		rewind(f);
    }

	fclose(f);
	if(a==0){
       printf("CEP nao encontrado");
	}
	else{
        printf("\nNumero de registros procurados : %i \n",c);
	}
}
