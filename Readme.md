Source code:
````
int hello(int a, string b){
    int X=20;
    float K=234324.2323;
    print "Próba";
}
int hello(int a){
    return a * 10;
}
int SUPER_TEST(){
    print K;
}

print "Test";

while(23) print "Test 123";

labelka: print "Jestem nazwna";

X = 212;

if (K == 10 && 5==7){
    while (10){
        print 2 + 3 * 100 / 2 + 1;
        K = 100;
        break;
    }
}

while(1){
    print 1;
    K = hello(2+2, "Sasas", (2*2)+2 == 2);
    if( X >= 10){
        continue;
    }
}


if( ( x>0) && (2<<10) || (2 ^ 1) & 4 & 5 != 5){
    K = 10;
    X = hello(K);
    print X;
}
````


AST Tree:
````
DECL
FUNDEF
| hello
| RET int
| ARG int a
| ARG string b
| DECL
| | int
| | | =
| | | | X
| | | | 20
| | float
| | | =
| | | | K
| | | | 234324.2323
| PRINT
| | "Próba"
FUNDEF
| hello
| RET int
| ARG int a
| DECL
| RETURN
| | *
| | | a
| | | 10
FUNDEF
| SUPER_TEST
| RET int
| DECL
| PRINT
| | K
PRINT
| "Test"
WHILE
| 23
| PRINT
| | "Test 123"
LABELED
| labelka
| PRINT
| | "Jestem nazwna"
=
| X
| 212
IF
| AND
| | ==
| | | K
| | | 10
| | ==
| | | 5
| | | 7
| DECL
| WHILE
| | 10
| | DECL
| | PRINT
| | | +
| | | | +
| | | | | 2
| | | | | /
| | | | | | *
| | | | | | | 3
| | | | | | | 100
| | | | | | 2
| | | | 1
| | =
| | | K
| | | 100
| | BREAK
WHILE
| 1
| DECL
| PRINT
| | 1
| =
| | K
| | CALL
| | | hello
| | | +
| | | | 2
| | | | 2
| | | "Sasas"
| | | ==
| | | | +
| | | | | *
| | | | | | 2
| | | | | | 2
| | | | | 2
| | | | 2
| IF
| | >=
| | | X
| | | 10
| | DECL
| | CONTINUE
IF
| ||
| | AND
| | | >
| | | | x
| | | | 0
| | | <<
| | | | 2
| | | | 10
| | &
| | | &
| | | | ^
| | | | | 2
| | | | | 1
| | | | 4
| | | !=
| | | | 5
| | | | 5
| DECL
| =
| | K
| | 10
| =
| | X
| | CALL
| | | hello
| | | K
| PRINT
| | X
````
