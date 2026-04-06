int max(int a, int b) {
    return (a > b) ? a : b;
}

int main() {
int m;
    int a = 1;
    int b = 49;
    int c = 4;
    int d = 3;
    int e = 67;
m = max(a,b);
m = max(m,c);
m = max(m,d);
m = max(m,e);


    return m;
}