%{
#include <ctype.h>
#include <stdbool.h> 

#define End 0
#define Entier 1
#define Aucun_entier 2
    /* first_num à false indique qu'un mot n'a pas été trouvé, 
       first_num à true indique qu'au moins un mot a pas été trouvé.*/
bool first_num = false;
int num = 0;
int max_num = 0;
int sum_all_num = 0;
%}

ENTIER [0-9]+


%%
    /* Espace(s) ou saut de ligne. */
[ \n]                                                   { return Aucun_entier; }

    /* Les mots composés de lettre(s) et de chiffre(s) ou uniquement de lettre(s). */
[a-zA-Z']*-?{ENTIER}*[a-zA-Z']+-?{ENTIER}*[a-zA-Z']*    { return Aucun_entier; }

    /* Entiers positifs ou négatifs. */
-?{ENTIER}                                              { num = atoi(yytext); return Entier; } 

    /* Autre. */
.		                                                { return Aucun_entier; }      
%%


void max_value_and_sum()
{
    if (first_num)
        {
            max_num = num;
            sum_all_num = sum_all_num + num;
        }
    else 
        {
            first_num = true;
            sum_all_num = sum_all_num + num;
            if(num > max_num)
                max_num = num;
        }
}

int main()
{
    int token;
    
    /* yylex() := analyse du flux d'entrée et reconnaissance des jetons */
    while ((token = yylex()) != End) 
    {
        switch(token) 
        {
            case Entier : 
                max_value_and_sum();
                break;

            case Aucun_entier : 
                break;
        }
    }
    
    if (!first_num)
        printf("Il n'y a pas de valeur entière dans ce fichier !\n");
    else 
        {
            printf("La valeur entière maximale est %d.\n", max_num );
            printf("La somme de toutes les valeurs entières du fichier est %d.\n", sum_all_num );
        }

    return 0;
}