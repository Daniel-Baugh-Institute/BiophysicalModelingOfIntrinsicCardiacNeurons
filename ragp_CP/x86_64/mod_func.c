#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _SynE_reg(void);
extern void _ch_Kcna1ab1_md80769_reg(void);
extern void _ch_Kcnc1_md74298_reg(void);
extern void _ch_Scn1a_cp35_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"mod/SynE.mod\"");
    fprintf(stderr," \"mod/ch_Kcna1ab1_md80769.mod\"");
    fprintf(stderr," \"mod/ch_Kcnc1_md74298.mod\"");
    fprintf(stderr," \"mod/ch_Scn1a_cp35.mod\"");
    fprintf(stderr, "\n");
  }
  _SynE_reg();
  _ch_Kcna1ab1_md80769_reg();
  _ch_Kcnc1_md74298_reg();
  _ch_Scn1a_cp35_reg();
}