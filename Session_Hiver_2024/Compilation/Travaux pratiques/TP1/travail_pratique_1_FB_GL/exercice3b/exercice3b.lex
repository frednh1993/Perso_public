%{
#include <ctype.h>
#include <stdbool.h>
#include <string.h> 

#define End 0
#define Word 1
#define Not_a_word 2

bool first_word = true;
int max_word_length = 0;
char *max_word;
%}


%%  
    /* Tout ce qui exclu un saut de ligne ou un ou des espace(s) ou des combinaisons. */
[^\n ]+  { return Word; }	   

    /* Autre. */
.|\n		{ return Not_a_word; } 
%%


void find_max_word() {

    if (first_word)
        {
            max_word_length = yyleng;
            max_word = (char *)malloc(max_word_length * sizeof(char) );
            first_word = false;
        }
    else 
        {
            if ( yyleng > max_word_length)
                {
                    strcpy(max_word, yytext);
                    max_word_length = yyleng;
                }
        }
}

int main() {
    int token;
    
    while ( (token = yylex()) != End) 
    {
        switch(token) 
        {
            case Word : 
                find_max_word();
                break;

            case Not_a_word : 
                break;
        }
    }
    
    if (first_word)
        printf("Il n'y a pas de mot dans ce fichier !\n");
    else 
        {
            printf("Le mot le plus long possède %d caractères.\n", max_word_length );
            printf("Il s'agit du mot %s\n", max_word );
        }

    free(max_word);
    return 0;
}