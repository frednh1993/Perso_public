%{
#include <ctype.h>
%}
MINUSCULE [a-z]
MAJUSCULE [A-Z]
ENTIER -?[0-9]+
%%
{MINUSCULE} { printf("%c", toupper(yytext[0])); } /* min à maj */
{MAJUSCULE} { printf("%c", tolower(yytext[0])); } /* maj à min */
{ENTIER} {
    int number = atoi(yytext);

    if (number < 0)
        printf("\n%d est un entier négatif !\n", number);
    else
        printf("\n%d est un entier positif !\n", number);
}

. {printf("\n%s est null !\n",yytext);}
%%
