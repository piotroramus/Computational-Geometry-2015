#ifdef __cplusplus
extern "C" {
#endif

#define REAL double

void exactinit();
REAL orient2dfast(REAL *pa, REAL *pb, REAL *pc);
REAL orient2dexact(REAL *pa, REAL *pb, REAL *pc);
REAL orient2dslow(REAL *pa, REAL *pb, REAL *pc);

#ifdef __cplusplus
}
#endif