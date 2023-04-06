import cython

from libc.string cimport strlen, memset

DEF E_CAP = 16384 

ctypedef (char*, char*) StrPair

cdef unsigned int edit_distance(char* src, char* dst):
    cdef Py_ssize_t src_len = strlen(src)
    cdef Py_ssize_t dst_len = strlen(dst)

    if src_len == 0:
        return dst_len
    if dst_len == 0:
        return src_len

    cdef unsigned int E[E_CAP]
    memset(E, 0, E_CAP * sizeof(unsigned int))

    cdef Py_ssize_t i = 0
    cdef Py_ssize_t j = 0

    for i in range(src_len + 1):
        E[(i*src_len)] = i
    for i in range(dst_len + 1):
        E[i] = i
    
    cdef unsigned int a, b, c
    for i in range(1, src_len + 1):
        for j in range(1, dst_len + 1):
            # delete
            a = E[((i - 1)*src_len) + j] + 1
            # insertion
            b = E[(i*src_len) + (j - 1)] + 1
            # substitution
            c = E[((i - 1)*src_len) + (j - 1)]
            if src[i - 1] != dst[j - 1]:
                c += 1

            E[(i * src_len) + j] = min(a, b, c)

    return E[(src_len)*(src_len) + (dst_len)]

@cython.cdivision(True)
cdef float score(unsigned int distance, unsigned int max_distance):
    if distance == 0:
        return 0.0
    
    return 1 - (distance / float(max_distance))

cpdef (StrPair, float) score_pair(StrPair pair):
    len_f0 = strlen(pair[0])
    len_f1 = strlen(pair[1])

    max_len = len_f0 if len_f0 > len_f1 else len_f1
    distance = edit_distance(pair[0], pair[1])

    return (pair, score(distance, max_len))

