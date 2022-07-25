grammar ep;

policy : (statement)+;

statement: identifier COLON expression (granularities)? (constraints)?;

expression: name | identifier | literal;

name: (component slash)+ component;

component: literal | identifier | function;

identifier: STRING | ustring | hstring | variable;

literal: (AP)(STRING)(AP);

constraints: WHERE constraint ( OR constraint)*;

constraint: BO constraint_body (COMA constraint_body)* BC;

constraint_body: identifier COLON components (OR components)*;

components: (literal | function);

function: STRING BRACKET;

granularities: ENCRYPTEDBY TBO granularity (COMA granularity)* TBC;

granularity: expression;

TBO: '[';

TBC: ']';

COLON: ':';

AP: '"';

AND: '&';

BO: '{';

BC: '}';

BRACKET: '()';

OR: '|';

COMA: ',';

fragment A:('a'|'A');
fragment B:('b'|'B');
fragment C:('c'|'C');
fragment D:('d'|'D');
fragment E:('e'|'E');
fragment F:('f'|'F');
fragment G:('g'|'G');
fragment H:('h'|'H');
fragment I:('i'|'I');
fragment J:('j'|'J');
fragment K:('k'|'K');
fragment L:('l'|'L');
fragment M:('m'|'M');
fragment N:('n'|'N');
fragment O:('o'|'O');
fragment P:('p'|'P');
fragment Q:('q'|'Q');
fragment R:('r'|'R');
fragment S:('s'|'S');
fragment T:('t'|'T');
fragment U:('u'|'U');
fragment V:('v'|'V');
fragment W:('w'|'W');
fragment X:('x'|'X');
fragment Y:('y'|'Y');
fragment Z:('z'|'Z');

ENCRYPTEDBY: E N C R Y P T E D B Y;

WHERE: W H E R E;

ustring: (UNDERSCORE)(STRING);

hstring: (HASH)(STRING);

variable: (VAR)(STRING);

UNDERSCORE: '_';

HASH: '#';

VAR: '$';

SIGNEDBY: '<=';

slash: '/';

STRING: ([a-zA-Z])([a-zA-Z0-9]|UNDERSCORE)*;

WS: [ \r\n\t]+ -> skip;

COMMENT: '//' ~[\r\n]* -> skip;
