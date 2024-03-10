%{
#include <ctype.h>
#define End 0
#define Word 1
#define Newline 2
int compteur_ligne =1;
int compteur_mot = 0;
%}
WORD [^\n ]+
NEWLINE \n
ANY .
%%
{WORD}          {return Word;}
{NEWLINE}       {return Newline;}
{ANY}           ;
%%
main() {
    int token;
    while ((token = yylex()) != End) {
        switch(token) {
            case Word :
                ++compteur_mot;
                break;
            case Newline :
                printf("%d mot(s) sur la ligne %d\n", compteur_mot, compteur_ligne);
                ++compteur_ligne;
                compteur_mot = 0;
                break;
        }
    }
    printf("%d mot(s) sur la ligne %d\n", compteur_mot, compteur_ligne);
}