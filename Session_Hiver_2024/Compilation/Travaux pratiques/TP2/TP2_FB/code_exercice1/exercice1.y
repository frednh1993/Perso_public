%{
    #include <stdio.h>
%}

%start S

%%
S : B A { printf("Action de la règle S -> BA\n"); };
A : 'a' B A { printf("Action de la règle A -> aBA\n"); }
  | /* epsilon */ { printf("Action de la règle A -> ε\n"); };
B : 'b' C D { printf("Action de la règle B -> bCD\n"); };
C : 'c' { printf("Action de la règle C -> c\n"); }
  | /* epsilon */ { printf("Action de la règle C -> ε\n"); };
D : 'd' { printf("Action de la règle D -> d\n"); }
  | /* epsilon */ { printf("Action de la règle D -> ε\n"); };
%%


void yyerror(char *msg) {
}

char alo[256], *txt = alo ;
int yylex(void) {
    if(*txt)
        return *txt++ ;
    else
        return 0 ;
}

int main(void) {
    printf("Taper le texte à tester : ") ;
    fflush(stdout) ;
    scanf("%s", alo) ;
    if( !yyparse())
        printf("SUCCES !\n") ;
    else
        printf("ECHEC !\n") ;
}