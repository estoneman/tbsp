#include <sys/errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define UNUSED(x) (void)(x)
#define LEET_LEN 154 // includes null terminator
#define DNS_LIST_CAP 1024

int readline(char* buf, char* fn, char* perm)
{

	FILE* fp;
	fp = fopen(fn, perm);
    if (fp == NULL) {
        fprintf(stderr, "Could not read file\n");
        exit(1);
    }

	// populate leet buffer
	fgets(buf, LEET_LEN, fp);

	fclose(fp);

	return 0;
}

int readfile(char* buf, const char* fn, const char* perm)
{
    UNUSED(buf);
    FILE* fp = fopen(fn, perm);
    if (fp == NULL) {
        fprintf(stderr, "Could not read file %s: %s\n", fn, strerror(errno));
        return -1;
    }

    size_t nread = fread(buf, DNS_LIST_CAP, 1, fp);

    fclose(fp);

    return nread;
}

size_t min(size_t a, size_t b, size_t c) {
    size_t min = a;
    if (b < min)
        min = b;
    else if (c < min)
        min = c;

    return min;
}

size_t max(size_t a, size_t b) {
    return (a < b ? b : a);
}

int edit_distance(const char* X, const char* Y) {
    size_t X_sz = strlen(X);
    size_t Y_sz = strlen(Y);

    if (X_sz == 0)
        return Y_sz;
    else if (Y_sz == 0)
        return X_sz;

    size_t x_axis = X_sz + 1;
    size_t y_axis = Y_sz + 1;

    size_t E[x_axis][y_axis];
    
    for (size_t i = 0; i < x_axis; ++i) {
        for (size_t j = 0; j < y_axis; ++j) {
            if (i == 0)
                E[i][j] = j;
            else if (j == 0)
                E[i][j] = i;
            else
                E[i][j] = 0;
        }
    }

    for (size_t i = 1; i < x_axis; ++i) {
        for (size_t j = 1; j < y_axis; ++j) {
            size_t a = E[i - 1][j] + 1;
            size_t b = E[i][j - 1] + 1;
            size_t c = E[i - 1][j - 1];
            if (X[i - 1] != Y[j - 1])
                c += 1;

            E[i][j] = min(a, b, c);
        }
    }

    return E[X_sz][Y_sz];
}

float scoring(int ed, int max_ed)
{
    if (ed == 0)
        return 1.0f;
    return 1 - (ed / (float)max_ed);
}

int main(int argc, char *argv[])
{
    UNUSED(argc);
    UNUSED(argv);

    char *leet = (char*) malloc(LEET_LEN); 
    readline(leet, "leet.map", "r");

    char *dns = (char*) malloc(DNS_LIST_CAP);
    const char* fn = "domains.in";

    size_t rc = readfile(dns, fn, "r");

    if (!rc) {
        fprintf(stderr, "Could not read file %s\n", fn);
        free(leet);
        free(dns);

        return EXIT_FAILURE;
    }

    char domain[128];
    size_t domain_sz = 0;

    char translated[128];
    size_t translated_sz = 0; 

    printf("Domain,Leet,Edit Distance,Score\n");
    for (size_t i = 0; i < DNS_LIST_CAP; ++i) {
        domain_sz = 0;
        translated_sz = 0;

        while (dns[i] != '\n') {
            domain[domain_sz++] = dns[i++];
        }
        domain[domain_sz] = '\0';

        for (size_t j = 0; j < strlen(domain); ++j) {
            char leet_char = leet[domain[j] % LEET_LEN];
            if (leet_char == '-')
                translated[translated_sz++] = domain[j];
            else
                translated[translated_sz++] = leet_char;
        }
        translated[translated_sz] = '\0';
        int ed = edit_distance(domain, translated);
        printf("%s,%s,%d,%.02f\n", domain,
                translated,
                ed,
                scoring(ed, max(strlen(domain), strlen(translated))));
    }

    free(leet);
    free(dns);

    return EXIT_SUCCESS;
}

