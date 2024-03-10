%{
#include <ctype.h>

int words_number = 0;
int lines_number = 1;
%}


%%
    /* Saut de ligne. */
\n	{ ++lines_number; }   	

    /* Tout ce qui exclu un saut de ligne ou un ou des espace(s) ou des cobinaisons. */
[^\n ]+  { ++words_number; }	   

    /* Autre. */
.		;   
%%


int main()
{
    yylex();
    printf("Il y a %d lignes dans votre fichier\n ", lines_number );
    printf("Il y a %d mots dans votre fichier\n", words_number );
    return 0;
}