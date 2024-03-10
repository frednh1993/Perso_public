%{
#include <ctype.h>
#define End 0
#define Single_line_comment 1
#define Multi_line_comment 2
%}
SINGLE_LINE_COMMENT \/\/
MULTILINE_COMMENT_START \/\*
MULTILINE_COMMENT_END \*\/

%%

{SINGLE_LINE_COMMENT}.*\n                                   {return Single_line_comment;}
{MULTILINE_COMMENT_START}[^\*\/]*{MULTILINE_COMMENT_END}    {return Multi_line_comment;}
.|\n                                                        ;
%%
main() {
    int token;
    while ((token = yylex()) != End) {
        switch(token) {
            case Single_line_comment :
                printf("Commentaire trouvé sur une ligne:\n%s", yytext);
                break;

            case Multi_line_comment :
                printf("Commentaire trouvé sur plusieurs lignes:\n%s\n", yytext);
                break;
        }
    }

}