#include <string.h>
2#include <math.h>

// Simplified min function
int min(int a, int b, int c) {
    int min_val = a;
    if (b < min_val) min_val = b;
    if (c < min_val) min_val = c;
    return min_val;
}

int levenshtein(char *s1, char *s2) {
    int threshold = 5 ;
    unsigned int s1len, s2len, x, y, lasting, olddiag;
    s1len = strlen(s1);
    s2len = strlen(s2);

    // Return early if the length difference exceeds the threshold
    if (abs((int)s1len - (int)s2len) > threshold) {
        return 100;
    }

    unsigned int column[s1len + 1];

    // Initialize the column array
    for (y = 0; y <= s1len; y++)
        column[y] = y;

    for (x = 1; x <= s2len; x++) {
        column[0] = x;
        int min_in_column = column[0];  // Track minimum value in current column for early exit

        for (y = 1, lasting = x - 1; y <= s1len; y++) {
            olddiag = column[y];
            column[y] = min(column[y] + 1, column[y - 1] + 1, lasting + (s1[y - 1] == s2[x - 1] ? 0 : 1));
            lasting = olddiag;

            // Track minimum value for early termination
            if (column[y] < min_in_column) {
                min_in_column = column[y];
            }
        }

        // If the minimum value in this column exceeds the threshold, return early
        if (min_in_column > threshold) {
            return 100;
        }
    }
    return column[s1len];
}
