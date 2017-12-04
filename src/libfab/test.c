#include <stdlib.h>
#include <stdio.h>

#include "asdf/asdf.h"
#include "asdf/file_io.h"
#include "asdf/cms.h"

#include "formats/mesh.h"
#include "formats/stl.h"

int main()
{
    printf("Loading asdf\n");
    ASDF* asdf = asdf_read("test.asdf");
    //ASDF* asdf = asdf_read("/Users/mkeeter/grad/cba/proj/lace/lace.asdf");
    printf("Triangulating\n");
    Mesh* mesh = triangulate_cms(asdf);
    printf("Freeing asdf\n");
    free_asdf(asdf);
    printf("Saving stl\n");
    save_stl(mesh, "mesh.stl");
    printf("Freeing mesh\n");
    free_mesh(mesh);
    return 0;
}
